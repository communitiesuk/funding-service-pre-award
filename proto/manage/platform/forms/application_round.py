from flask_babel import lazy_gettext as _l
from flask_wtf import FlaskForm
from govuk_frontend_wtf.wtforms_widgets import (
    GovSubmitInput,
)
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from wtforms.widgets.core import HiddenInput


class CreateRoundForm(FlaskForm):
    create_new_round = SubmitField(_l("Create a new application round"), widget=GovSubmitInput())


class MakeRoundLiveForm(FlaskForm):
    submit = SubmitField(_l("Make round live"), widget=GovSubmitInput())


class PreviewApplicationForm(FlaskForm):
    round_id = StringField(None, widget=HiddenInput(), validators=[DataRequired()])
    organisation_id = StringField(None, widget=HiddenInput(), validators=[DataRequired()])
    submit = SubmitField(None, widget=GovSubmitInput(), validators=[DataRequired()])

    def __init__(self, *args, submit_label: str | None = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.submit.label.text = submit_label
