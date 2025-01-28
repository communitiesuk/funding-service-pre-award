from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field

from data.models import Round


class RoundSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Round
        exclude = ["eoi_decision_schema"]

    fund_id = auto_field()
