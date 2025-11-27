import uuid

from flask_sqlalchemy.model import DefaultMeta
from sqlalchemy import Column, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy_json import NestedMutableJson

from pre_award.application_store.db.models.application.applications import Applications
from pre_award.db import db

BaseModel: DefaultMeta = db.Model


class Eligibility(BaseModel):
    id = Column(
        "id",
        UUID(as_uuid=True),
        default=uuid.uuid4,
        primary_key=True,
        nullable=False,
    )
    form_id = Column("form_id", db.String(), nullable=False)
    answers = Column("answers", NestedMutableJson)
    eligible = Column("eligible", db.Boolean(), nullable=True)

    # Add ondelete="CASCADE"
    application_id = db.Column("application_id", db.ForeignKey(Applications.id, ondelete="CASCADE"), nullable=False)
    application = db.relationship("Applications", back_populates="eligibility")

    date_submitted = db.Column("date_submitted", DateTime())

    def as_dict(self):
        date_submitted = self.date_submitted.isoformat() if self.date_submitted else "null"

        return {
            "id": str(self.id),
            "form_id": self.form_id,
            "answers": self.answers,
            "eligible": self.eligible,
            "application_id": self.application_id,
            "date_submitted": date_submitted,
        }
