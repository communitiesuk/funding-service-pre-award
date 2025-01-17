from uuid import uuid4

from flask_sqlalchemy.model import DefaultMeta
from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from db import db

BaseModel: DefaultMeta = db.Model


class QaComplete(BaseModel):
    __tablename__ = "qa_complete"

    id = Column("id", UUID(as_uuid=True), default=uuid4, primary_key=True)
    application_id = Column(
        "application_id",
        UUID(as_uuid=True),
        ForeignKey("assessment_records.application_id"),
    )
    user_id = Column("user_id", String, nullable=False)
    date_created = Column("date_created", db.DateTime(), server_default=func.now())
