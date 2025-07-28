from flask_wtf import FlaskForm
from wtforms import RadioField, SelectMultipleField, TextAreaField
from wtforms.validators import InputRequired, Regexp, length

from pre_award.config import Config


class TagAssociationForm(FlaskForm):
    tags = SelectMultipleField(
        "Tags to associate",
        validators=[
            InputRequired(message="Provide which tag(s) you are associating"),
        ],
    )


tag_value_field = TextAreaField(
    "value",
    validators=[
        InputRequired(message="Enter a tag name"),
        length(max=Config.TEXT_AREA_INPUT_MAX_CHARACTERS),
        Regexp(
            r"^[A-Za-z0-9_' -]+$", message="Tag name can only include letters, numbers, apostrophes, hyphens and spaces"
        ),
    ],
)


class NewTagForm(FlaskForm):
    value = tag_value_field

    type = RadioField(
        "type",
        validators=[InputRequired(message="Select a tag purpose")],
    )


class EditTagForm(FlaskForm):
    value = tag_value_field


class DeactivateTagForm(FlaskForm):
    pass


class ReactivateTagForm(FlaskForm):
    pass
