from flask_wtf import FlaskForm
from wtforms import SelectMultipleField, TextAreaField
from wtforms.validators import InputRequired, Length

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

    form = RequestChangesForm()

    selected_field_ids = form.field_ids.data or []

    for field_id, question, _ in question_choices:
        field_name = f"reason_{field_id}"

        validators = [Length(max=Config.TEXT_AREA_INPUT_MAX_CHARACTERS)]
        if field_id in selected_field_ids:
            validators.append(InputRequired(message="Provide a reason for requesting changes to this application"))
        text_area_field = TextAreaField(
            f"Reason for {question}",
            validators=validators,
        )
        setattr(RequestChangesForm, field_name, text_area_field)

    return RequestChangesForm
