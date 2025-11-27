"""The module containing all code related to the `comments` table within the
Postgres db."""

import uuid

from sqlalchemy import ForeignKey, func
from sqlalchemy.dialects.postgresql import ENUM, UUID
from sqlalchemy.orm import relationship

from pre_award.assessment_store.db.models.comment.enums import CommentType
from pre_award.db import db


class Comment(db.Model):
    """Comment The sqlalchemy-flask model class used to define the `Comment` table
    in the Postgres database."""

    __tablename__ = "comments"

    id = db.Column("comment_id", UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)

    application_id = db.Column(
        "application_id",
        UUID,
        ForeignKey("assessment_records.application_id", ondelete="CASCADE"),
    )

    user_id = db.Column("user_id", db.String(), nullable=False)

    date_created = db.Column("date_created", db.DateTime(), server_default=func.now())

    sub_criteria_id = db.Column("sub_criteria_id", db.String(), nullable=True)

    comment_type = db.Column("comment_type", ENUM(CommentType), nullable=True)

    theme_id = db.Column("theme_id", db.String(), nullable=True)

    updates = relationship("CommentsUpdate", passive_deletes=True, lazy="selectin")
    assessment_record = relationship("AssessmentRecord", back_populates="comments")
