from flask import Blueprint, send_from_directory, render_template, redirect, url_for, flash, request, abort
from flask_login import login_user, logout_user, current_user, login_required
from sqlalchemy import func
from app import db
from app.models import User, Exam, Question, Answer
from app.forms import LoginForm, RegistrationForm, ExamForm
from wtforms import RadioField, validators
from wtforms.validators import DataRequired
import random

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
            
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('¡Registro exitoso! Por favor inicia sesión.', 'success')
        return redirect(url_for('main.login'))
    return render_template('register.html', form=form)

@main_bp.route('/dashboard')
@login_required
def dashboard():
    exams = current_user.exams.order_by(Exam.timestamp.desc()).all()
    
    # Calcular estadísticas
    subjects = ['lenguaje', 'matematicas', 'fisica']
    stats = {
        'total_exams': len(exams),
        'average_score': sum(exam.score for exam in exams) / len(exams) if exams else 0,
        'by_subject': {
            subject: {
                'count': len([e for e in exams if e.subject == subject]),
                'average': sum(e.score for e in exams if e.subject == subject) / 
                          len([e for e in exams if e.subject == subject]) if 
                          len([e for e in exams if e.subject == subject]) > 0 else 0
            } for subject in subjects
        }
    }
    
    return render_template('dashboard.html', exams=exams, stats=stats)

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
    if exam.user_id != current_user.id:
        abort(403)
    
    answers = (db.session.query(Answer, Question)
               .join(Question)
               .filter(Answer.exam_id == exam_id)
               .order_by(Question.id)
               .all())
    
    # Calcular estadísticas del examen
    correct_count = sum(1 for answer, _ in answers if answer.is_correct)
    incorrect_count = len(answers) - correct_count
        
    answer_list = [answer for answer, question in answers]  # Extract only Answer objects

    return render_template(
        'exam_results.html',
        exam=exam,
        answers=answer_list,  # Pass only the Answer objects
        correct_count=correct_count,
        incorrect_count=incorrect_count
    )

@main_bp.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)

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