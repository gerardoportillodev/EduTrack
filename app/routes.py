from flask import Blueprint, send_from_directory, render_template, redirect, url_for, flash, request, abort
from flask_login import login_user, logout_user, current_user, login_required
from sqlalchemy import func
from app import db, mail
from app.models import User, Exam, Question, Answer
from app.forms import LoginForm, RegistrationForm, ExamForm
from wtforms import RadioField, validators
from wtforms.validators import DataRequired
import random
from datetime import datetime, timedelta
from collections import defaultdict
from flask_mail import Message
from app import mail
from flask import current_app

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
@main_bp.route('/index')
def index():
    return render_template('index.html', current_user=current_user)

@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Usuario o contraseña inválidos', 'danger')
            return redirect(url_for('main.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        flash('¡Has iniciado sesión correctamente!', 'success')
        return redirect(next_page or url_for('main.dashboard'))
    return render_template('login.html', form=form)

@main_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión correctamente.', 'info')
    return redirect(url_for('main.index'))

@main_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user:
            flash('El nombre de usuario ya está en uso', 'danger')
            return redirect(url_for('main.register'))
            
        user = User(
            username=form.username.data,
            parent_email=form.parent_email.data  # <-- Agregado aquí
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('¡Registro exitoso! Por favor inicia sesión.', 'success')
        return redirect(url_for('main.login'))
    return render_template('register.html', form=form)

@main_bp.route('/dashboard')
@login_required
def dashboard():
    exams = Exam.query.filter_by(user_id=current_user.id).order_by(Exam.timestamp.asc()).all()
    subjects = ['matematicas', 'lenguaje', 'fisica']

    # Calcula promedios por materia
    by_subject = {}
    for s in subjects:
        subject_exams = [e for e in exams if e.subject == s]
        avg = sum(e.score for e in subject_exams) / len(subject_exams) if subject_exams else 0
        by_subject[s] = {
            'average': avg
        }

    # Mejor materia
    best_subject = max(by_subject.items(), key=lambda x: x[1]['average']) if by_subject else ('N/A', {'average': 0})

    # Stats generales
    total_exams = len(exams)
    overall_average = sum(e.score for e in exams) / total_exams if total_exams > 0 else 0

    stats = {
        'total_exams': total_exams,
        'overall_average': overall_average,
        'by_subject': by_subject,
        'best_subject': {
            'name': best_subject[0].capitalize(),
            'average': best_subject[1]['average']
        }
    }

    # --- Evolución del rendimiento por materia ---
    evolucion_labels = []
    evolucion_dict = {s: [] for s in subjects}

    for exam in exams:
        fecha = exam.timestamp.strftime('%d/%m/%Y')
        if fecha not in evolucion_labels:
            evolucion_labels.append(fecha)
        # Para cada materia, agrega el score si es de esa materia, si no, None
        for s in subjects:
            if exam.subject == s:
                evolucion_dict[s].append(exam.score)
            else:
                evolucion_dict[s].append(None)

    return render_template(
        "dashboard.html",
        stats=stats,
        exams=exams,
        evolucion_labels=evolucion_labels,
        evolucion_matematicas=evolucion_dict['matematicas'],
        evolucion_lenguaje=evolucion_dict['lenguaje'],
        evolucion_fisica=evolucion_dict['fisica'],
    )

@main_bp.route('/select_subject')
@login_required
def select_subject():
    return render_template('select_subject.html')

@main_bp.route('/start_exam/<subject>', methods=['GET', 'POST'])
@login_required
def start_exam(subject):
    if subject not in ['lenguaje', 'matematicas', 'fisica']:
        abort(404)
        
    questions = Question.query.filter_by(subject=subject).order_by(func.random()).limit(10).all()
    
    if not questions:
        flash(f'No hay preguntas disponibles para {subject.capitalize()}', 'warning')
        return redirect(url_for('main.select_subject'))
    
    class DynamicExamForm(ExamForm):
        pass
    
    for question in questions:
        setattr(DynamicExamForm, f'question_{question.id}', 
                RadioField(
                    question.question_text,
                    choices=[
                        ('a', question.option_a),
                        ('b', question.option_b),
                        ('c', question.option_c),
                        ('d', question.option_d)
                    ],
                    validators=[DataRequired()],
                    render_kw={'class': 'form-check-input'}
                ))
    
    form = DynamicExamForm()
    
    if form.validate_on_submit():
        exam = Exam(subject=subject, user_id=current_user.id)
        db.session.add(exam)
        db.session.commit()
        
        correct_answers = 0
        for question in questions:
            selected_option = getattr(form, f'question_{question.id}').data
            is_correct = (selected_option == question.correct_answer)
            if is_correct:
                correct_answers += 1
                
            feedback = generate_feedback(question, selected_option, is_correct)
            
            answer = Answer(
                exam_id=exam.id,
                question_id=question.id,
                selected_option=selected_option,
                is_correct=is_correct,
                feedback=feedback
            )
            db.session.add(answer)
        
        exam.score = round((correct_answers / len(questions)) * 100, 2)
        db.session.commit()
        
        flash('¡Examen completado! Revisa tus resultados.', 'success')
        return redirect(url_for('main.exam_results', exam_id=exam.id))
    
    return render_template('exam.html', form=form, subject=subject.capitalize(), questions=questions)

@main_bp.route('/exam_results/<int:exam_id>')
@login_required
def exam_results(exam_id):
    exam = Exam.query.get_or_404(exam_id)
    answers = Answer.query.filter_by(exam_id=exam.id).all()
    results = []
    correct_count = 0
    incorrect_count = 0
    for answer in answers:
        question = Question.query.get(answer.question_id)
        feedback = answer.feedback
        results.append({
            'question': question,
            'question_text': question.question_text,
            'user_answer': question.__dict__.get(f'option_{answer.selected_option}', ''),
            'correct_answer': question.__dict__.get(f'option_{question.correct_answer}', ''),
            'is_correct': answer.is_correct,
            'feedback': feedback
        })
        if answer.is_correct:
            correct_count += 1
        else:
            incorrect_count += 1

    # --- ENVÍA EL CORREO AQUÍ ---
    send_exam_results_email(current_user, exam, results)

    return render_template(
        'exam_results.html',
        exam=exam,
        answers=results,
        correct_count=correct_count,
        incorrect_count=incorrect_count
    )

@main_bp.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)


@main_bp.route('/exam_history')
@login_required
def exam_history():
    exams = Exam.query.filter_by(user_id=current_user.id).order_by(Exam.timestamp.desc()).all()
    return render_template('exam_history.html', exams=exams)

@main_bp.route('/compare_exam/<int:exam_id>')
@login_required
def compare_exam(exam_id):
    exam = Exam.query.get_or_404(exam_id)
    user_exams = Exam.query.filter_by(user_id=current_user.id).all()
    subject_exams = [e for e in user_exams if e.subject == exam.subject]

    overall_average = sum(e.score for e in user_exams) / len(user_exams) if user_exams else 0
    subject_average = sum(e.score for e in subject_exams) / len(subject_exams) if subject_exams else 0

    return render_template(
        'compare_exam.html',
        exam=exam,
        overall_average=overall_average,
        subject_average=subject_average
    )

def generate_feedback(question, selected_option, is_correct):
    if is_correct:
        return f"¡Correcto! {get_feedback_message(question, selected_option, True)}"
    else:
        correct_option = getattr(question, f'option_{question.correct_answer}')
        return (
            f"Incorrecto. La respuesta correcta era {question.correct_answer.upper()}: {correct_option}. "
            f"{getattr(question, f'feedback_{selected_option}')}"
        )

def get_feedback_message(question, option, is_correct):
    feedback = {
        'matematicas': {
            True: "Has aplicado correctamente los conceptos matemáticos.",
            False: "Revisa los cálculos y fórmulas aplicadas."
        },
        'lenguaje': {
            True: "Excelente comprensión del tema de lenguaje.",
            False: "Considera revisar los conceptos gramaticales o literarios."
        },
        'fisica': {
            True: "Buen trabajo aplicando los principios físicos.",
            False: "Verifica las unidades y fórmulas físicas relevantes."
        }
    }
    return feedback.get(question.subject, {}).get(is_correct, "")

def send_exam_results_email(user, exam, answers):
    from flask_mail import Message
    from flask import current_app
    from app import mail

    # Usa parent_email si existe y es válido, si no, usa username solo si es un correo
    recipient = user.parent_email if user.parent_email else user.username
    if not recipient or "@" not in recipient:
        print("No se puede enviar correo: destinatario inválido.")
        return  # No enviar si no hay destinatario válido

    correctas = [a for a in answers if a['is_correct']]
    incorrectas = [a for a in answers if not a['is_correct']]
    html_body = f"""
    <h3>Resultados del examen de {exam.subject.capitalize()}</h3>
    <p><strong>Calificación:</strong> {exam.score}%</p>
    <h4>Respuestas correctas:</h4>
    <ul>
    {''.join(f"<li>{a['question_text']}<br><em>Respuesta: {a['user_answer']}</em><br>Feedback: {a['feedback']}</li>" for a in correctas)}
    </ul>
    <h4>Respuestas incorrectas:</h4>
    <ul>
    {''.join(f"<li>{a['question_text']}<br><em>Tu respuesta: {a['user_answer']}</em><br>Respuesta correcta: {a['correct_answer']}<br>Feedback: {a['feedback']}</li>" for a in incorrectas)}
    </ul>
    """

    msg = Message(
        subject=f"Resultados del examen de {exam.subject.capitalize()}",
        recipients=[recipient],
        html=html_body,
        sender=current_app.config['MAIL_DEFAULT_SENDER']
    )
    mail.send(msg)

from flask import flash, redirect, url_for
from flask_login import login_required, current_user

@main_bp.route('/test_mail')
@login_required
def test_mail():
    from flask_mail import Message
    from app import mail
    from flask import current_app

    msg = Message(
        subject="Prueba de correo EduTrack",
        recipients=[current_user.parent_email or current_user.username],
        body="¡Este es un correo de prueba desde EduTrack!",
        sender=current_app.config['MAIL_DEFAULT_SENDER']
    )
    try:
        mail.send(msg)
        flash('Correo de prueba enviado correctamente.', 'success')
    except Exception as e:
        flash(f'Error al enviar el correo: {e}', 'danger')
    return redirect(url_for('main.profile'))