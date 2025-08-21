from unittest.mock import Mock

from pre_award.apply.constants import ApplicationStatus
from pre_award.apply.models.application import Application


def test_match_forms_to_state_all_forms_complete(apply_test_client):
    application = Application(
        id="app123",
        reference="ref123",
        account_id="acc123",
        status=ApplicationStatus.COMPLETED.name,
        fund_id="fund456",
        round_id="round789",
        project_name="Test Project",
        date_submitted=None,
        started_at=None,
        last_edited=None,
        language="en",
        forms=[
            {"name": "form_1", "status": ApplicationStatus.COMPLETED.name},
            {"name": "form_2", "status": ApplicationStatus.COMPLETED.name},
        ],
        is_deleted=False,
    )

    display_config = [
        Mock(
            title="Section 1",
            weighting=1,
            requires_feedback=False,
            section_id="section_1",
            children=[
                Mock(form_name="form_1", title="Form 1"),
                Mock(form_name="form_2", title="Form 2"),
            ],
        ),
    ]

    expected_sections_config = [
        {
            "section_title": "Section 1",
            "section_weighting": 1,
            "requires_feedback": False,
            "feedback_status": ApplicationStatus.NOT_STARTED.name,
            "section_id": "section_1",
            "forms": [
                {
                    "form_name": "form_1",
                    "state": {"name": "form_1", "status": ApplicationStatus.COMPLETED.name},
                    "form_title": "Form 1",
                },
                {
                    "form_name": "form_2",
                    "state": {"name": "form_2", "status": ApplicationStatus.COMPLETED.name},
                    "form_title": "Form 2",
                },
            ],
            "all_forms_complete": True,
        },
    ]

    result = application.match_forms_to_state(display_config)

    assert result == expected_sections_config


def test_match_forms_to_state_not_complete(apply_test_client):
    application = Application(
        id="app123",
        reference="ref123",
        account_id="acc123",
        status=ApplicationStatus.IN_PROGRESS.name,
        fund_id="fund456",
        round_id="round789",
        project_name="Test Project",
        date_submitted=None,
        started_at=None,
        last_edited=None,
        language="en",
        forms=[
            {"name": "form_1", "status": ApplicationStatus.COMPLETED.name},
            {"name": "form_2", "status": ApplicationStatus.NOT_STARTED.name},
        ],
        is_deleted=False,
    )

    display_config = [
        Mock(
            title="Section 1",
            weighting=1,
            requires_feedback=False,
            section_id="section_1",
            children=[
                Mock(form_name="form_1", title="Form 1"),
                Mock(form_name="form_2", title="Form 2"),
            ],
        ),
        Mock(
            title="Section 2",
            weighting=2,
            requires_feedback=True,
            section_id="section_2",
            children=[
                Mock(form_name="form_3", title="Form 3"),
            ],
        ),
    ]

    expected_sections_config = [
        {
            "section_title": "Section 1",
            "section_weighting": 1,
            "requires_feedback": False,
            "feedback_status": ApplicationStatus.NOT_STARTED.name,
            "section_id": "section_1",
            "forms": [
                {
                    "form_name": "form_1",
                    "state": {"name": "form_1", "status": ApplicationStatus.COMPLETED.name},
                    "form_title": "Form 1",
                },
                {
                    "form_name": "form_2",
                    "state": {"name": "form_2", "status": ApplicationStatus.NOT_STARTED.name},
                    "form_title": "Form 2",
                },
            ],
            "all_forms_complete": False,
        },
        {
            "section_title": "Section 2",
            "section_weighting": 2,
            "requires_feedback": True,
            "feedback_status": ApplicationStatus.NOT_STARTED.name,
            "section_id": "section_2",
            "forms": [
                {
                    "form_name": "form_3",
                    "state": None,
                    "form_title": "Form 3",
                }
            ],
            "all_forms_complete": False,
        },
    ]

    result = application.match_forms_to_state(display_config)

    assert result == expected_sections_config
