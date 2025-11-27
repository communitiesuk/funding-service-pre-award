import uuid

from flask_sqlalchemy.model import DefaultMeta
from sqlalchemy import DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy_json import NestedMutableJson

from pre_award.application_store.db.models.application.applications import Applications
from pre_award.application_store.db.models.application.enums import Status
from pre_award.db import db

BaseModel: DefaultMeta = db.Model


class Feedback(BaseModel):
    id = db.Column(
        "id",
        UUID(as_uuid=True),
        default=uuid.uuid4,
        primary_key=True,
        nullable=False,
    )
    application_id = db.Column("application_id", db.ForeignKey(Applications.id, ondelete="CASCADE"), nullable=False)
    fund_id = db.Column("fund_id", db.String(), nullable=False)
    round_id = db.Column("round_id", db.String(), nullable=False)
    section_id = db.Column("section_id", db.String(), nullable=False)
    feedback_json = db.Column("feedback_json", NestedMutableJson, nullable=False)
    status = db.Column("status", db.Enum(Status), default="NOT_STARTED", nullable=False)
    date_submitted = db.Column("date_submitted", DateTime(), server_default=func.now())

    __table_args__ = (db.UniqueConstraint("application_id", "section_id"),)

    application = relationship(
        "Applications",
        back_populates="feedbacks",
    )

    def as_dict(self):
        date_submitted = self.date_submitted.isoformat() if self.date_submitted else "null"
        return {
            "id": str(self.id),
            "application_id": self.application_id,
            "fund_id": self.fund_id,
            "round_id": self.round_id,
            "section_id": self.section_id,
            "feedback": self.feedback_json,
            "status": self.status.name,
            "date_submitted": date_submitted,
        }
