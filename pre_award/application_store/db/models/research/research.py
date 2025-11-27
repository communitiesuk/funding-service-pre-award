from flask_sqlalchemy.model import DefaultMeta
from sqlalchemy import DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from pre_award.db import db

BaseModel: DefaultMeta = db.Model


class ResearchSurvey(BaseModel):
    __tablename__ = "research_survey"

    id = db.Column(db.Integer, primary_key=True)
    application_id = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey("applications.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )
    fund_id = db.Column("fund_id", db.String(), nullable=False)
    round_id = db.Column("round_id", db.String(), nullable=False)
    data = db.Column(db.JSON, nullable=True)
    date_submitted = db.Column("date_submitted", DateTime(), server_default=func.now())

    application = relationship("Applications", back_populates="research_surveys")

    def as_dict(self):
        return {
            "id": self.id,
            "application_id": self.application_id,
            "fund_id": self.fund_id,
            "round_id": self.round_id,
            "data": self.data,
            "date_submitted": self.date_submitted,
        }
