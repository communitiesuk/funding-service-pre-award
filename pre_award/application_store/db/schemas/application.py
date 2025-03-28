from marshmallow import post_dump
from marshmallow.fields import DateTime, Enum, Method
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from marshmallow_sqlalchemy.fields import Nested

from pre_award.application_store.db.models import Applications
from pre_award.application_store.db.models.application.enums import Language, Status
from pre_award.application_store.db.schemas.form import FormsRunnerSchema
from pre_award.application_store.external_services import get_round_name


class ApplicationSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Applications
        exclude = ["key"]

    @post_dump
    def handle_nones(self, data, **kwargs):
        if data["last_edited"] is None:
            data["last_edited"] = data["started_at"]
        if data["date_submitted"] is None:
            data["date_submitted"] = "null"
        if data["language"] is None:
            data["language"] = "en"
        return data

    def get_round_name(self, obj):
        # TODO: is this actually being used at all?
        # If we're not using this, it would be good to remove it or exclude it.
        # i.e exclude = ["round_name"], as we don't want it to run during each
        # serialization - it makes a GET request per application.  The request
        # is LRU cached for now, incase this is actually used.
        return get_round_name(obj.fund_id, obj.round_id)

    language = Enum(Language, default=Language.en)
    project_name = auto_field()
    started_at = DateTime(format="iso")
    status = Enum(Status)
    last_edited = DateTime(format="iso")
    date_submitted = DateTime(format="%Y-%m-%dT%H:%M:%S.%f")
    round_name = Method("get_round_name")
    forms = Nested(FormsRunnerSchema, many=True, allow_none=True)
