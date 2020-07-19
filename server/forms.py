from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class InputDataForm(FlaskForm):
    dict_name = StringField('Dictionary name', validators=[DataRequired()])
    input_text = StringField('Input text', validators=[DataRequired()])
    submit = SubmitField('Add words to dictionray')
