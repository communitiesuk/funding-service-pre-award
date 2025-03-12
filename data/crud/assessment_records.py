from typing import List, Sequence
from uuid import UUID

from sqlalchemy import select

from pre_award.assessment_store.db.models.assessment_record.assessment_records import AssessmentRecord
from pre_award.assessment_store.db.models.assessment_record.enums import Status
from pre_award.db import db


def get_assessments_by_round(round_id: UUID, statuses: List[Status] | None = None) -> Sequence[AssessmentRecord]:
    filters = [AssessmentRecord.round_id == str(round_id)]

    if statuses:
        filters.append(AssessmentRecord.workflow_status.in_(statuses))

    return db.session.scalars(select(AssessmentRecord).where(*filters)).all()
