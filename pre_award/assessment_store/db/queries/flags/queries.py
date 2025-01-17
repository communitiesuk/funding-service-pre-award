from typing import Dict

from sqlalchemy import select

from assessment_store.db.models.flags.assessment_flag import AssessmentFlag
from assessment_store.db.models.flags.flag_update import FlagStatus, FlagUpdate
from db import db


def get_flags_for_application(application_id):
    stmt = select(AssessmentFlag).where(AssessmentFlag.application_id == application_id)
    results = db.session.scalars(stmt).all()
    return results


def get_flag_by_id(flag_id):
    stmt = select(AssessmentFlag).where(AssessmentFlag.id == flag_id)
    results = db.session.scalars(stmt).all()
    return results


def add_flag_for_application(
    justification: str,
    sections_to_flag: str,
    application_id: str,
    user_id: str,
    status: FlagStatus,
    allocation: str,
    field_ids: list[str] = None,
    is_change_request: bool = False,
) -> Dict:
    flag_update = FlagUpdate(
        justification=justification,
        user_id=user_id,
        status=status,
        allocation=allocation,
    )
    assessment_flag = AssessmentFlag(
        application_id=application_id,
        sections_to_flag=sections_to_flag,
        latest_allocation=allocation,
        latest_status=status,
        updates=[flag_update],
        field_ids=field_ids,
        is_change_request=is_change_request,
    )
    db.session.add(assessment_flag)
    db.session.commit()
    return assessment_flag


def add_update_to_assessment_flag(
    justification: str,
    user_id: str,
    status: FlagStatus,
    allocation: str,
    assessment_flag_id: str,
) -> Dict:
    stmt = select(AssessmentFlag).where(AssessmentFlag.id == assessment_flag_id)

    assessment_flag = db.session.scalars(stmt).one()

    flag_update = FlagUpdate(
        justification=justification,
        user_id=user_id,
        status=status,
        allocation=allocation,
        assessment_flag_id=assessment_flag_id,
    )
    assessment_flag.updates.append(flag_update)
    assessment_flag.latest_allocation = allocation
    assessment_flag.latest_status = status

    db.session.add(assessment_flag)
    db.session.commit()
    return assessment_flag
