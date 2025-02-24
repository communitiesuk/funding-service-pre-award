from flask_babel import lazy_gettext as _l
from flask_wtf import FlaskForm
from govuk_frontend_wtf.wtforms_widgets import (
    GovDateInput,
    GovSubmitInput,
)
from wtforms import SubmitField
from wtforms.fields.datetime import DateField
from wtforms.fields.simple import StringField
from wtforms.validators import DataRequired
from wtforms.widgets.core import HiddenInput


class CreateReportingRoundForm(FlaskForm):
    reporting_period_starts = DateField(_l("Reporting period starts"), format="%d %m %Y", widget=GovDateInput())
    reporting_period_ends = DateField(_l("Reporting period ends"), format="%d %m %Y", widget=GovDateInput())
    submission_period_starts = DateField(_l("Submission period starts"), format="%d %m %Y", widget=GovDateInput())
    submission_period_ends = DateField(_l("Submission period ends"), format="%d %m %Y", widget=GovDateInput())

    submit = SubmitField(_l("Create reporting round"), widget=GovSubmitInput())


class PublishReportingRoundForm(FlaskForm):
    submit = SubmitField(_l("Publish reporting round"), widget=GovSubmitInput())


class PreviewReportForm(FlaskForm):
    round_id = StringField(None, widget=HiddenInput(), validators=[DataRequired()])
    organisation_id = StringField(None, widget=HiddenInput(), validators=[DataRequired()])
    submit = SubmitField(None, widget=GovSubmitInput(), validators=[DataRequired()])

    def __init__(self, *args, submit_label: str | None = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.submit.label.text = submit_label
