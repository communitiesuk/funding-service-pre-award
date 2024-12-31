from flask_wtf import FlaskForm
from wtforms import SelectMultipleField, TextAreaField
from wtforms.validators import InputRequired, length

from config import Config


class RequestChangesForm(FlaskForm):
    justification = TextAreaField(
        "Reason for request changes",
        validators=[
            length(max=Config.TEXT_AREA_INPUT_MAX_CHARACTERS),
            InputRequired(message="Provide a reason for requesting changes to this application"),
        ],
    )
    field_ids = SelectMultipleField(
        "Questions to change",
        choices=None,
        validators=[
            InputRequired(message="Select which question(s) you are requesting changes to"),
        ],
    )

    def __init__(self, question_choices=None):
        super().__init__()

        self.field_ids.choices = question_choices
