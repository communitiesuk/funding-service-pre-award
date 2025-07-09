from typing import Dict

from sqlalchemy import and_, desc, func, select
from sqlalchemy.orm import contains_eager

from pre_award.assessment_store.db.models.flags.assessment_flag import AssessmentFlag
from pre_award.assessment_store.db.models.flags.flag_update import FlagStatus, FlagUpdate
from pre_award.db import db


def get_flags_for_application(application_id):
    stmt = select(AssessmentFlag).where(AssessmentFlag.application_id == application_id)
    results = db.session.scalars(stmt).all()
    return results


def get_change_requests_for_application(application_id, only_raised=False, sort_by_update=False, sort_by_raised=False):
    """
    Retrieves change requests for a specific application.

    Args:
        application_id (UUID or str): The unique identifier of the application.
        only_raised (bool, optional): If True, filters the results to include only change requests
                                      with a status of 'RAISED'
        sort_by_update (bool, optional): If True, sorts the change requests in descending order
                                          based on the latest update date.
        sort_by_raised (bool, optional): If True, sorts the change requests in descending order
                                          based on when they were raised (created).

    Returns:
        list: A list of AssessmentFlag representing the change requests for the application.
    """
    stmt = select(AssessmentFlag).where(
        AssessmentFlag.application_id == application_id, AssessmentFlag.is_change_request.is_(True)
    )
    if only_raised:
        stmt = stmt.where(AssessmentFlag.latest_status == FlagStatus.RAISED)
    if sort_by_update:
        # Order change requests according to their latest update
        stmt = stmt.join(FlagUpdate).group_by(AssessmentFlag.id).order_by(desc(func.max(FlagUpdate.date_created)))
    elif sort_by_raised:
        stmt = (
            stmt.join(
                FlagUpdate,
                and_(FlagUpdate.assessment_flag_id == AssessmentFlag.id, FlagUpdate.status == FlagStatus.RAISED),
            )
            .group_by(AssessmentFlag.id)
            .order_by(desc(func.max(FlagUpdate.date_created)))
        )

    results = db.session.scalars(stmt).all()
    return results


def is_first_change_request_for_date(application_id, date):
    change_requests = get_change_requests_for_application(
        application_id=application_id, only_raised=True, sort_by_update=True
    )
    return not change_requests or all(
        date > flag_update.date_created.date() for flag_update in change_requests[0].updates
    )


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


def resolve_open_change_requests_for_sub_criteria(
    application_id, sub_criteria_id, user_id, justification="Sub-criteria was accepted and scored"
):
    """
    Resolves open change requests for a given sub-criteria within an application.

    This function identifies all change requests (AssessmentFlags) that:
    - Belong to the specified application,
    - Are marked as change requests (`is_change_request=True`),
    - Have a latest status of `RESOLVED` (indicating the applicant has responded),
    - Include the specified sub-criteria in their flagged sections.

    For each matching change request, the function:
    - Creates a new `FlagUpdate` with the status set to `STOPPED`, indicating that the assessor has accepted and scored
    the response,
    - Updates the `latest_status` of the flag to `STOPPED`,
    - Commits the changes to the database.

    Args:
        application_id (int): The ID of the application containing the change requests.
        sub_criteria_id (str): The identifier of the sub-criteria being resolved.
        user_id (int): The ID of the user (assessor) performing the resolution.
        justification (str, optional): A justification message for stopping the flag. Defaults to
        "Sub-criteria was accepted and scored".

    Returns:
        List[AssessmentFlag]: A list of the updated change request flags.

    Note:
        The `RESOLVED` status is used when the applicant has responded to a change request.
        The `STOPPED` status is used when the assessor has accepted and scored the response.
    """

    stmt = select(AssessmentFlag).where(
        AssessmentFlag.application_id == application_id,
        AssessmentFlag.is_change_request.is_(True),
        AssessmentFlag.latest_status == FlagStatus.RESOLVED,
        AssessmentFlag.sections_to_flag.contains([sub_criteria_id]),
    )
    open_change_requests = db.session.scalars(stmt).all()
    for open_change_request in open_change_requests:
        flag_update = FlagUpdate(
            justification=justification,
            user_id=user_id,
            status=FlagStatus.STOPPED,
            allocation=None,
            assessment_flag_id=open_change_request.id,
        )
        open_change_request.updates.append(flag_update)
        open_change_request.latest_status = FlagStatus.STOPPED
        db.session.add(open_change_request)

    db.session.commit()

    return open_change_requests


def prepare_change_requests_metadata(application_id: str) -> dict[str, list] | None:
    assessment_flags = (
        db.session.query(AssessmentFlag)
        .join(FlagUpdate)
        .filter(
            AssessmentFlag.is_change_request.is_(True),
            AssessmentFlag.application_id == application_id,
            AssessmentFlag.latest_status == FlagStatus.RAISED,
        )
        .options(contains_eager(AssessmentFlag.updates))
        .filter(FlagUpdate.status == FlagStatus.RAISED)
        .all()
    )

    if not assessment_flags:
        return None

    assessor_change_requests: dict[str, list] = {}
    for change_request in assessment_flags:
        for field_id in change_request.field_ids:
            if field_id not in assessor_change_requests:
                assessor_change_requests[field_id] = []

            assessor_change_requests[field_id].extend([update.justification for update in change_request.updates])

    return assessor_change_requests
