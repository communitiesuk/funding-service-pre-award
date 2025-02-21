from flask_wtf import FlaskForm
from govuk_frontend_wtf.wtforms_widgets import GovRadioInput, GovSubmitInput, GovTextInput
from wtforms.fields.choices import RadioField
from wtforms.fields.simple import StringField, SubmitField
from wtforms.validators import DataRequired, InputRequired

from proto.common.data.models import ProtoApplication


class SetupNewRecipientFlowForm(FlaskForm):
    flow = RadioField(
        "How would you like to setup your new grant recipient?",
        widget=GovRadioInput(),
        choices=[("application", "From an application"), ("manual", "From scratch")],
        validators=[DataRequired()],
    )

    submit = SubmitField("Continue", widget=GovSubmitInput())


class SetupNewRecipientFromApplicationForm(FlaskForm):
    application = RadioField(
        "Select the organisation to setup as a grant recipient",
        widget=GovRadioInput(),
        choices=None,
        validators=[DataRequired()],
    )

    submit = SubmitField("Continue", widget=GovSubmitInput())

    def __init__(self, applications: list[ProtoApplication], *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.application.choices = [
            (application.external_id, f"Bolton Council (Application reference: {application.code})")
            for application in applications
        ]


class UpdateRecipientFundingAllocationForm(FlaskForm):
    funding_allocated = StringField(
        "How much funding would you like to allocate?",
        widget=GovTextInput(),
        validators=[InputRequired()],
    )

    submit = SubmitField("Save", widget=GovSubmitInput())
