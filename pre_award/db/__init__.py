import enum

import sqlalchemy
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import JSON, MetaData

convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}


class FundingType(enum.Enum):
    COMPETITIVE = "COMPETITIVE"
    UNCOMPETED = "UNCOMPETED"
    EOI = "EOI"


metadata = MetaData(naming_convention=convention)

db = SQLAlchemy(metadata=metadata)

db.Model.registry.update_type_annotation_map(
    {dict[str, str]: JSON(none_as_null=True), FundingType: sqlalchemy.Enum(FundingType, native_enum=False)}
)

migrate = Migrate()
