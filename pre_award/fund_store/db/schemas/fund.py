from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from data.models import Fund, FundingType


class FundSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Fund

    funding_type = fields.Enum(FundingType)
