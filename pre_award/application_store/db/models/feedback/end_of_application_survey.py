from flask_sqlalchemy.model import DefaultMeta
from sqlalchemy import DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from pre_award.db import db

BaseModel: DefaultMeta = db.Model


class EndOfApplicationSurveyFeedback(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    application_id = db.Column(UUID(as_uuid=True), db.ForeignKey("applications.id"), nullable=False)
    fund_id = db.Column("fund_id", db.String(), nullable=False)
    round_id = db.Column("round_id", db.String(), nullable=False)
    page_number = db.Column(db.Integer, nullable=False)
    data = db.Column(db.JSON, nullable=True)
    date_submitted = db.Column("date_submitted", DateTime(), server_default=func.now())

    __table_args__ = (db.UniqueConstraint("application_id", "page_number", name="_unique_application_page"),)

    @property
    def get_section_comment_rating(self) -> tuple[str, str, str]:
        section = ""
        comment = ""
        rating = ""
        for key in self.data.keys():
            if key == "more_detail":
                comment = self.data[key]
            elif key != "csrf_token":
                section = key
                rating = self.data[key]

        return section, comment, rating

    def as_dict(self):
        return {
            "id": self.id,
            "application_id": self.application_id,
            "fund_id": self.fund_id,
            "round_id": self.round_id,
            "page_number": self.page_number,
            "data": self.data,
            "date_submitted": self.date_submitted,
        }
