from flask_wtf import FlaskForm
from wtforms import SelectMultipleField, TextAreaField
from wtforms.validators import InputRequired, length

from pre_award.config import Config


def build_request_changes_form(question_choices):
    class RequestChangesForm(FlaskForm):
        field_ids = SelectMultipleField(
            "Questions to change",
            choices=question_choices,
            validators=[
                InputRequired(message="Select which question(s) you are requesting changes to"),
            ],
        )

    for field_id, question, _ in question_choices:
        field_name = f"reason_{field_id}"
        text_area_field = TextAreaField(
            f"Reason for {question}",
            validators=[
                length(max=Config.TEXT_AREA_INPUT_MAX_CHARACTERS),
                InputRequired(message="Provide a reason for requesting changes to this application"),
            ],
        )

        setattr(RequestChangesForm, field_name, text_area_field)

    return RequestChangesForm
