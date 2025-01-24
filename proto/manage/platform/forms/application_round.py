from flask_babel import lazy_gettext as _l
from flask_wtf import FlaskForm
from govuk_frontend_wtf.wtforms_widgets import (
    GovSubmitInput,
    GovTextInput,
)
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Optional
from wtforms.widgets.core import HiddenInput


class CreateRoundForm(FlaskForm):
    code = StringField(
        _l("Round code"), widget=GovTextInput(), validators=[DataRequired(message=_l("Enter a grant code"))]
    )

    title = StringField(
        _l("Round title"), widget=GovTextInput(), validators=[DataRequired(message=_l("Enter a title for the grant"))]
    )
    title_cy = StringField(_l("Round title (Welsh)"), widget=GovTextInput(), validators=[Optional()])

    # fixme: re-enable these, govuk-frontend-wtf datefield doesn't seem to be working - must be me doing something bad
    # proto_start_date = DateField(
    #     _l("When will applications open for the round?"),
    #     widget=GovDateInput(),
    #     validators=[DataRequired(message=_l("Enter a start date for the round"))],
    # )
    # proto_end_date = DateField(
    #     _l("When will applications close for the round?"),
    #     widget=GovDateInput(),  # FIXME: govuk-frontend-wtf doesn't have datetime support, ohno
    #     validators=[DataRequired(message=_l("Enter an end date for the round"))],
    # )
    submit = SubmitField(_l("Create round"), widget=GovSubmitInput())


class MakeRoundLiveForm(FlaskForm):
    submit = SubmitField(_l("Make round live"), widget=GovSubmitInput())


class PreviewApplicationForm(FlaskForm):
    round_id = StringField(None, widget=HiddenInput(), validators=[DataRequired()])
    account_id = StringField(None, widget=HiddenInput(), validators=[DataRequired()])
    submit = SubmitField(None, widget=GovSubmitInput(), validators=[DataRequired()])

    def __init__(self, *args, submit_label: str | None = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.submit.label.text = submit_label
