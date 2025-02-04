from flask_wtf import FlaskForm
from wtforms import TextAreaField
from wtforms.validators import InputRequired, length

from pre_award.config import Config


class ChangeRequestForm(FlaskForm):
    comment = TextAreaField(
        "Change Request Comment",
        validators=[
            length(max=Config.TEXT_AREA_INPUT_MAX_CHARACTERS),
            InputRequired(),
        ],
    )
