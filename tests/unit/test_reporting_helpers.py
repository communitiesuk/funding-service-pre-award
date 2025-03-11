from typing import Sequence
from unittest.mock import MagicMock

from pre_award.application_store.db.models.application.applications import Applications
from pre_award.application_store.db.models.application.enums import Status as ApplicationStatus
from pre_award.assessment_store.db.models.assessment_record.assessment_records import AssessmentRecord
from pre_award.assessment_store.db.models.assessment_record.enums import Status as AssessmentStatus
from reporting.helpers import get_applications_stats, get_assessment_averages, get_assessments_stats


def test_get_applications_stats_for_all_statuses() -> None:
    mock_application_not_stared = MagicMock()
    mock_application_not_stared.status = ApplicationStatus.NOT_STARTED
    mock_application_in_progress = MagicMock()
    mock_application_in_progress.status = ApplicationStatus.IN_PROGRESS
    mock_application_completed = MagicMock()
    mock_application_completed.status = ApplicationStatus.COMPLETED
    mock_application_submitted = MagicMock()
    mock_application_submitted.status = ApplicationStatus.SUBMITTED

    applications = [
        mock_application_not_stared,
        mock_application_in_progress,
        mock_application_completed,
        mock_application_submitted,
    ]

    expected = {
        "completed": 1,
        "not_started": 1,
        "in_progress": 1,
        "submitted": 1,
    }

    assert get_applications_stats(applications) == expected


def test_get_applications_stats_with_multiple_applications_same_status() -> None:
    mock_application = MagicMock()
    mock_application.status = ApplicationStatus.COMPLETED

    applications = [mock_application, mock_application, mock_application]

    expected = {
        "completed": 3,
        "not_started": 0,
        "in_progress": 0,
        "submitted": 0,
    }

    assert get_applications_stats(applications) == expected


def test_get_applications_stats_with_empty_applications() -> None:
    applications: Sequence[Applications] = []

    expected = {
        "completed": 0,
        "not_started": 0,
        "in_progress": 0,
        "submitted": 0,
    }

    assert get_applications_stats(applications) == expected


def test_get_applications_stats_with_mixed_statuses() -> None:
    mock_application_not_stared = MagicMock()
    mock_application_not_stared.status = ApplicationStatus.NOT_STARTED
    mock_application_in_progress = MagicMock()
    mock_application_in_progress.status = ApplicationStatus.IN_PROGRESS
    mock_application_submitted = MagicMock()
    mock_application_submitted.status = ApplicationStatus.SUBMITTED

    applications = [
        mock_application_not_stared,
        mock_application_in_progress,
        mock_application_in_progress,
        mock_application_submitted,
        mock_application_submitted,
        mock_application_submitted,
    ]

    expected = {
        "completed": 0,
        "not_started": 1,
        "in_progress": 2,
        "submitted": 3,
    }

    assert get_applications_stats(applications) == expected


def test_get_applications_stats_when_unknown_status() -> None:
    mock_application_unknown = MagicMock()
    mock_application_unknown.status = "UNKNOWN_STATUS"
    mock_application_completed = MagicMock()
    mock_application_completed.status = ApplicationStatus.COMPLETED

    applications = [mock_application_unknown, mock_application_completed]

    expected = {
        "completed": 1,
        "not_started": 0,
        "in_progress": 0,
        "submitted": 0,
    }

    assert get_applications_stats(applications) == expected


def test_get_assessments_stats_with_all_fields_populated() -> None:
    assessment_record_1 = MagicMock()
    assessment_record_1.workflow_status = AssessmentStatus.COMPLETED
    assessment_record_1.is_withdrawn = False
    assessment_record_1.comments = ["comment1", "comment2"]
    assessment_record_1.tag_associations = ["tag1"]
    assessment_record_1.flags = ["flag1", "flag2"]
    assessment_record_1.change_requests = ["cr1"]

    assessment_record_2 = MagicMock()
    assessment_record_2.workflow_status = AssessmentStatus.IN_PROGRESS
    assessment_record_2.is_withdrawn = True
    assessment_record_2.comments = ["comment3"]
    assessment_record_2.tag_associations = ["tag2", "tag3"]
    assessment_record_2.flags = ["flag3"]
    assessment_record_2.change_requests = []

    assessments = [assessment_record_1, assessment_record_2]

    expected = {
        "completed": 1,
        "not_started": 0,
        "in_progress": 1,
        "withdrawn": 1,
        "comments": 3,
        "tags": 3,
        "flags": 2,  # (2 + 1) - (1 + 0) = 2
        "change_requests": 1,
    }

    assert get_assessments_stats(assessments) == expected


def test_get_assessments_stats_with_empty_assessments() -> None:
    assessments: Sequence[AssessmentRecord] = []

    expected = {
        "completed": 0,
        "not_started": 0,
        "in_progress": 0,
        "withdrawn": 0,
        "comments": 0,
        "tags": 0,
        "flags": 0,
        "change_requests": 0,
    }

    assert get_assessments_stats(assessments) == expected


def test_get_assessments_stats_with_only_completed_assessments() -> None:
    assessment_record_1 = MagicMock()
    assessment_record_1.workflow_status = AssessmentStatus.COMPLETED
    assessment_record_1.is_withdrawn = False
    assessment_record_1.comments = []
    assessment_record_1.tag_associations = []
    assessment_record_1.flags = []
    assessment_record_1.change_requests = []

    assessment_record_2 = MagicMock()
    assessment_record_2.workflow_status = AssessmentStatus.COMPLETED
    assessment_record_2.is_withdrawn = False
    assessment_record_2.comments = ["comment1"]
    assessment_record_2.tag_associations = ["tag1"]
    assessment_record_2.flags = ["flag1"]
    assessment_record_2.change_requests = ["cr1"]

    assessments = [assessment_record_1, assessment_record_2]

    expected = {
        "completed": 2,
        "not_started": 0,
        "in_progress": 0,
        "withdrawn": 0,
        "comments": 1,
        "tags": 1,
        "flags": 0,  # (0 + 1) - (0 + 1) = 0
        "change_requests": 1,
    }

    assert get_assessments_stats(assessments) == expected


def test_get_assessments_stats_with_withdrawn_assessments() -> None:
    assessment_record_1 = MagicMock()
    assessment_record_1.workflow_status = AssessmentStatus.NOT_STARTED
    assessment_record_1.is_withdrawn = True
    assessment_record_1.comments = []
    assessment_record_1.tag_associations = []
    assessment_record_1.flags = []
    assessment_record_1.change_requests = []

    assessment_record_2 = MagicMock()
    assessment_record_2.workflow_status = AssessmentStatus.IN_PROGRESS
    assessment_record_2.is_withdrawn = True
    assessment_record_2.comments = ["comment1"]
    assessment_record_2.tag_associations = ["tag1"]
    assessment_record_2.flags = ["flag1"]
    assessment_record_2.change_requests = ["cr1"]

    assessments = [assessment_record_1, assessment_record_2]

    expected = {
        "completed": 0,
        "not_started": 1,
        "in_progress": 1,
        "withdrawn": 2,
        "comments": 1,
        "tags": 1,
        "flags": 0,  # (0 + 1) - (0 + 1) = 0
        "change_requests": 1,
    }

    assert get_assessments_stats(assessments) == expected


def test_get_assessments_stats_with_flags_and_change_requests() -> None:
    assessment_record_1 = MagicMock()
    assessment_record_1.workflow_status = AssessmentStatus.COMPLETED
    assessment_record_1.is_withdrawn = False
    assessment_record_1.comments = []
    assessment_record_1.tag_associations = []
    assessment_record_1.flags = ["flag1", "flag2"]
    assessment_record_1.change_requests = ["cr1"]

    assessment_record_2 = MagicMock()
    assessment_record_2.workflow_status = AssessmentStatus.IN_PROGRESS
    assessment_record_2.is_withdrawn = False
    assessment_record_2.comments = []
    assessment_record_2.tag_associations = []
    assessment_record_2.flags = ["flag3"]
    assessment_record_2.change_requests = []

    assessments = [assessment_record_1, assessment_record_2]

    expected = {
        "completed": 1,
        "not_started": 0,
        "in_progress": 1,
        "withdrawn": 0,
        "comments": 0,
        "tags": 0,
        "flags": 2,  # (2 + 1) - (1 + 0) = 2
        "change_requests": 1,
    }

    assert get_assessments_stats(assessments) == expected


def test_get_assessment_averages_with_empty_assessments() -> None:
    assessments: Sequence[AssessmentRecord] = []

    assessment_stats = {
        "completed": 0,
        "comments": 0,
        "tags": 0,
        "flags": 0,
        "change_requests": 0,
    }

    expected = {
        "application_success_rate": 0.00,
        "comments_per_assessment": 0.00,
        "tags_per_assessment": 0.00,
        "flags_per_assessment": 0.00,
        "change_requests_per_assessment": 0.00,
    }

    assert get_assessment_averages(assessments, assessment_stats) == expected


def test_get_assessment_averages_with_all_zeros() -> None:
    assessments = [MagicMock(), MagicMock()]

    assessment_stats = {
        "completed": 0,
        "comments": 0,
        "tags": 0,
        "flags": 0,
        "change_requests": 0,
    }

    expected = {
        "application_success_rate": 0.00,
        "comments_per_assessment": 0.00,
        "tags_per_assessment": 0.00,
        "flags_per_assessment": 0.00,
        "change_requests_per_assessment": 0.00,
    }

    assert get_assessment_averages(assessments, assessment_stats) == expected


def test_get_assessment_averages_with_all_fields_populated() -> None:
    assessments = [MagicMock(), MagicMock(), MagicMock()]

    assessment_stats = {
        "completed": 2,
        "comments": 6,
        "tags": 3,
        "flags": 4,
        "change_requests": 1,
    }

    expected = {
        "application_success_rate": round(2 * 100 / 3, 2),  # 66.67
        "comments_per_assessment": round(6 / 3, 2),  # 2.00
        "tags_per_assessment": round(3 / 3, 2),  # 1.00
        "flags_per_assessment": round(4 / 3, 2),  # 1.33
        "change_requests_per_assessment": round(1 / 3, 2),  # 0.33
    }

    assert get_assessment_averages(assessments, assessment_stats) == expected


def test_get_assessment_averages_with_single_assessment() -> None:
    assessments = [MagicMock()]

    assessment_stats = {
        "completed": 1,
        "comments": 5,
        "tags": 2,
        "flags": 3,
        "change_requests": 1,
    }

    expected = {
        "application_success_rate": round(1 * 100 / 1, 2),  # 100.00
        "comments_per_assessment": round(5 / 1, 2),  # 5.00
        "tags_per_assessment": round(2 / 1, 2),  # 2.00
        "flags_per_assessment": round(3 / 1, 2),  # 3.00
        "change_requests_per_assessment": round(1 / 1, 2),  # 1.00
    }

    assert get_assessment_averages(assessments, assessment_stats) == expected


def test_get_assessment_averages_with_rounding() -> None:
    assessments = [MagicMock(), MagicMock()]

    assessment_stats = {
        "completed": 1,
        "comments": 3,
        "tags": 1,
        "flags": 1,
        "change_requests": 1,
    }

    expected = {
        "application_success_rate": round(1 * 100 / 2, 2),  # 50.00
        "comments_per_assessment": round(3 / 2, 2),  # 1.50
        "tags_per_assessment": round(1 / 2, 2),  # 0.50
        "flags_per_assessment": round(1 / 2, 2),  # 0.50
        "change_requests_per_assessment": round(1 / 2, 2),  # 0.50
    }

    assert get_assessment_averages(assessments, assessment_stats) == expected
