import flask_wtf
import wtforms


class RegisterForm(flask_wtf.FlaskForm):
    role = wtforms.SelectField('Вы:',
                               choices=[('teacher', 'Учитель'), ('student', 'Ученик')])
    login = wtforms.StringField('Логин', validators=[wtforms.validators.DataRequired()])
    password = wtforms.PasswordField('Пароль', validators=[wtforms.validators.DataRequired()])
    submit = wtforms.SubmitField('Зарегистрироваться')
