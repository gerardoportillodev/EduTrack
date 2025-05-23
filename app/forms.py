from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo, Email, Optional

class LoginForm(FlaskForm):
    username = StringField('Usuario', validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    remember_me = BooleanField('Recordar sesión')
    submit = SubmitField('Iniciar Sesión')

class RegistrationForm(FlaskForm):
    username = StringField('Usuario', 
                         validators=[DataRequired(), 
                                    Length(min=4, max=25)])
    password = PasswordField('Contraseña', 
                           validators=[DataRequired(), 
                                     Length(min=6)])
    password2 = PasswordField('Confirmar Contraseña',
                            validators=[DataRequired(),
                                      EqualTo('password')])
    parent_email = StringField('Correo del padre/madre o estudiante', validators=[Optional(), Email()])
    submit = SubmitField('Registrarse')

class ExamForm(FlaskForm):
    submit = SubmitField('Enviar Examen')