from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field

from pre_award.account_store.db.models.role import Role


class RoleSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Role
        include_fk = True

    role = auto_field()
