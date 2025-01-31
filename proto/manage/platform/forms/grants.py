from flask_babel import lazy_gettext as _l
from flask_wtf import FlaskForm
from govuk_frontend_wtf.wtforms_widgets import GovRadioInput, GovSubmitInput, GovTextArea, GovTextInput
from markupsafe import Markup
from wtforms import RadioField, StringField, SubmitField
from wtforms.validators import URL, DataRequired

from proto.common.data.models.fund import FundingType


class CreateGrantForm(FlaskForm):
    name = StringField(
        _l("Grant name"), widget=GovTextInput(), validators=[DataRequired(message=_l("Enter a name for the grant"))]
    )

    proto_apply_action_description = StringField(
        _l("What will this grant be used for?"),
        widget=GovTextArea(),
        validators=[DataRequired(message=_l("Enter what this grant will be used for"))],
        description=_l("Start or continue an application to..."),
    )

    funding_type = RadioField(
        _l("What application process does this grant use?"),
        widget=GovRadioInput(),
        choices=[(FundingType.COMPETITIVE.value, "Competed"), (FundingType.UNCOMPETED.value, "Un-competed")],
        validators=[DataRequired(message=_l("Select an application process for the grant"))],
    )

    submit = SubmitField(_l("Set up grant"), widget=GovSubmitInput())


class MakeGrantLiveForm(FlaskForm):
    submit = SubmitField(_l("Make grant live"), widget=GovSubmitInput())


class EditGrantProspectusLink(FlaskForm):
    prospectus_link = StringField(
        "Prospectus link",
        description=Markup("""
        <p class="govuk-hint">
        The prospectus should explain:
        <ul class="govuk-list govuk-list--bullet govuk-hint">
        <li>who can apply</li>
        <li>what funding is available</li>
        <li>the goals the grant is trying to achieve</li>
        <li>how funding will be awarded</li>
        <li>the monitoring and evaluation requirements for grant recipients</li>
        </ul>
        </p>
        """),
        widget=GovTextInput(),
        validators=[URL(message=_l("Enter a valid grant prospectus link"))],
    )
    submit = SubmitField(_l("Save"), widget=GovSubmitInput())
