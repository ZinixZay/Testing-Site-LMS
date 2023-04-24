import flask_wtf
import wtforms


class ConstructorForm(flask_wtf.FlaskForm):
    title = wtforms.StringField('Название:', validators=[wtforms.validators.DataRequired()])
    theme = wtforms.SelectField('Тема:', choices=[("математика", "Математика"), ("информатика", "Информатика"),
                                                  ("русский язык", "Русский Язык"), ("физика", "Физика"),
                                                  ("химия", "Химия"), ("биология", "Биология"),
                                                  ("география", "География"), ("обществознание", "Обществознание"),
                                                  ("литература", "Литература"), ("история", "История"),
                                                  ("английский язык", "Английский Язык"),
                                                  ("немецкий язык", "Немецкий Язык"),
                                                  ("французский язык", "Французский Язык"),
                                                  ("испанский язык", "Испанский Язык")])
    secrecy = wtforms.StringField("Показывать ошибки ученикам после выполнения задания")
    submit = wtforms.SubmitField('Создать')
