import uuid
from enum import Enum
from typing import List

from flask_sqlalchemy.model import DefaultMeta
from sqlalchemy import JSON, Column
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.types import Boolean
from sqlalchemy.types import Enum as SQLAEnum

from db import db
from fund_store.db.models.round import Round

BaseModel: DefaultMeta = db.Model


class FundingType(Enum):
    COMPETITIVE = "COMPETITIVE"
    UNCOMPETED = "UNCOMPETED"
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
    rounds: Mapped[List["Round"]] = relationship("Round")
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
