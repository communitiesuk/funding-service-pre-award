import uuid

from flask_sqlalchemy.model import DefaultMeta
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import UUID

from db import db

BaseModel: DefaultMeta = db.Model


class TagType(BaseModel):
    __tablename__ = "tag_types"
    id = Column(
        UUID(as_uuid=True),
        default=uuid.uuid4,
        primary_key=True,
    )
    purpose = Column(
        db.String(255),
        nullable=False,
        unique=True,
    )
    description = Column(
        db.String(255),
        nullable=False,
    )
