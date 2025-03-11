from typing import List, Sequence
from uuid import UUID

from sqlalchemy import select

from pre_award.assessment_store.db.models.assessment_record.assessment_records import AssessmentRecord
from pre_award.assessment_store.db.models.assessment_record.enums import Status
from pre_award.db import db


def get_assessments_by_round(round_id: UUID, statuses: List[Status] | None = None) -> Sequence[AssessmentRecord]:
    if statuses is None:
        statuses = [
            Status.NOT_STARTED,
            Status.IN_PROGRESS,
            Status.SUBMITTED,
            Status.COMPLETED,
            Status.CHANGE_REQUESTED,
            Status.CHANGE_RECEIVED,
        ]

    return db.session.scalars(
        select(AssessmentRecord).where(
            AssessmentRecord.round_id == round_id,
            AssessmentRecord.workflow_status.in_(statuses),
        )
    ).all()
