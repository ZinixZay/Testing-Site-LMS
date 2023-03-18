import flask_wtf
import wtforms


class RegisterForm(flask_wtf.FlaskForm):
    role = wtforms.SelectField('Вы:',
                               choices=[('teacher', 'Учитель'), ('student', 'Ученик')])
    login = wtforms.StringField('Логин', validators=[wtforms.validators.DataRequired()])
    password = wtforms.PasswordField('Пароль', validators=[wtforms.validators.DataRequired()])
    email = wtforms.StringField('Почта', validators=[wtforms.validators.DataRequired(), wtforms.validators.Email()])
    submit = wtforms.SubmitField('Зарегистрироваться')
