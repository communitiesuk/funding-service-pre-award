from typing import Sequence

from pre_award.application_store.db.models.application.applications import Applications
from pre_award.application_store.db.models.application.enums import Status as ApplicationStatus
from pre_award.assessment_store.db.models.assessment_record.assessment_records import AssessmentRecord
from pre_award.assessment_store.db.models.assessment_record.enums import Status as AssessmentStatus


def get_applications_stats(applications: Sequence[Applications]) -> dict[str, int]:
    applications_stats = {
        "completed": 0,
        "not_started": 0,
        "in_progress": 0,
        "submitted": 0,
    }

    for application in applications:
        if application.status == ApplicationStatus.NOT_STARTED:
            applications_stats["not_started"] += 1
        elif application.status == ApplicationStatus.IN_PROGRESS:
            applications_stats["in_progress"] += 1
        elif application.status == ApplicationStatus.COMPLETED:
            applications_stats["completed"] += 1
        elif application.status == ApplicationStatus.SUBMITTED:
            applications_stats["submitted"] += 1

    return applications_stats


def get_assessments_stats(assessments: Sequence[AssessmentRecord]) -> dict[str, int]:
    assessments_stats = {
        "completed": 0,
        "not_started": 0,
        "in_progress": 0,
        "withdrawn": 0,
        "comments": 0,
        "tags": 0,
        "flags": 0,
        "change_requests": 0,
    }

    for assessment in assessments:
        if assessment.workflow_status == AssessmentStatus.COMPLETED:
            assessments_stats["completed"] += 1
        if assessment.workflow_status == AssessmentStatus.IN_PROGRESS:
            assessments_stats["in_progress"] += 1
        if assessment.workflow_status == AssessmentStatus.NOT_STARTED:
            assessments_stats["not_started"] += 1
        if assessment.is_withdrawn:
            assessments_stats["withdrawn"] += 1

        assessments_stats["comments"] += len(assessment.comments)
        assessments_stats["tags"] += len(assessment.tag_associations)
        assessments_stats["flags"] += len(assessment.flags) - len(assessment.change_requests)
        assessments_stats["change_requests"] += len(assessment.change_requests)

    return assessments_stats


def get_assessment_averages(
    assessments: Sequence[AssessmentRecord], assessment_stats: dict[str, int]
) -> dict[str, float]:
    assessment_averages = {
        "application_success_rate": 0.00,
        "comments_per_assessment": 0.00,
        "tags_per_assessment": 0.00,
        "flags_per_assessment": 0.00,
        "change_requests_per_assessment": 0.00,
    }

    total = len(assessments)
    if total == 0:
        return assessment_averages

    assessment_averages["application_success_rate"] = round(assessment_stats["completed"] * 100 / total, 2)
    assessment_averages["comments_per_assessment"] = round(assessment_stats["comments"] / total, 2)
    assessment_averages["tags_per_assessment"] = round(assessment_stats["tags"] / total, 2)
    assessment_averages["flags_per_assessment"] = round(assessment_stats["flags"] / total, 2)
    assessment_averages["change_requests_per_assessment"] = round(assessment_stats["change_requests"] / total, 2)

    return assessment_averages
