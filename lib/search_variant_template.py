import flask_wtf
import wtforms


class SearchForm(flask_wtf.FlaskForm):
    search_type = wtforms.SelectField('Искать по:',
                                      choices=[('id', 'Идентификатору варианта'),
                                               ('title', 'Названию варианта'),
                                               ('theme', 'Теме варианта')])
    search_request = wtforms.StringField('Запрос:', validators=[wtforms.validators.DataRequired()])
    submit = wtforms.SubmitField('Искать')
