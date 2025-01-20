import uuid
from datetime import timedelta

from flask_sqlalchemy.model import DefaultMeta
from sqlalchemy import Column, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.types import Boolean

from db import db

BaseModel: DefaultMeta = db.Model


class MagicLink(BaseModel):
    id = Column(
        "id",
        UUID(as_uuid=True),
        default=uuid.uuid4,
        primary_key=True,
        nullable=False,
    )
    email = Column("email", db.String())
    token = Column("token", db.String(), index=True, unique=True)
    path = Column("path", db.String())
    used = Column("used", Boolean(), default=False)

    # having this business logic encapsulated here is nice because its reliable and guaranteed but also might not be where the programmer expects to look for it
    # this could either be set as a constant in config/ where you would expect to look or moved up to the services layer (or left alone!)
    expires_date = Column("expires_date", DateTime(), server_default=func.now() + timedelta(hours=1))

    proto_created_date = Column("proto_created_date", DateTime(), server_default=func.now())
    proto_updated_date = Column("proto_updated_date", DateTime(), server_default=func.now(), onupdate=func.now())
