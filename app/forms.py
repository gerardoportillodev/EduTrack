from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo

class LoginForm(FlaskForm):
    username = StringField('Usuario', validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    remember_me = BooleanField('Recordar sesión')
    submit = SubmitField('Iniciar Sesión')

class RegistrationForm(FlaskForm):  # Añade esta clase
    username = StringField('Usuario', 
                         validators=[DataRequired(), 
                                    Length(min=4, max=25)])
    password = PasswordField('Contraseña', 
                           validators=[DataRequired(), 
                                     Length(min=6)])
    password2 = PasswordField('Confirmar Contraseña',
                            validators=[DataRequired(),
                                      EqualTo('password')])
    submit = SubmitField('Registrarse')

class ExamForm(FlaskForm):  # Asegúrate que esta clase existe
    submit = SubmitField('Enviar Examen')