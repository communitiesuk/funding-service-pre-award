"""
Contains test configuration.
"""

from datetime import datetime
from typing import Any
from uuid import uuid4

import pytest
from flask import Flask
from flask.testing import FlaskClient
from sqlalchemy_utils import Ltree
from werkzeug.test import TestResponse

from app import create_app
from pre_award.config import Config
from pre_award.fund_store.db.models.section import Section
from pre_award.fund_store.db.queries import insert_fund_data, insert_sections, upsert_round_data
from services.data.models.fund import Fund, FundingType
from services.data.models.round import Round


@pytest.fixture(scope="session")
def seed_dynamic_data(request, app, clear_test_data, _db):
    marker = request.node.get_closest_marker("seed_config")
    fund_count = 0
    round_count = 0
    if marker is None:
        fund_id = str(uuid4())
        round_id_1 = str(uuid4())
        seed_config = {
            "funds": [
                {
                    "id": fund_id,
                    "short_name": "FUND",
                    "funding_type": "COMPETITIVE",
                    "ggis_scheme_reference_number": "",
                    "rounds": [
                        {
                            "id": round_id_1,
                            "sections": [
                                Section(
                                    id=1000,
                                    round_id=round_id_1,
                                    title_json={"en": "Application"},
                                    path=Ltree("3.1"),
                                ),
                                Section(
                                    id=1008,
                                    round_id=round_id_1,
                                    title_json={"en": "skills"},
                                    path=Ltree("3.1.3"),
                                ),
                                Section(
                                    id=1001,
                                    round_id=round_id_1,
                                    title_json={"en": "Middle1"},
                                    path=Ltree("3.1.1"),
                                ),
                                Section(
                                    id=1002,
                                    round_id=round_id_1,
                                    title_json={"en": "Bottom1"},
                                    path=Ltree("3.1.1.1"),
                                ),
                                Section(
                                    id=1003,
                                    round_id=round_id_1,
                                    title_json={"en": "Middle2"},
                                    path=Ltree("3.1.2"),
                                ),
                                Section(
                                    id=1004,
                                    round_id=round_id_1,
                                    title_json={"en": "Bottom2"},
                                    path=Ltree("3.1.2.1"),
                                ),
                                Section(
                                    id=1005,
                                    round_id=round_id_1,
                                    title_json={"en": "Assessment"},
                                    path=Ltree("0.2"),
                                ),
                                Section(
                                    id=1006,
                                    round_id=round_id_1,
                                    title_json={"en": "assess section 1"},
                                    path=Ltree("0.2.1"),
                                ),
                                Section(
                                    id=1007,
                                    round_id=round_id_1,
                                    title_json={"en": "assess section 1 a"},
                                    path=Ltree("0.2.1.1"),
                                ),
                            ],
                        },
                        {
                            "id": str(uuid4()),
                            "sections": [],
                            # "fund_id": fund_id,
                            # "short_name": "RND2"
                        },
                    ],
                }
            ]
        }
    else:
        seed_config = marker.args[0]
    inserted_data = {"funds": []}
    for fund in seed_config["funds"]:
        fund_count += 1
        # fund_id = str(uuid4())
        # short_suffix = fund_id[0:4]
        fund_config = {
            "id": fund["id"],
            "name_json": {"en": f"Unit Test Fund {fund_count}"},  # fund['short_name']}",
            "title_json": {"en": f"Unit test fund title {fund_count}"},  # {fund['short_name']}",
            "short_name": f"FND{fund_count}",  # fund["short_name"],
            "description_json": {"en": "testing description"},
            "welsh_available": True,
            "owner_organisation_name": "testing org name",
            "owner_organisation_shortname": "TON",
            "owner_organisation_logo_uri": "...",
            "funding_type": fund["funding_type"] or FundingType.COMPETITIVE,
            "ggis_scheme_reference_number": fund["ggis_scheme_reference_number"] or "",
        }
        insert_fund_data(fund_config)
        rounds = []
        for round in fund["rounds"]:
            round_count += 1
            # round_id = str(uuid4())
            # round_short_suffix = round_id[0:4]
            round_config = {
                "id": round["id"],
                "title_json": {"en": f"Unit Test Round {round_count}"},  # {round['short_name']}",
                "short_name": f"RND{round_count}",  # round["short_name"],
                "opens": "2023-01-01 12:00:00",
                "assessment_start": None,
                "deadline": "2023-12-31 12:00:00",
                "application_reminder_sent": True,
                "reminder_date": None,
                "fund_id": fund["id"],
                "assessment_deadline": "2024-02-28 12:00:00",
                "prospectus": "http://google.com",
                "privacy_notice": "http://google.com",
                "reference_contact_page_over_email": False,
                "contact_us_banner_json": {"en": "", "cy": ""},
                "contact_email": "contact@example.com",
                "contact_phone": "01234567890",
                "contact_textphone": "1234",
                "support_times": "8am - 12:30pm",
                "support_days": "Monday and Tuesday",
                "instructions_json": {"en": "Instructions to fill out the form"},
                "project_name_field_id": "abc123",
                "feedback_link": "www.feedback.link",
                "application_guidance_json": {"en": "help text"},
                "guidance_url": "guidance link",
                "all_uploaded_documents_section_available": False,
                "application_fields_download_available": False,
                "display_logo_on_pdf_exports": False,
                "mark_as_complete_enabled": False,
                "is_expression_of_interest": False,
                "feedback_survey_config": {
                    "has_feedback_survey": False,
                    "has_section_feedback": False,
                    "is_feedback_survey_optional": True,
                    "is_section_feedback_optional": True,
                },
                "eligibility_config": {"has_eligibility": False},
                "eoi_decision_schema": None,
            }
            rounds.append(round_config)

        upsert_round_data(rounds)
        inserted_data["funds"].append({"rounds": rounds, "id": fund_id, "short_name": fund["short_name"]})

        for fund in seed_config["funds"]:
            for round in fund["rounds"]:
                insert_sections(round["sections"])

    yield inserted_data


@pytest.fixture(scope="session")
def app(request) -> Flask:
    app = create_app()
    request.getfixturevalue("mock_redis")
    yield app


class _FlaskClientWithHost(FlaskClient):
    def open(
        self,
        *args: Any,
        buffered: bool = False,
        follow_redirects: bool = False,
        **kwargs: Any,
    ) -> TestResponse:
        if "headers" in kwargs:
            kwargs["headers"].setdefault("Host", Config.API_HOST)
        else:
            kwargs.setdefault("headers", {"Host": Config.API_HOST})
        return super().open(*args, buffered=buffered, follow_redirects=follow_redirects, **kwargs)


@pytest.fixture(scope="function")
def flask_test_client():
    app = create_app()
    app.test_client_class = _FlaskClientWithHost
    with app.test_client() as test_client:
        yield test_client


@pytest.fixture(scope="function")
def mock_get_fund_round(mocker):
    mock_fund: Fund = Fund(
        id=uuid4(),
        short_name="FND1",
        name_json={"en": "Fund Name 1"},
        title_json={"en": "Fund 1"},
        description_json={"en": "description text"},
        funding_type=FundingType.COMPETITIVE,
        ggis_scheme_reference_number="G2-SCH-0000092414",
    )
    round_config = {
        "id": uuid4(),
        "assessment_deadline": datetime.now(),
        "deadline": datetime.now(),
        "reminder_date": None,
        "fund_id": "",
        "opens": datetime.now(),
        "assessment_start": None,
        "prospectus": "",
        "privacy_notice": "",
        "contact_email": "",
        "contact_phone": "",
        "contact_textphone": "",
        "support_days": "",
        "support_times": "",
    }
    mock_round: Round = Round(title_json={"en": "Round 1"}, short_name="RND1", **round_config)
    mocker.patch("pre_award.fund_store.api.routes.get_all_funds", return_value=[mock_fund])
    mocker.patch("pre_award.fund_store.api.routes.get_fund_by_id", return_value=mock_fund)
    mocker.patch("pre_award.fund_store.api.routes.get_fund_by_short_name", return_value=mock_fund)
    mocker.patch("pre_award.fund_store.api.routes.get_round_by_id", return_value=mock_round)
    mocker.patch("pre_award.fund_store.api.routes.get_round_by_short_name", return_value=mock_round)
    mocker.patch("pre_award.fund_store.api.routes.get_rounds_for_fund_by_id", return_value=[mock_round])
    mocker.patch("pre_award.fund_store.api.routes.get_rounds_for_fund_by_short_name", return_value=[mock_round])


@pytest.fixture(scope="function")
def mock_get_sections(mocker):
    mock_sections = Section(
        id=0,
        title_json={"en": "Top"},
        path="0",
        children=[
            Section(
                id=1,
                title_json={"en": "Middle"},
                path="0.1",
                children=[Section(id=2, title_json={"en": "Bottom"}, path="0.1.1", children=[])],
            ),
            Section(
                id=3,
                title_json={"en": "Middle2"},
                path="0.2",
                children=[Section(id=4, title_json={"en": "Bottom2"}, path="0.2.1", children=[])],
            ),
        ],
    )
    mocker.patch("pre_award.fund_store.api.routes.get_application_sections_for_round", return_value=[mock_sections])
    mocker.patch("pre_award.fund_store.api.routes.get_assessment_sections_for_round", return_value=[mock_sections])
