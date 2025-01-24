import uuid
from enum import Enum

from flask_sqlalchemy.model import DefaultMeta
from sqlalchemy import Column, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.types import Enum as SQLAEnum

from pre_award.db import db

BaseModel: DefaultMeta = db.Model


class EventType(Enum):
    APPLICATION_DEADLINE_REMINDER = "APPLICATION_DEADLINE_REMINDER"
    SEND_INCOMPLETE_APPLICATIONS = "SEND_INCOMPLETE_APPLICATIONS"
    ACCOUNT_IMPORT = "ACCOUNT_IMPORT"


class Event(BaseModel):
    id = Column(
        "id",
        UUID(as_uuid=True),
        default=uuid.uuid4,
        primary_key=True,
        nullable=False,
    )
    round_id = Column(
        "round_id",
        UUID(as_uuid=True),
        ForeignKey("round.id"),
        nullable=True,
    )
    type = Column("type", SQLAEnum(EventType, name="event_type"), nullable=False, unique=False)
    activation_date = Column("activation_date", DateTime(), nullable=False)
    processed = Column("processed", DateTime(), nullable=True)
