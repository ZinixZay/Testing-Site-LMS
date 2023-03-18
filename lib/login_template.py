import flask_wtf
import wtforms


class LoginForm(flask_wtf.FlaskForm):
    login = wtforms.StringField('Почта или Логин', validators=[wtforms.validators.DataRequired()])
    password = wtforms.PasswordField('Пароль', validators=[wtforms.validators.DataRequired()])
    remember_me = wtforms.BooleanField('Запомнить меня')
    submit = wtforms.SubmitField('Войти')
