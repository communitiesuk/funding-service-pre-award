from marshmallow import post_dump
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from pre_award.application_store.db.models import Eligibility
from pre_award.application_store.db.models.eligibility.eligibility_trail import EligibilityUpdate


class EligibilitySchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Eligibility
        exclude = ["key"]

    @post_dump
    def handle_nones(self, data, **kwargs):
        if data["date_submitted"] is None:
            data["date_submitted"] = "null"


class EligibilityUpdateSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = EligibilityUpdate
