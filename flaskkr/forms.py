from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, SubmitField, BooleanField
from wtforms.validators import DataRequired, EqualTo


class SignUpForm(FlaskForm):
    name = StringField('Escribe tu nombre', validators=[DataRequired()])
    username = StringField('Escribe tu nombre de ususario', validators=[DataRequired()])
    email = EmailField('Escribe tu email', validators=[DataRequired()])
    password = PasswordField('Escribe tu contraseña', validators=[DataRequired()])
    password2 = PasswordField('Confirma tu contraseña', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Crear cuenta')


class LoginForm(FlaskForm):
    email = EmailField('Escribe tu email', validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    remember = BooleanField('Recuérdame')
    submit = SubmitField('Entrar')


class UpdateDataForm(FlaskForm):
    new_name = StringField('Escribe un nuevo nombre')
    new_username = StringField('Escribe un nuevo nombre de usuario')
    new_email = EmailField('Escribe un nuevo email')
    password = PasswordField('Escribe tu contraseña para confirmar los cambios', validators=[DataRequired()])
    submit = SubmitField('Actualizar datos')


class UpdatePassword(FlaskForm):
    current_password = PasswordField('Actual contraseña', validators=[DataRequired()])
    new_password = PasswordField('Nueva contraseña', validators=[DataRequired()])
    new_password2 = PasswordField('Confirma tu nueva contraseña', validators=[DataRequired(), EqualTo('new_password', message='Las contraseñas no son iguales')])
    submit = SubmitField('Actualizar contraseña')


class AddTodo(FlaskForm):
    description = StringField('Añade una descripción', validators=[DataRequired()])
    submit = SubmitField('Agregar tarea')


class UpdateTodo(FlaskForm):
    description = StringField('Añade una nueva descripción', validators=[DataRequired()])
    submit = SubmitField('Actualizar todo')