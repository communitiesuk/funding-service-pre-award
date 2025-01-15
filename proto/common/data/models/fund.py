import uuid
from enum import Enum

from flask_sqlalchemy.model import DefaultMeta
from pydantic import UUID4, Field
from pydantic import BaseModel as PydanticBaseModel
from sqlalchemy import JSON, Column, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.types import Boolean
from sqlalchemy.types import Enum as SQLAEnum

from db import db

# if TYPE_CHECKING:
# from proto.common.data.models.round import Round
# else:
# Round = "Round"

# from proto.common.data.models.round import Round
BaseModel: DefaultMeta = db.Model


# ideally I'd like id internal int, external_id optionally human readbale
# PROTO: will probably namespace the SQL Alchemy as the domain object and the pydantic representation Schema
class ProtoGrantSchema(PydanticBaseModel):
    external_id: UUID4 = Field(alias="id")
    short_code: str = Field(alias="short_name")
    name: str = Field(alias="proto_name")
    name_cy: str = Field(alias="proto_name_cy")

    class Config:
        orm_mode = True


class FundingType(Enum):
    COMPETITIVE = "COMPETITIVE"
    UNCOMPETED = "UNCOMPETED"
    # PROTO: removed from options
    EOI = "EOI"


class Fund(BaseModel):
    id = Column(
        "id",
        UUID(as_uuid=True),
        default=uuid.uuid4,
        primary_key=True,
        nullable=False,
    )
    name_json = Column("name_json", JSON(none_as_null=True), nullable=False, unique=False)
    title_json = Column("title_json", JSON(none_as_null=True), nullable=False, unique=False)
    short_name = Column("short_name", db.String(), nullable=False, unique=True)
    description_json = Column("description_json", JSON(none_as_null=True), nullable=False, unique=False)
    # rounds: Mapped[List[Round]] = relationship("Round")
    welsh_available = Column("welsh_available", Boolean, default=False, nullable=False)
    owner_organisation_name = Column("owner_organisation_name", db.String(), nullable=False, unique=False)
    owner_organisation_shortname = Column("owner_organisation_shortname", db.String(), nullable=False, unique=False)
    owner_organisation_logo_uri = Column("owner_organisation_logo_uri", db.Text(), nullable=True, unique=False)
    funding_type = Column(
        "funding_type",
        SQLAEnum(FundingType, name="fundingtype"),
        nullable=False,
        unique=False,
    )
    ggis_scheme_reference_number = Column("ggis_scheme_reference_number", db.String(255), nullable=True, unique=False)

    # For the (assumed limited) fields which will be user provided and translatable, default to field name in english and field name _language-code otherwise
    # do NOT store text in JSON for translation reasons, for now - this complexity hasn't proven valuable to me yet (used generically by macros/ utils for example)
    proto_name = Column("proto_name", db.String(), nullable=True, unique=False)
    proto_name_cy = Column("proto_name_cy", db.String(), nullable=True, unique=False)

    # likely a decision - if we're not using the org info for grants anywhere - don't store it
    # if we ARE using it it should be stored in a separate `organisations` table that could be kept up to date with the gov uk Collections API
    # that could also be shared for managing things like default access to grants in assess but again that should be grounded in needing to do it

    proto_created_date = Column("proto_created_date", DateTime(), server_default=func.now())
    proto_updated_date = Column("proto_updated_date", DateTime(), server_default=func.now(), onupdate=func.now())

    proto_prospectus_link = Column("proto_prospectus_link", db.String(), nullable=True)

    proto_apply_action_description = Column("proto_apply_action_description", db.String(), nullable=True)
