"""The module containing all code related to the `scores` table within the
Postgres db."""

import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import ENUM, UUID
from sqlalchemy.sql import func

from pre_award.assessment_store.db.models.score.enums import ScoringSystem
from pre_award.db import db


class Score(db.Model):
    """Score The sqlalchemy-flask model class used to define the `scores` table in
    the Postgres database."""

    __tablename__ = "scores"

    id = db.Column("score_id", UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)

    score = db.Column("score", db.Integer(), nullable=False)

    justification = db.Column("justification", db.Text(), nullable=False)

    application_id = db.Column(
        "application_id",
        UUID,
        ForeignKey("assessment_records.application_id", ondelete="CASCADE"),
    )
    assessment_record = db.relationship("AssessmentRecord", back_populates="scores")

    date_created = db.Column("date_created", db.DateTime(), server_default=func.now())

    sub_criteria_id = db.Column("sub_criteria_id", db.String(), nullable=False)

    user_id = db.Column("user_id", db.String(), nullable=False)


class AssessmentRound(db.Model):
    """The sqlalchemy-flask model class used to define the `assessment round`
    table in the Postgres database."""

    __tablename__ = "assessment_round"

    round_id = db.Column(
        "round_id",
        UUID(as_uuid=True),
        default=uuid.uuid4,
        primary_key=True,
        nullable=False,
    )

    # link to the scoring system table
    scoring_system_id = db.Column(
        "scoring_system_id",
        UUID(as_uuid=True),
        ForeignKey("scoring_system.id"),
        nullable=True,
    )


class ScoringSystem(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True)

    scoring_system_name = db.Column(ENUM(ScoringSystem), nullable=False)

    minimum_score = db.Column("minimum_score", db.Integer(), nullable=False)

    maximum_score = db.Column("maximum_score", db.Integer(), nullable=False)
