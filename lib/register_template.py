import flask_wtf
import wtforms


class RegisterForm(flask_wtf.FlaskForm):
    role = wtforms.SelectField('Вы:',
                               choices=[('Учитель', 'Учитель'), ('Ученик', 'Ученик')])
    login = wtforms.StringField('Логин', validators=[wtforms.validators.DataRequired()])
    password = wtforms.PasswordField('Пароль', validators=[wtforms.validators.DataRequired()])
    submit = wtforms.SubmitField('Зарегистрироваться')
