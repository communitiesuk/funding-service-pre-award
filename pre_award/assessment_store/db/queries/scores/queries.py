"""Queries which are performed on the `scores` table.

Joins allowed.

"""

import uuid
from typing import Dict

from flask import current_app as app
from sqlalchemy import String, cast, select
from sqlalchemy.orm.exc import NoResultFound

from pre_award.assessment_store.db.models import AssessmentRecord
from pre_award.assessment_store.db.models.assessment_record.enums import Status as ApplicationStatus
from pre_award.assessment_store.db.models.score import AssessmentRound, Score, ScoringSystem
from pre_award.assessment_store.db.queries.assessment_records.queries import (
    check_all_change_requests_accepted,
    update_application_status,
)
from pre_award.assessment_store.db.queries.flags.queries import resolve_open_change_requests_for_sub_criteria
from pre_award.assessment_store.db.schemas import AssessmentRoundMetadata, ScoreMetadata, ScoringSystemMetadata
from pre_award.db import db


def get_scores_for_app_sub_crit(
    application_id: str,
    sub_criteria_id: str = None,
    score_history: bool = False,
) -> list[dict]:
    """get_scores_for_app_sub_crit executes a query on scores which returns the
    most recent score or all scores for the given application_id and
    sub_criteria_id.

    :param application_id: The stringified application UUID.
    :param sub_criteria_id: The stringified sub_criteria UUID.
    :param score_history: Boolean value that reurns all scores if true
    :return: dictionary.

    """

    if sub_criteria_id:
        stmt = (
            select(Score)
            .where(
                Score.application_id == application_id,
                Score.sub_criteria_id == sub_criteria_id,
            )
            .order_by(Score.date_created.desc())
        )
    else:
        stmt = (
            select(Score)
            .where(
                Score.application_id == application_id,
            )
            .order_by(Score.date_created.desc())
        )

    if not score_history:
        stmt = stmt.limit(1)

    score_rows = db.session.scalars(stmt)

    metadata_serialiser = ScoreMetadata()

    score_metadatas = [metadata_serialiser.dump(score_row) for score_row in score_rows]

    return score_metadatas


def create_score_for_app_sub_crit(
    score: int,
    justification: str,
    application_id: str,
    sub_criteria_id: str,
    user_id: str,
) -> Dict:
    """create_score_for_app_sub_crit executes a query on scores which creates a
    justified score for the given application_id and sub_criteria_id.

    :param application_id: The stringified application UUID.
    :param sub_criteria_id: The stringified sub_criteria UUID.
    :param score: The score integer.
    :param justification: The justification text.
    :param date_created: The date_created.
    :param user_id: The stringified user_id.
    :return: dictionary.

    """
    score = Score(
        score=score,
        justification=justification,
        application_id=application_id,
        sub_criteria_id=sub_criteria_id,
        user_id=user_id,
    )
    db.session.add(score)
    db.session.commit()

    metadata_serialiser = ScoreMetadata()
    score_metadata = metadata_serialiser.dump(score)

    return score_metadata


def get_sub_criteria_to_latest_score_map(application_id: str) -> dict:
    stmt = (
        select(Score.sub_criteria_id, Score.score)
        .select_from(Score)
        .join(
            AssessmentRecord,
            Score.application_id == AssessmentRecord.application_id,
        )
        .where(AssessmentRecord.application_id == application_id)
        .order_by(Score.date_created.desc())
    )

    result = db.session.execute(stmt).fetchall()

    sub_criteria_to_latest_score = {}
    for sid, score in result:
        if sid not in sub_criteria_to_latest_score:
            sub_criteria_to_latest_score[sid] = score
    return sub_criteria_to_latest_score


def get_scoring_system_for_round_id(round_id: str) -> dict:
    stmt = (
        select(ScoringSystem, AssessmentRound.round_id)
        .select_from(AssessmentRound)
        .join(ScoringSystem, AssessmentRound.scoring_system_id == ScoringSystem.id)
        .where(AssessmentRound.round_id == round_id)
    )

    try:
        result = db.session.execute(stmt).one()
        scoring_system_instance = result[0]

        metadata_serialiser = ScoringSystemMetadata()
        processed_scoring_system = metadata_serialiser.dump(scoring_system_instance)

    except NoResultFound:
        # Return a default scoring system of OneToFive
        stmt = select(ScoringSystem).where(ScoringSystem.scoring_system_name == "OneToFive")
        result = db.session.execute(stmt).one()
        scoring_system_instance = result[0]

        metadata_serialiser = ScoringSystemMetadata()
        processed_scoring_system = metadata_serialiser.dump(scoring_system_instance)
        app.logger.warning(
            "No scoring system found for round_id: %(round_id)s. Defaulting to OneToFive", dict(round_id=round_id)
        )
    return processed_scoring_system


def _insert_scoring_system(scoring_system_name: str, min_score: int, max_score: int) -> dict:
    scoring_system = ScoringSystem(
        id=uuid.uuid4(),
        scoring_system_name=scoring_system_name,
        minimum_score=min_score,
        maximum_score=max_score,
    )
    db.session.add(scoring_system)
    db.session.commit()

    metadata_serialiser = ScoringSystemMetadata()
    inserted_scoring_system = metadata_serialiser.dump(scoring_system)
    return inserted_scoring_system


def insert_scoring_system_for_round_id(round_id: str, scoring_system_id: str) -> dict:
    assessment_round = AssessmentRound(
        round_id=round_id,
        scoring_system_id=scoring_system_id,
    )
    db.session.add(assessment_round)
    db.session.commit()

    metadata_serialiser = AssessmentRoundMetadata()
    inserted_assessment_round = metadata_serialiser.dump(assessment_round)
    return inserted_assessment_round


def approve_sub_criteria(application_id, sub_criteria_id, user_id, message):
    # Temporary solution to "accept" a sub-criteria is to provide it a non-zero score
    create_score_for_app_sub_crit(
        score=1,
        justification=message,
        application_id=application_id,
        user_id=user_id,
        sub_criteria_id=sub_criteria_id,
    )

    resolve_open_change_requests_for_sub_criteria(
        application_id=application_id, sub_criteria_id=sub_criteria_id, user_id=user_id
    )

    if check_all_change_requests_accepted(application_id=application_id):
        update_application_status(application_id=application_id, status=ApplicationStatus.IN_PROGRESS)


def update_scoring_system_for_round_id(round_id: str, scoring_system_id: str) -> dict:
    """
    Update (or insert) the scoring system for a given round.
    Returns the serialized AssessmentRound record.
    """
    assessment_round = db.session.query(AssessmentRound).filter(AssessmentRound.round_id == round_id).one_or_none()

    if assessment_round is None:
        assessment_round = AssessmentRound(round_id=round_id, scoring_system_id=scoring_system_id)
        db.session.add(assessment_round)
    else:
        assessment_round.scoring_system_id = scoring_system_id

    db.session.commit()
    return AssessmentRoundMetadata().dump(assessment_round)


def lookup_scoring_system_id(name: str) -> str | None:
    """
    Directly look up a scoring system by name (case-insensitive).
    """
    system = (
        db.session.query(ScoringSystem)
        .filter(cast(ScoringSystem.scoring_system_name, String).ilike(name))
        .one_or_none()
    )
    return str(system.id) if system else None


def list_existing_scoring_systems() -> list[ScoringSystem]:
    """Return a list of existing scoring systems."""
    return db.session.query(ScoringSystem).all()


def get_scoring_info_by_round(round_id: str) -> ScoringSystem | None:
    assessment_round = db.session.query(AssessmentRound).filter(AssessmentRound.round_id == round_id).first()
    if assessment_round is None:
        return None
    else:
        scoring_system = (
            db.session.query(ScoringSystem).filter(ScoringSystem.id == assessment_round.scoring_system_id).first()
        )
        return scoring_system
