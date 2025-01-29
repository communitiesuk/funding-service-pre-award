from flask_babel import lazy_gettext as _l
from flask_wtf import FlaskForm
from govuk_frontend_wtf.wtforms_widgets import GovRadioInput, GovSubmitInput, GovTextArea, GovTextInput
from wtforms import RadioField, StringField, SubmitField
from wtforms.validators import DataRequired

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
