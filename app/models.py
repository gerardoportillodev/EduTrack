from flask_login import UserMixin
from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    parent_email = db.Column(db.String(120), nullable=True)
    
    exams = db.relationship('Exam', backref='student', lazy='dynamic')

    def __repr__(self):
        return f'<User {self.username}>'
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    # Los siguientes métodos ya están heredados de UserMixin:
    # - is_authenticated (propiedad que devuelve True si el usuario tiene credenciales válidas)
    # - is_active (propiedad que devuelve True si la cuenta de usuario está activa)
    # - is_anonymous (propiedad que devuelve False para usuarios reales)
    # - get_id() (método que devuelve el id del usuario como string)

class Exam(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(64))  # 'lenguaje', 'matematicas', 'fisica'
    score = db.Column(db.Float)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    answers = db.relationship('Answer', backref='exam', lazy='dynamic')

    def __repr__(self):
        return f'<Exam {self.subject} - {self.score}>'

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(64))
    question_text = db.Column(db.String(500))
    option_a = db.Column(db.String(200))
    option_b = db.Column(db.String(200))
    option_c = db.Column(db.String(200))
    option_d = db.Column(db.String(200))
    feedback_a = db.Column(db.String(1000))
    feedback_b = db.Column(db.String(1000))
    feedback_c = db.Column(db.String(1000))
    feedback_d = db.Column(db.String(1000))
    correct_answer = db.Column(db.String(1))  # 'a', 'b', 'c' o 'd'
    difficulty = db.Column(db.Integer)  # 1-5

    def __repr__(self):
        return f'<Question {self.id}: {self.question_text[:50]}...>'

class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    exam_id = db.Column(db.Integer, db.ForeignKey('exam.id'))
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    selected_option = db.Column(db.String(1))
    is_correct = db.Column(db.Boolean)
    feedback = db.Column(db.String(500))

    def __repr__(self):
        return f'<Ans {self.id}: {self.is_correct} {self.selected_option} ...>'