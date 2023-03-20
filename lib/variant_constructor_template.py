import flask_wtf
import wtforms


class ConstructorForm(flask_wtf.FlaskForm):
    title = wtforms.StringField('Название:', validators=[wtforms.validators.DataRequired()])
    theme = wtforms.SelectField('Тема:', choices=[("math", "Математика"), ("info", "Информатика"),
                                                  ("rus", "Русский Язык"), ("phys", "Физика"), ("chem", "Химия"),
                                                  ("bio", "Биология"), ("geo", "География"), ("soc", "Обществознание"),
                                                  ("lit", "Литература"), ("hist", "История"),
                                                  ("eng", "Английский Язык"), ("germ", "Немецкий Язык"),
                                                  ("fren", "Французский Язык"), ("span", "Испанский Язык")])
    secrecy = wtforms.StringField("Показывать ошибки ученикам после тестирования")
    submit = wtforms.SubmitField('Отправить')
