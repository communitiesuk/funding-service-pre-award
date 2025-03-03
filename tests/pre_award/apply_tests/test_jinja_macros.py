from bs4 import BeautifulSoup
from flask import Flask, get_template_attribute, render_template_string

from pre_award.apply.models.statuses import get_formatted


def test_tasklist_section_without_change_requests(app: Flask) -> None:
    with app.app_context():
        rendered = render_template_string(
            "{{ tasklist_section(section, application_meta_data, application_status, index, existing_feedback_map) }}",
            tasklist_section=get_template_attribute("apply/partials/tasklist_section.html", "tasklist_section"),
            section={
                "section_title": "Test Section",
                "forms": [
                    {"form_title": "Form A", "form_name": "form_a", "state": {"status": "IN_PROGRESS"}},
                    {"form_title": "Form B", "form_name": "form_b", "state": {"status": "COMPLETED"}},
                ],
            },
            application_meta_data={
                "application_id": "12345",
                "is_resubmission": False,
                "change_requested_status": "CHANGE_REQUESTED",
            },
            application_status=get_formatted,
            index=0,
            existing_feedback_map={},
        )

    soup = BeautifulSoup(rendered, "html.parser")
    links = soup.find_all("a", class_="govuk-link--no-visited-state")

    assert len(links) == 2, "Expected all to be links when no change requests exist"


def test_tasklist_section_with_change_requests(app: Flask) -> None:
    with app.app_context():
        rendered = render_template_string(
            """{{ tasklist_section(section, application_meta_data, application_status, index, existing_feedback_map,
            form_names_with_change_request) }}""",
            tasklist_section=get_template_attribute("apply/partials/tasklist_section.html", "tasklist_section"),
            section={
                "section_title": "Test Section",
                "forms": [
                    {"form_title": "Form A", "form_name": "form_a", "state": {"status": "COMPLETED"}},
                    {
                        "form_title": "Form B",
                        "form_name": "form_b",
                        "state": {"status": "CHANGE_REQUESTED", "questions": [{"fields": [{"key": "field_key_1"}]}]},
                    },
                ],
            },
            application_meta_data={
                "application_id": "12345",
                "is_resubmission": True,
                "change_requested_status": "CHANGE_REQUESTED",
            },
            application_status=get_formatted,
            index=0,
            existing_feedback_map={},
            form_names_with_change_request=["form_b"],
        )

    soup = BeautifulSoup(rendered, "html.parser")
    links = soup.find_all("a", class_="govuk-link--no-visited-state")

    assert len(links) == 1, """Expected one link when change requests exist and form['questions']['fields']['key']
        is in form_names_with_change_request"""
