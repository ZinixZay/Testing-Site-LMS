import flask_wtf
import wtforms
from core.database_functions import get_all_variants
from main import current_user


class VariantsForm(flask_wtf.FlaskForm):
    choices = get_all_variants(current_user)
    variant = wtforms.SelectField('Choose your variant: ', choices=choices)
