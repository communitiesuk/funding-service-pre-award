from unittest.mock import Mock

from pre_award.assess.services.models.flag import FlagType
from pre_award.assessment_store.api.routes._helpers import _derive_status
from pre_award.assessment_store.db.models.assessment_record.enums import Status


def test_derive_status():
    # Mock flags
    flag_raised = Mock()
    flag_raised.sections_to_flag = {"criteria1"}
    flag_raised.latest_status = FlagType.RAISED

    flag_resolved = Mock()
    flag_resolved.sections_to_flag = {"criteria1"}
    flag_resolved.latest_status = FlagType.RESOLVED

    # Test cases
    test_cases = [
        # No scoring, no flags, no comments
        {
            "change_requests": [],
            "workflow_status": "ANY",
            "sub_criteria_id": "criteria1",
            "expected": Status.NOT_STARTED.name,
        },
        # Scored
        {
            "change_requests": [],
            "workflow_status": "ANY",
            "sub_criteria_id": "criteria1",
            "score_map": {"criteria1": "any_score"},
            "expected": Status.COMPLETED.name,
        },
        # Flag with raised status
        {
            "change_requests": [flag_raised],
            "workflow_status": "ANY",
            "sub_criteria_id": "criteria1",
            "expected": Status.CHANGE_REQUESTED.name,
        },
        # Flag resolved, any workflow status
        {
            "change_requests": [flag_resolved],
            "workflow_status": Status.CHANGE_REQUESTED.name,
            "sub_criteria_id": "criteria1",
            "expected": Status.CHANGE_RECEIVED.name,
        },
        # Flag raised supersedes workflow status
        {
            "change_requests": [flag_raised],
            "workflow_status": Status.CHANGE_RECEIVED.name,
            "sub_criteria_id": "criteria1",
            "expected": Status.CHANGE_REQUESTED.name,
        },
    ]

    for case in test_cases:
        score_map = case.get("score_map", {})
        comment_map = case.get("comment_map", {})
        result = _derive_status(
            score_map=score_map,
            comment_map=comment_map,
            change_requests=case["change_requests"],
            workflow_status=case["workflow_status"],
            sub_criteria_id=case["sub_criteria_id"],
        )

        assert result == case["expected"], f"Failed for case: {case}"
