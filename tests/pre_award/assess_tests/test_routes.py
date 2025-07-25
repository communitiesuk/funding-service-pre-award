import urllib
from collections import namedtuple
from unittest import mock

import pytest
from bs4 import BeautifulSoup
from flask import session

from pre_award.apply.models.fund import Fund
from pre_award.assess.assessments.models.round_status import RoundStatus
from pre_award.assess.assessments.models.round_summary import RoundSummary, Stats
from pre_award.assess.services.models.flag import Flag
from pre_award.assessment_store.db.models.assessment_record.enums import Status
from tests.pre_award.apply_tests.api_data.test_data import TEST_APPLICATION_SUMMARIES, TEST_FUNDS_DATA, TEST_ROUNDS_DATA
from tests.pre_award.assess_tests.api_data.test_data import fund_specific_claim_map
from tests.pre_award.assess_tests.conftest import (
    assert_fund_dashboard,
    create_valid_token,
    get_subcriteria_soup,
    test_commenter_claims,
    test_dpif_commenter_claims,
    test_lead_assessor_claims,
)


class TestRoutes:
    @pytest.mark.mock_parameters(
        {
            "get_assessment_stats_path": [
                "pre_award.assess.assessments.models.round_summary.get_assessments_stats",
            ],
            "get_rounds_path": [
                "pre_award.assess.assessments.models.round_summary.get_rounds",
            ],
            "fund_id": "test-fund",
            "round_id": "test-round",
        }
    )
    def test_route_landing(
        self,
        assess_test_client,
        mock_get_funds,
        mock_get_rounds,
        mock_get_assessment_stats,
    ):
        response = assess_test_client.get("/assess/assessor_tool_dashboard/")
        assert 200 == response.status_code, "Wrong status code on response"
        soup = BeautifulSoup(response.data, "html.parser")
        assert soup.title.string == "Assessment tool dashboard – Assessment Hub – GOV.UK", (
            "Response does not contain expected heading"
        )
        all_table_data_elements = str(
            soup.find_all(["td", "th"], class_=lambda c: c and ("govuk-table__cell" in c or "govuk-table__header" in c))
        )
        assert len(all_table_data_elements) > 0
        project_titles = [
            "Assessment closing date",
            "Applications received",
            "Assessments completed",
            "QA Complete",
        ]
        live_round_titles = [
            "Application closing date",
            "Applications submitted",
            "Applications in progress",
            "Applications not started",
            "Applications completed but not started",
        ]
        # breakpoint()
        assert all(title in all_table_data_elements for title in project_titles) or all(
            title in all_table_data_elements for title in live_round_titles
        )
        for mock_func in mock_get_assessment_stats:
            assert mock_func.call_count == 1
        for mock_func in mock_get_rounds:
            assert mock_func.call_count == 1

    @pytest.mark.mock_parameters(
        {
            "get_assessment_stats_path": [
                "assess.assessments.models.round_summary.get_assessments_stats",
            ],
            "get_rounds_path": [
                "assess.assessments.models.round_summary.get_rounds",
            ],
            "fund_id": "test-fund",
            "round_id": "test-round",
        }
    )
    @pytest.mark.parametrize(
        "exp_link_count, download_available, mock_is_lead_assessor",
        [(2, False, True), (4, True, True), (0, False, False)],
    )
    def test_route_landing_export_link_visibility(
        self,
        assess_test_client,
        mock_get_funds,
        mocker,
        exp_link_count,
        download_available,
        mock_is_lead_assessor,
    ):
        access_controller_mock = mock.MagicMock()
        access_controller_mock.is_lead_assessor = mock_is_lead_assessor
        mocker.patch(
            "pre_award.assess.assessments.routes.create_round_summaries",
            return_value=[
                RoundSummary(
                    status=RoundStatus(False, False, True, True, True, False),
                    fund_id="111",
                    round_id="222",
                    fund_name="test fund",
                    round_name="test round",
                    assessments_href="",
                    access_controller=access_controller_mock,
                    export_href="/assess/assessor_export/TF/tr/ASSESSOR_EXPORT",
                    feedback_export_href="/assess/feedback_export/TF/tr",
                    assessment_tracker_href="/assess/tracker",
                    round_application_fields_download_available=download_available,
                    sorting_date="",
                    assessment_stats=Stats(
                        date="2023-12-12T12:00:00",
                        total_received=1,
                        completed=1,
                        started=1,
                        qa_complete=1,
                        stopped=1,
                    ),
                    live_round_stats=None,
                )
            ],
        )
        token = create_valid_token(test_lead_assessor_claims)
        assess_test_client.set_cookie("fsd_user_token", token)
        response = assess_test_client.get("/assess/assessor_tool_dashboard/")
        assert 200 == response.status_code, "Wrong status code on response"
        soup = BeautifulSoup(response.data, "html.parser")
        all_links = soup.find_all("a", class_="govuk-link")
        all_exports_links = [link for link in all_links if "Export" in link.get_text()]
        assert len(all_exports_links) == exp_link_count
        if not download_available and mock_is_lead_assessor:
            assert "Assessment Tracker Export" in all_exports_links[-2].get_text()

    fund_case = namedtuple("FundCase", "fund_short round_short role_key assigned_div expected_extra_tabs")

    @pytest.mark.parametrize(
        "case",
        [
            fund_case("CYP", "TR", "ASSESSOR", "assigned-to-you", []),
            fund_case("CYP", "TR", "LEAD_ASSESSOR", "assigned-to-you", ["reporting-to-you"]),
            fund_case("NSTF", "TR", "ASSESSOR", "assigned-to-you", []),
            fund_case("NSTF", "TR", "LEAD_ASSESSOR", "assigned-to-you", ["reporting-to-you"]),
            fund_case("COF", "TR", "ASSESSOR", "assigned-to-you", []),
            fund_case("COF", "TR", "LEAD_ASSESSOR", "assigned-to-you", ["reporting-to-you"]),
            fund_case("DPIF", "TR", "ASSESSOR", "assigned-to-you", []),
            fund_case("DPIF", "TR", "LEAD_ASSESSOR", "assigned-to-you", ["reporting-to-you"]),
        ],
    )
    def test_fund_dashboard_for_assessors(
        self,
        case,
        assess_test_client,
        fund_dashboard_all_mocks,
        mock_competed_cof_fund,
    ):
        fund_short_name, round_short_name = case.fund_short, case.round_short

        # set the cookie to the correct assessor role
        token = create_valid_token(fund_specific_claim_map[fund_short_name][case.role_key])
        assess_test_client.set_cookie("fsd_user_token", token)

        # hit the dashboard
        response = assess_test_client.get(
            f"/assess/fund_dashboard/{fund_short_name}/{round_short_name}",
            follow_redirects=True,
        )

        # common expectations
        expected_titles = [
            "Reference",
            "Project name",
            "Funding requested",
            "Asset type",
            "Location",
            "Status",
            "Assigned to",
            "Date submitted",
        ]
        expected_tabs = ["All applications", "Assigned to you (1)"]
        for extra in case.expected_extra_tabs:
            expected_tabs.append(extra.replace("-", " ").capitalize() + " (1)")

        expected_first_row = [
            "FQAC",
            "Project Completed Flag and QA",
            "£7,000.00",
            "Gallery",
            "England",
            "1 tag\n                            \n\n\n\n\n                                Tag one red",
            "Flagged for test_team",
            "-",
            "04/01/2024 at 15:54",
        ]
        expected_filter_labels = [
            "Search reference or project name",
            "Filter by status",
            "Filter by assigned to",
            "Filter by tag",
        ]
        expected_assigned_values = [
            "ASAP",
            "Project In prog and assigned",
            "£13,000.00",
            "Gallery",
            "England",
            fund_specific_claim_map[fund_short_name][case.role_key]["fullName"],
        ]

        # do all the assertions
        assert_fund_dashboard(
            response,
            expected_titles=expected_titles,
            expected_tabs=expected_tabs,
            expected_first_row=expected_first_row,
            expected_filter_labels=expected_filter_labels,
            expected_assigned_values=expected_assigned_values,
            assigned_div_id=case.assigned_div,
        )

    @pytest.mark.mock_parameters(
        {
            "fund_short_name": "COF",
            "round_short_name": "TR",
            "expected_search_params": {
                "search_term": "",
                "search_in": "project_name,short_id",
                "asset_type": "ALL",
                "assigned_to": "ALL",
                "status": "QA_COMPLETE",
                "filter_by_tag": "ALL",
            },
        }
    )
    @pytest.mark.application_id("resolved_app")
    def test_team_stats_are_present(
        self,
        request,
        assess_test_client,
        mock_get_funds,
        mock_get_round,
        mock_get_fund,
        mock_get_application_overviews,
        mock_get_users_for_fund,
        mock_get_assessment_progress,
        mock_get_application_metadata,
        mock_get_active_tags_for_fund_round,
        mock_get_tag_types,
        mock_competed_cof_fund,
    ):
        params = request.node.get_closest_marker("mock_parameters").args[0]
        fund_short_name = params["fund_short_name"]
        round_short_name = params["round_short_name"]

        assess_test_client.set_cookie(
            "fsd_user_token",
            create_valid_token(fund_specific_claim_map[fund_short_name]["LEAD_ASSESSOR"]),
        )

        response = assess_test_client.get(
            f"/assess/fund_dashboard/{fund_short_name}/{round_short_name}",
            follow_redirects=True,
            query_string={"status": "QA_COMPLETE"},
        )

        assert 200 == response.status_code, "Wrong status code on response"
        assert b"Total flagged for test_team" in response.data

    @pytest.mark.mock_parameters(
        {
            "fund_short_name": "COF",
            "round_short_name": "TR",
            "expected_search_params": {
                "search_term": "",
                "search_in": "project_name,short_id",
                "asset_type": "ALL",
                "assigned_to": "Not assigned",
                "status": "ALL",
                "filter_by_tag": "ALL",
            },
        }
    )
    def test_route_fund_dashboard_filter_not_assigned(
        self,
        request,
        assess_test_client,
        mock_get_funds,
        mock_get_round,
        mock_get_fund,
        mock_get_application_overviews,
        mock_get_users_for_fund,
        mock_get_assessment_progress,
        mock_get_application_metadata,
        mock_get_active_tags_for_fund_round,
        mock_get_tag_types,
        mock_competed_cof_fund,
    ):
        params = request.node.get_closest_marker("mock_parameters").args[0]
        fund_short_name = params["fund_short_name"]
        round_short_name = params["round_short_name"]

        assess_test_client.set_cookie(
            "fsd_user_token",
            create_valid_token(fund_specific_claim_map[fund_short_name]["LEAD_ASSESSOR"]),
        )

        response = assess_test_client.get(
            f"/assess/fund_dashboard/{fund_short_name}/{round_short_name}",
            follow_redirects=True,
            query_string={"assigned_to": "Not assigned"},
        )

        assert 200 == response.status_code, "Wrong status code on response"
        soup = BeautifulSoup(response.data, "html.parser")

        all_applications_section = soup.find("h1", class_="govuk-heading-l", string="All applications")
        table = all_applications_section.find_next("table", {"id": "application_overviews_table"})
        rows = table.find_all("tr", class_="govuk-table__row")

        reference_values = []
        for row in rows:
            cells = row.find_all("td", class_="govuk-table__cell")
            if cells:
                reference_values.append(cells[0].text.strip())  # Assuming reference is the first column

        expected_values = ["FQAC", "FS", "INP"]

        # Check that each expected value appears exactly once in the reference column
        for value in expected_values:
            assert reference_values.count(value) == 1

        for value in reference_values:
            # Application with reference 'ASAP' is the assigned application
            assert value != "ASAP"

    @pytest.mark.mock_parameters(
        {
            "fund_short_name": "COF",
            "round_short_name": "TR",
            "expected_search_params": {
                "search_term": "",
                "search_in": "project_name,short_id",
                "asset_type": "ALL",
                "assigned_to": "ALL",
                "status": "QA_COMPLETE",
                "filter_by_tag": "ALL",
            },
        }
    )
    def test_route_fund_dashboard_filter_session_persistence(
        self,
        request,
        assess_test_client,
        app,
        mock_get_funds,
        mock_get_round,
        mock_get_fund,
        mock_get_application_overviews,
        mock_get_users_for_fund,
        mock_get_assessment_progress,
        mock_get_application_metadata,
        mock_get_active_tags_for_fund_round,
        mock_get_tag_types,
        mock_competed_cof_fund,
    ):
        params = request.node.get_closest_marker("mock_parameters").args[0]
        fund_short_name = params["fund_short_name"]
        round_short_name = params["round_short_name"]
        expected_search_params = params["expected_search_params"]

        assess_test_client.set_cookie(
            "fsd_user_token",
            create_valid_token(fund_specific_claim_map[fund_short_name]["LEAD_ASSESSOR"]),
        )

        response = assess_test_client.get(
            f"/assess/fund_dashboard/{fund_short_name}/{round_short_name}",
            follow_redirects=True,
            query_string=expected_search_params,
        )

        assert 200 == response.status_code, "Wrong status code on response"

        with assess_test_client.session_transaction() as sess:
            assert sess is not None
            assert sess.get(f"filter_params_{fund_short_name.upper()}_{round_short_name.upper()}") == {
                "search_term": "",
                "assigned_to": "ALL",
                "status": "QA_COMPLETE",
                "filter_by_tag": "ALL",
            }, "Session did not persist the expected filter parameters"

    @pytest.mark.mock_parameters(
        {
            "fund_short_name": "TF",
            "round_short_name": "TR",
            "expected_search_params": {
                "search_term": "",
                "search_in": "project_name,short_id",
                "asset_type": "ALL",
                "assigned_to": "ALL",
                "status": "QA_COMPLETE",
                "filter_by_tag": "ALL",
            },
        }
    )
    def test_route_fund_dashboard_filter_status(
        self,
        request,
        assess_test_client,
        mock_get_fund,
        mock_get_funds,
        mock_get_round,
        mock_get_application_overviews,
        mock_get_users_for_fund,
        mock_get_assessment_progress,
        mock_get_active_tags_for_fund_round,
        mock_get_tag_types,
        mock_competed_cof_fund,
    ):
        params = request.node.get_closest_marker("mock_parameters").args[0]
        fund_short_name = params["fund_short_name"]
        round_short_name = params["round_short_name"]

        response = assess_test_client.get(
            f"/assess/fund_dashboard/{fund_short_name}/{round_short_name}",
            follow_redirects=True,
            query_string={"status": "QA_COMPLETE"},
        )

        assert 200 == response.status_code, "Wrong status code on response"
        soup = BeautifulSoup(response.data, "html.parser")
        assert soup.title.string == "Team dashboard – Assessment Hub – GOV.UK", (
            "Response does not contain expected heading"
        )

    @pytest.mark.mock_parameters(
        {
            "fund_short_name": "TF",
            "round_short_name": "TR",
            "expected_search_params": {
                "search_term": "",
                "search_in": "project_name,short_id",
                "asset_type": "pub",
                "assigned_to": "ALL",
                "status": "ALL",
                "filter_by_tag": "ALL",
            },
        }
    )
    def test_route_fund_dashboard_filter_asset_type(
        self,
        request,
        assess_test_client,
        mock_get_fund,
        mock_get_funds,
        mock_get_round,
        mock_get_application_overviews,
        mock_get_users_for_fund,
        mock_get_assessment_progress,
        mock_get_active_tags_for_fund_round,
        mock_get_tag_types,
        mock_competed_cof_fund,
    ):
        params = request.node.get_closest_marker("mock_parameters").args[0]
        fund_short_name = params["fund_short_name"]
        round_short_name = params["round_short_name"]

        response = assess_test_client.get(
            f"/assess/fund_dashboard/{fund_short_name}/{round_short_name}",
            follow_redirects=True,
            query_string={"asset_type": "pub"},
        )

        assert 200 == response.status_code, "Wrong status code on response"
        soup = BeautifulSoup(response.data, "html.parser")
        assert soup.title.string == "Team dashboard – Assessment Hub – GOV.UK", (
            "Response does not contain expected heading"
        )

    @pytest.mark.mock_parameters(
        {
            "fund_short_name": "TF",
            "round_short_name": "TR",
            "expected_search_params": {
                "search_term": "hello",
                "search_in": "project_name,short_id",
                "assigned_to": "ALL",
                "asset_type": "ALL",
                "status": "ALL",
                "filter_by_tag": "ALL",
            },
        }
    )
    def test_route_fund_dashboard_search_term(
        self,
        request,
        assess_test_client,
        mock_get_fund,
        mock_get_funds,
        mock_get_round,
        mock_get_application_overviews,
        mock_get_users_for_fund,
        mock_get_assessment_progress,
        mock_get_active_tags_for_fund_round,
        mock_get_tag_types,
        mock_competed_cof_fund,
    ):
        params = request.node.get_closest_marker("mock_parameters").args[0]
        fund_short_name = params["fund_short_name"]
        round_short_name = params["round_short_name"]

        response = assess_test_client.get(
            f"/assess/fund_dashboard/{fund_short_name}/{round_short_name}",
            follow_redirects=True,
            query_string={"search_term": "hello"},
        )

        assert 200 == response.status_code, "Wrong status code on response"
        soup = BeautifulSoup(response.data, "html.parser")
        soup = BeautifulSoup(response.data, "html.parser")
        assert soup.title.string == "Team dashboard – Assessment Hub – GOV.UK", (
            "Response does not contain expected heading"
        )

    @pytest.mark.mock_parameters(
        {
            "fund_short_name": "TF",
            "round_short_name": "TR",
            "expected_search_params": {
                "search_term": "",
                "search_in": "project_name,short_id",
                "asset_type": "ALL",
                "assigned_to": "ALL",
                "status": "ALL",
                "filter_by_tag": "ALL",
            },
        }
    )
    def test_route_fund_dashboard_clear_filters(
        self,
        request,
        assess_test_client,
        mock_get_fund,
        mock_get_funds,
        mock_get_round,
        mock_get_application_overviews,
        mock_get_users_for_fund,
        mock_get_assessment_progress,
        mock_get_active_tags_for_fund_round,
        mock_get_tag_types,
        mock_competed_cof_fund,
    ):
        params = request.node.get_closest_marker("mock_parameters").args[0]
        fund_short_name = params["fund_short_name"]
        round_short_name = params["round_short_name"]

        response = assess_test_client.get(
            f"/assess/fund_dashboard/{fund_short_name}/{round_short_name}",
            follow_redirects=True,
            query_string={
                "clear_filters": "",
                "search_term": "hello",
                "assigned_to": "ALL",
                "asset_type": "cinema",
                "status": "in-progress",
            },
        )

        assert 200 == response.status_code, "Wrong status code on response"
        soup = BeautifulSoup(response.data, "html.parser")
        assert soup.title.string == "Team dashboard – Assessment Hub – GOV.UK", (
            "Response does not contain expected heading"
        )

    @pytest.mark.mock_parameters(
        {
            "fund_short_name": "COF",
            "round_short_name": "TR",
            "expected_search_params": {
                "search_term": "",
                "search_in": "project_name,short_id",
                "asset_type": "ALL",
                "assigned_to": "ALL",
                "status": "ALL",
                "filter_by_tag": "ALL",
            },
        }
    )
    @pytest.mark.parametrize(
        "sort_column,sort_order,column_id",
        [
            ("location", "asc", 4),
            ("location", "desc", 4),
            ("funding_requested", "asc", 3),
            ("funding_requested", "desc", 3),
            ("", "", 4),
        ],
    )
    def test_route_fund_dashboard_sort_column(
        self,
        request,
        assess_test_client,
        mock_get_fund,
        mock_get_funds,
        mock_get_round,
        mock_get_application_overviews,
        mock_get_users_for_fund,
        mock_get_assessment_progress,
        mock_get_application_metadata,
        sort_column,
        sort_order,
        column_id,
        mock_get_active_tags_for_fund_round,
        mock_get_tag_types,
        mock_competed_cof_fund,
    ):
        assess_test_client.set_cookie(
            "fsd_user_token",
            create_valid_token(fund_specific_claim_map["COF"]["ASSESSOR"]),
        )

        params = request.node.get_closest_marker("mock_parameters").args[0]
        fund_short_name = params["fund_short_name"]
        round_short_name = params["round_short_name"]

        response = assess_test_client.get(
            f"/assess/fund_dashboard/{fund_short_name}/{round_short_name}",
            follow_redirects=True,
            query_string={
                "sort_column": sort_column,
                "sort_order": sort_order,
            },
        )

        assert 200 == response.status_code, "Wrong status code on response"
        soup = BeautifulSoup(response.data, "html.parser")

        # Find the table element by its class name
        tbody = soup.find("tbody", {"class": "govuk-table__body"})

        # Find all the elements in the column
        column_data = [row.find_all("td")[column_id].text for idx, row in enumerate(tbody.find_all("tr"))]

        if sort_order == "asc":
            all_table_data_elements = str(
                soup.find_all(
                    "th",
                    attrs={
                        "class": "govuk-table__header",
                        "aria-sort": "ascending",
                    },
                )
            )
            assert 'aria-sort="ascending"' in all_table_data_elements
            assert sort_column in all_table_data_elements
            # check if the data is in ascending order
            assert all(column_data[i] <= column_data[i + 1] for i in range(len(column_data) - 1))
        elif sort_order == "desc":
            all_table_data_elements = str(
                soup.find_all(
                    "th",
                    attrs={
                        "class": "govuk-table__header",
                        "aria-sort": "descending",
                    },
                )
            )
            assert 'aria-sort="descending"' in all_table_data_elements
            assert sort_column in all_table_data_elements
            # check if the data is in descending order
            assert all(column_data[i] >= column_data[i + 1] for i in range(len(column_data) - 1))
        else:
            all_table_data_elements = str(
                soup.find_all(
                    "th",
                    attrs={
                        "class": "govuk-table__header",
                        "aria-sort": "none",
                    },
                )
            )
            assert 'aria-sort="none"' in all_table_data_elements

    @pytest.mark.application_id("resolved_app")
    @pytest.mark.sub_criteria_id("test_sub_criteria_id")
    def test_route_sub_criteria_scoring(
        self,
        assess_test_client,
        request,
        mock_get_sub_criteria,
        mock_get_fund,
        mock_get_funds,
        mock_get_round,
        mock_get_application_metadata,
        mock_get_comments,
        mock_get_scores,
        mock_get_bulk_accounts,
        mock_get_assessor_tasklist_state,
        mock_get_scoring_system,
        mock_competed_cof_fund,
    ):
        application_id = request.node.get_closest_marker("application_id").args[0]
        sub_criteria_id = request.node.get_closest_marker("sub_criteria_id").args[0]
        # Use unittest.mock to create a mock object for get_scores_and_justification # noqa

        token = create_valid_token(test_lead_assessor_claims)
        assess_test_client.set_cookie("fsd_user_token", token)

        # Send a request to the route you want to test
        response = assess_test_client.get(
            f"/assess/application_id/{application_id}/sub_criteria_id/{sub_criteria_id}/score"  # noqa
        )

        # Assert that the response has the expected status code
        assert 200 == response.status_code, "Wrong status code on response"
        soup = BeautifulSoup(response.data, "html.parser")
        assert soup.title.string == "Score – test_sub_criteria – Project In prog and Res – Assessment Hub – GOV.UK"
        assert b"Current score: 3" in response.data
        assert b"Rescore" in response.data
        assert b"Lead assessor" in response.data
        assert b"This is a comment" in response.data

    @pytest.mark.application_id("resolved_app")
    @pytest.mark.sub_criteria_id("test_sub_criteria_id")
    def test_route_sub_criteria_scoring_inaccessible_to_commenters(
        self,
        assess_test_client,
        mock_get_funds,
        mock_get_application_metadata,
        mock_get_fund,
        mock_get_round,
        mock_get_assessor_tasklist_state,
        mock_competed_cof_fund,
        expect_flagging,
    ):
        # Mocking fsd-user-token cookie
        token = create_valid_token(test_commenter_claims)
        assess_test_client.set_cookie("fsd_user_token", token)

        # Send a request to the route you want to test
        response = assess_test_client.get(
            "http://assessment.communities.gov.localhost:3010/assess/application_id/app_123/sub_criteria_id/1a2b3c4d/score"
        )  # noqa

        # Assert that the response has the expected status code
        assert 302 == response.status_code, (
            "Commenter should receive a 302 to authenticator when trying to access the sub criteria scoring page"
        )
        params = {"roles_required": "TF_LEAD_ASSESSOR|TF_ASSESSOR"}
        encoded_params = urllib.parse.urlencode(params)
        assert (
            response.location == f"https://authenticator.communities.gov.localhost:4004/service/user?{encoded_params}"  # noqa
        )

    @pytest.mark.application_id("resolved_app")
    @pytest.mark.sub_criteria_id("test_sub_criteria_id")
    def test_route_sub_criteria_acceptance_redirect_to_score(
        self,
        assess_test_client,
        request,
        mock_get_sub_criteria,
        mock_get_fund,
        mock_get_funds,
        mock_get_round,
        mock_get_application_metadata,
        mock_get_comments,
        mock_get_scores,
        mock_get_bulk_accounts,
        mock_get_assessor_tasklist_state,
        mock_get_scoring_system,
        mock_uncompeted_pfn_fund,
    ):
        application_id = request.node.get_closest_marker("application_id").args[0]
        sub_criteria_id = request.node.get_closest_marker("sub_criteria_id").args[0]

        token = create_valid_token(test_lead_assessor_claims)
        assess_test_client.set_cookie("fsd_user_token", token)
        mock_get_assessor_tasklist_state[1].return_value.is_qa_complete = False
        response = assess_test_client.get(
            f"/assess/application_id/{application_id}/sub_criteria_id/{sub_criteria_id}/score"  # noqa
        )
        assert 200 == response.status_code
        soup = BeautifulSoup(response.data, "html.parser")

        # Page should contain current score banner and rationale
        banner_heading = soup.findAll("h2", class_="govuk-heading-m")[1].text
        assert "Current score" in banner_heading, "Current score not found in the response"

        rationale = soup.findAll("p", class_="govuk-body-m")[0].text
        assert "Rationale" in rationale, "Rationale not found in the response"

    def test_homepage_route_accessible(self, assess_test_client, mock_get_funds):
        # Remove fsd-user-token cookie
        assess_test_client.set_cookie("fsd_user_token", "")

        # Send a request to the homepage "/" route
        response = assess_test_client.get("/")

        # Assert that the response has the expected status code
        assert 200 == response.status_code, "Homepage route should be accessible"

        # Send a request to the root route
        response = assess_test_client.get("", follow_redirects=True)

        # Assert that the response has the expected status code
        assert 200 == response.status_code, "Homepage route should be accessible"

    @pytest.mark.application_id("flagged_qa_completed_app")
    def test_flag_route_already_flagged(
        self,
        request,
        assess_test_client,
        mock_get_flags,
        mock_get_available_teams,
        mock_get_assessor_tasklist_state,
        mock_get_sub_criteria_banner_state,
        mock_get_fund,
        mock_get_funds,
        mock_get_round,
        mock_get_application_metadata,
        mock_competed_cof_fund,
    ):
        application_id = request.node.get_closest_marker("application_id").args[0]
        token = create_valid_token(test_lead_assessor_claims)
        assess_test_client.set_cookie("fsd_user_token", token)

        response = assess_test_client.get(f"assess/flag/{application_id}")

        assert response.status_code == 200

    @pytest.mark.application_id("resolved_app")
    @pytest.mark.flag_id("resolved_app")
    def test_flag_route_works_for_application_with_latest_resolved_flag(
        self,
        request,
        assess_test_client,
        mock_get_flags,
        mock_get_available_teams,
        mock_get_flag,
        mock_get_assessor_tasklist_state,
        mock_get_sub_criteria_banner_state,
        mock_get_fund,
        mock_get_funds,
        mock_get_round,
        mock_get_application_metadata,
        mock_competed_cof_fund,
    ):
        marker = request.node.get_closest_marker("application_id")
        application_id = marker.args[0]
        token = create_valid_token(test_lead_assessor_claims)
        assess_test_client.set_cookie("fsd_user_token", token)

        response = assess_test_client.get(f"assess/flag/{application_id}")

        assert response.status_code == 200

    @pytest.mark.application_id("stopped_app")
    def test_application_route_should_show_stopped_flag(
        self,
        request,
        assess_test_client,
        mock_get_assessor_tasklist_state,
        mock_get_fund,
        mock_get_funds,
        mock_get_application_metadata,
        mock_get_round,
        mock_get_flags,
        mock_get_qa_complete,
        mock_get_bulk_accounts,
        mock_get_associated_tags_for_application,
        mocker,
        mock_get_scoring_system,
        mock_get_calculate_overall_score_percentage,
        mock_competed_cof_fund,
    ):
        marker = request.node.get_closest_marker("application_id")
        application_id = marker.args[0]
        token = create_valid_token(test_lead_assessor_claims)
        assess_test_client.set_cookie("fsd_user_token", token)

        response = assess_test_client.get(f"assess/application/{application_id}")

        assert 200 == response.status_code, "Wrong status code on response"
        soup = BeautifulSoup(response.data, "html.parser")
        assert (
            soup.find("h1", class_="assessment-alert__heading").string.strip()
            == "Flagged for test_team - Assessment stopped"
        )
        assert b"Lead User (Lead assessor) lead@test.com" in response.data
        assert b"20 February 2023 at 12:00" in response.data

    @pytest.mark.application_id("resolved_app")
    def test_application_route_should_show_resolved_flag(
        self,
        request,
        assess_test_client,
        mock_get_assessor_tasklist_state,
        mock_get_fund,
        mock_get_funds,
        mock_get_application_metadata,
        mock_get_round,
        mock_get_flags,
        mock_get_qa_complete,
        mock_get_bulk_accounts,
        mock_get_comments,
        mock_get_associated_tags_for_application,
        mocker,
        mock_get_scoring_system,
        mock_get_calculate_overall_score_percentage,
        mock_competed_cof_fund,
    ):
        mocker.patch(
            "pre_award.apply.default.application_routes.get_fund_and_round",
            return_value=(Fund.from_dict(TEST_FUNDS_DATA[0]), TEST_ROUNDS_DATA[0]),
        )
        fund_args = {
            "name": "Testing Fund",
            "short_name": "",
            "description": "",
            "welsh_available": True,
            "title": "Test Fund by ID",
            "id": "222",
            "funding_type": "COMPETITIVE",
        }
        mocker.patch(
            "pre_award.apply.default.data.get_data",
            return_value=fund_args,
        )
        mocker.patch(
            "pre_award.apply.helpers.get_application_data",
            return_value=TEST_APPLICATION_SUMMARIES[0],
        )
        marker = request.node.get_closest_marker("application_id")
        application_id = marker.args[0]
        token = create_valid_token(test_lead_assessor_claims)
        assess_test_client.set_cookie("fsd_user_token", token)

        response = assess_test_client.get(f"assess/application/{application_id}")

        assert response.status_code == 200
        assert b"Remove flag" not in response.data
        assert b"Flagged for test_team resolved" in response.data
        assert b"Resolve flag action" in response.data
        assert b"Reason" in response.data

    @pytest.mark.application_id("resolved_app")
    def test_flag_route_submit_flag(
        self,
        assess_test_client,
        mocker,
        mock_get_assessor_tasklist_state,
        mock_get_available_teams,
        mock_get_fund,
        mock_get_round,
        mock_get_funds,
        mock_submit_flag,
        mock_get_application_metadata,
        mock_get_sub_criteria_banner_state,
    ):
        token = create_valid_token(test_lead_assessor_claims)
        assess_test_client.set_cookie("fsd_user_token", token)
        session["csrf_token"] = "test"

        response = assess_test_client.post(
            "assess/flag/resolved_app",
            data={
                "justification": "Test justification",
                "section": ["test_sub_criteria_id"],
                "teams_available": "Team A",
            },
        )

        assert response.status_code == 302
        assert response.headers["Location"] == "/assess/application/resolved_app"

    @pytest.mark.application_id("flagged_qa_completed_app")
    @pytest.mark.flag_id("flagged_qa_completed_app")
    def test_flag_route_get_resolve_flag(
        self,
        request,
        assess_test_client,
        mock_get_flags,
        mock_get_flag,
        mock_get_assessor_tasklist_state,
        mock_get_sub_criteria_banner_state,
        mock_get_fund,
        mock_get_funds,
        mock_get_round,
        mock_get_application_metadata,
        mock_competed_cof_fund,
    ):
        token = create_valid_token(test_lead_assessor_claims)
        assess_test_client.set_cookie("fsd_user_token", token)
        application_id = request.node.get_closest_marker("application_id").args[0]
        flag_id = request.node.get_closest_marker("flag_id").args[0]
        response = assess_test_client.get(
            f"assess/resolve_flag/{application_id}?flag_id={flag_id}",
        )

        assert response.status_code == 200
        assert b"Resolve flag" in response.data
        assert b"Query resolved" in response.data
        assert b"Stop assessment" in response.data
        assert b"Reason" in response.data
        soup = BeautifulSoup(response.data, "html.parser")
        assert soup.title.string == "Resolve flag – Assessment Hub – GOV.UK"

    @pytest.mark.mock_parameters(
        {
            "flag": Flag.from_dict(
                {
                    "application_id": "flagged_app",
                    "latest_status": "RESOLVED",
                    "latest_allocation": None,
                    "id": "flagged_app",
                    "sections_to_flag": ["Test section"],
                    "field_ids": [],
                    "is_change_request": False,
                    "updates": [
                        {
                            "id": "316f607a-03b7-4592-b927-5021a28b7d6a",
                            "user_id": "test_user_lead_assessor",
                            "date_created": "2023-01-01T00:00:00",
                            "justification": "Checked with so and so.",
                            "status": "RESOLVED",
                            "allocation": None,
                        }
                    ],
                }
            )
        }
    )
    @pytest.mark.submit_flag_paths(["pre_award.assess.flagging.helpers.submit_flag"])
    @pytest.mark.application_id("flagged_app")
    @pytest.mark.flag_id("flagged_app")
    def test_post_resolved_flag(
        self,
        request,
        assess_test_client,
        mocker,
        mock_get_flags,
        mock_get_flag,
        mock_get_assessor_tasklist_state,
        mock_get_fund,
        mock_get_funds,
        mock_get_round,
        mock_get_application_metadata,
        mock_submit_flag,
    ):
        token = create_valid_token(test_lead_assessor_claims)
        assess_test_client.set_cookie("fsd_user_token", token)
        application_id = request.node.get_closest_marker("application_id").args[0]
        flag_id = request.node.get_closest_marker("flag_id").args[0]

        response = assess_test_client.post(
            f"assess/resolve_flag/{application_id}?flag_id={flag_id}",
            data={
                "resolution_flag": "RESOLVED",
                "justification": "Checked with so and so.",
            },
        )

        assert response.status_code == 302
        assert response.headers["Location"] == f"/assess/application/{application_id}"

    @pytest.mark.application_id("stopped_app")
    @pytest.mark.flag_id("stopped_app")
    def test_flag_route_get_continue_application(
        self,
        request,
        assess_test_client,
        mock_get_flags,
        mock_get_flag,
        mock_get_sub_criteria_banner_state,
        mock_get_assessor_tasklist_state,
        mock_get_round,
        mock_get_fund,
        mock_get_funds,
        mock_get_application_metadata,
        mock_competed_cof_fund,
    ):
        application_id = request.node.get_closest_marker("application_id").args[0]
        flag_id = request.node.get_closest_marker("flag_id").args[0]
        token = create_valid_token(test_lead_assessor_claims)
        assess_test_client.set_cookie("fsd_user_token", token)

        response = assess_test_client.get(
            f"/assess/continue_assessment/{application_id}?flag_id={flag_id}",
        )

        assert response.status_code == 200
        assert b"Continue assessment" in response.data
        assert b"Reason for continuing assessment" in response.data
        assert b"Project In prog and Stop" in response.data

    @pytest.mark.mock_parameters(
        {
            "flag": Flag.from_dict(
                {
                    "application_id": "stopped_app",
                    "latest_status": "RESOLVED",
                    "latest_allocation": None,
                    "id": "stopped_app",
                    "sections_to_flag": ["Test section"],
                    "field_ids": [],
                    "is_change_request": False,
                    "updates": [
                        {
                            "id": "316f607a-03b7-4592-b927-5021a28b7d6a",
                            "user_id": "test_user_lead_assessor",
                            "date_created": "2023-01-01T00:00:00",
                            "justification": "Checked with so and so.",
                            "status": "RESOLVED",
                            "allocation": None,
                        }
                    ],
                }
            )
        }
    )
    @pytest.mark.submit_flag_paths(["pre_award.assess.flagging.helpers.submit_flag"])
    @pytest.mark.application_id("stopped_app")
    @pytest.mark.flag_id("stopped_app")
    def test_post_continue_application(
        self,
        request,
        assess_test_client,
        mocker,
        mock_get_funds,
        mock_get_application_metadata,
        mock_get_fund,
        mock_get_flag,
        mock_get_round,
        mock_get_assessor_tasklist_state,
        mock_submit_flag,
    ):
        flag_id = request.node.get_closest_marker("flag_id").args[0]
        token = create_valid_token(test_lead_assessor_claims)
        assess_test_client.set_cookie("fsd_user_token", token)

        response = assess_test_client.post(
            f"assess/continue_assessment/stopped_app?flag_id={flag_id}",
            data={
                "reason": "We should continue the application.",
            },
        )

        assert response.status_code == 302
        assert response.headers["Location"] == "/assess/application/stopped_app"

    @pytest.mark.application_id("flagged_qa_completed_app")
    def test_qa_complete_flag_displayed(
        self,
        request,
        assess_test_client,
        mock_get_round,
        mock_get_assessor_tasklist_state,
        mock_get_flags,
        mock_get_qa_complete,
        mock_get_bulk_accounts,
        mock_get_sub_criteria_banner_state,
        mock_get_fund,
        mock_get_funds,
        mock_get_application_metadata,
        mock_get_associated_tags_for_application,
        mocker,
        mock_get_scoring_system,
        mock_get_calculate_overall_score_percentage,
        mock_competed_cof_fund,
    ):
        token = create_valid_token(test_lead_assessor_claims)
        assess_test_client.set_cookie("fsd_user_token", token)
        application_id = request.node.get_closest_marker("application_id").args[0]
        response = assess_test_client.get(
            f"assess/application/{application_id}",
        )

        assert response.status_code == 200
        assert b"Marked as QA complete" in response.data
        assert b"20 February 2023 at 12:00" in response.data

    @pytest.mark.application_id("flagged_qa_completed_app")
    def test_qa_completed_flagged_application(
        self,
        request,
        assess_test_client,
        mock_get_assessor_tasklist_state,
        mock_get_fund,
        mock_get_funds,
        mock_get_application_metadata,
        mock_get_round,
        mock_get_flags,
        mock_get_qa_complete,
        mock_get_bulk_accounts,
        mock_get_associated_tags_for_application,
        mocker,
        mock_get_scoring_system,
        mock_get_calculate_overall_score_percentage,
        mock_competed_cof_fund,
    ):
        token = create_valid_token(test_lead_assessor_claims)
        assess_test_client.set_cookie("fsd_user_token", token)

        marker = request.node.get_closest_marker("application_id")
        application_id = marker.args[0]

        response = assess_test_client.get(
            f"assess/application/{application_id}",
        )

        assert response.status_code == 200
        assert b"Marked as QA complete" in response.data
        assert b"19 February 2023 at 12:00" in response.data
        assert b"Section(s) flagged" in response.data
        assert b"Reason" in response.data
        assert b"Resolve flag" in response.data

    @pytest.mark.mock_parameters(
        {
            "fund_short_name": "COF",
            "round_short_name": "TR",
            "expected_search_params": {
                "search_term": "",
                "search_in": "project_name,short_id",
                "assigned_to": "ALL",
                "asset_type": "ALL",
                "status": "ALL",
                "filter_by_tag": "ALL",
            },
        }
    )
    def test_route_fund_dashboard_shows_flagged(
        self,
        request,
        assess_test_client,
        mock_get_funds,
        mock_get_fund,
        mock_get_round,
        mock_get_application_overviews,
        mock_get_users_for_fund,
        mock_get_assessment_progress,
        mock_get_active_tags_for_fund_round,
        mock_get_tag_types,
        mock_competed_cof_fund,
    ):
        assess_test_client.set_cookie(
            "fsd_user_token",
            create_valid_token(fund_specific_claim_map["COF"]["ASSESSOR"]),
        )

        params = request.node.get_closest_marker("mock_parameters").args[0]
        fund_short_name = params["fund_short_name"]
        round_short_name = params["round_short_name"]
        response = assess_test_client.get(
            f"/assess/fund_dashboard/{fund_short_name}/{round_short_name}",
            follow_redirects=True,
        )

        assert 200 == response.status_code, "Wrong status code on response"

        assert b"stopped-tag" in response.data, "Stopped Flag is not displaying"

        assert b"flagged-tag" in response.data, "Flagged Flag is not displaying"

        assert b"Resolved" not in response.data, "Resolved Flag is displaying and should not"

        assert 200 == response.status_code, "Wrong status code on response"
        soup = BeautifulSoup(response.data, "html.parser")
        assert soup.title.string == "Team dashboard – Assessment Hub – GOV.UK", (
            "Response does not contain expected heading"
        )

    @pytest.mark.application_id("resolved_app")
    @pytest.mark.sub_criteria_id("test_sub_criteria_id")
    def test_page_title_subcriteria_theme_match(
        self,
        request,
        assess_test_client,
        mock_get_sub_criteria,
        mock_get_fund,
        mock_get_funds,
        mock_get_round,
        mock_get_application_metadata,
        mock_get_comments,
        mock_get_sub_criteria_theme,
        mock_get_assessor_tasklist_state,
        mock_get_bulk_accounts,
        mock_get_assessment_flags,
        mock_competed_cof_fund,
    ):
        soup = get_subcriteria_soup(request, assess_test_client)
        assert soup.title.string == (
            "test_theme_name – test_sub_criteria – Project In prog and Res – Assessment Hub – GOV.UK"
        )

    @pytest.mark.application_id("uncompeted_app")
    @pytest.mark.fund_id("UNCOMPETED_FUND")
    @pytest.mark.sub_criteria_id("test_uncomp_sub_criteria_id")
    def test_uncompeted_fund_subcriteria(
        self,
        request,
        assess_test_client,
        mock_get_sub_criteria,
        mock_get_fund,
        mock_get_funds,
        mock_get_round,
        mock_get_application_metadata,
        mock_get_sub_criteria_theme,
        mock_get_assessor_tasklist_state,
        mock_get_bulk_accounts,
        mock_get_assessment_flags,
        mock_uncompeted_pfn_fund,
    ):
        soup = get_subcriteria_soup(request, assess_test_client)
        # Check that the expected text exists in a specified paragraph element.
        assert (
            "Review the applicant's responses and 'Approve and score' when you're ready."
            in soup.findAll("p", class_="govuk-body")[4].text
        )

    @pytest.mark.application_id("resolved_app")
    @pytest.mark.fund_id("DPIF")
    @pytest.mark.sub_criteria_id("test_sub_criteria_id")
    def test_dpif_subcriteria(
        self,
        request,
        assess_test_client,
        mock_get_sub_criteria,
        mock_get_fund,
        mock_get_funds,
        mock_get_round,
        mock_get_application_metadata,
        mock_get_flags,
        mock_get_comments,
        mock_get_sub_criteria_theme,
        mock_get_assessor_tasklist_state,
        mock_get_bulk_accounts,
        mock_get_assessment_flags,
    ):
        # Mocking fsd-user-token cookie
        token = create_valid_token(test_dpif_commenter_claims)
        assess_test_client.set_cookie("fsd_user_token", token)

        application_id = request.node.get_closest_marker("application_id").args[0]
        sub_criteria_id = request.node.get_closest_marker("sub_criteria_id").args[0]

        response = assess_test_client.get(
            f"/assess/application_id/{application_id}/sub_criteria_id/{sub_criteria_id}"  # noqa
        )
        soup = BeautifulSoup(response.data, "html.parser")
        # Verify that the text specific to uncompeted journey is not present
        assert (
            "Review the applicant's responses and 'Accept all responses' when you're ready."
            not in soup.findAll("p", class_="govuk-body")[4].text
        )

    @pytest.mark.application_id("resolved_app")
    def test_get_docs_for_download(
        self,
        assess_test_client,
        request,
        mock_get_assessor_tasklist_state,
        mock_get_fund,
        mock_get_funds,
        mock_get_application_metadata,
        mock_get_flags,
        mock_get_round,
        templates_rendered,
        mock_get_associated_tags_for_application,
        mocker,
        mock_competed_cof_fund,
    ):
        marker = request.node.get_closest_marker("application_id")
        application_id = marker.args[0]

        token = create_valid_token(test_lead_assessor_claims)
        assess_test_client.set_cookie("fsd_user_token", token)
        mocker.patch(
            "pre_award.assess.assessments.routes.get_application_json",
            return_value={"jsonb_blob": "mock"},
        )
        with mock.patch(
            "pre_award.assess.assessments.routes.get_files_for_application_upload_fields",
            return_value=[
                ("sample1.doc", "mock/url/for/get/file"),
                ("sample2.doc", "mock/url/for/get/file"),
            ],
        ):
            response = assess_test_client.get(f"/assess/application/{application_id}/export")
            assert 200 == response.status_code
            assert 1 == len(templates_rendered)
            rendered_template = templates_rendered[0]
            assert "assessments/contract_downloads.html" == rendered_template[0].name
            assert application_id == rendered_template[1]["application_id"]
            assert b"sample1.doc" in response.data
            assert b"sample2.doc" in response.data

    def test_download_q_and_a(
        self,
        assess_test_client,
        mock_get_fund,
        mock_get_round,
        mock_get_funds,
        mock_get_application_metadata,
        mock_get_application_json,
        mocks_for_file_export_download,
    ):
        token = create_valid_token(test_lead_assessor_claims)
        assess_test_client.set_cookie("fsd_user_token", token)
        response = assess_test_client.get("/assess/application/test_app_id/export/test_short_id/answers.txt")
        sample_1 = "Project information"
        sample_2 = "Q) Have you been given"
        assert response.status_code == 200
        assert sample_1 in response.text
        assert sample_2 in response.text

    @pytest.mark.application_id("uncompeted_app")
    @pytest.mark.fund_id("UNCOMPETED_FUND")
    def test_change_received_notification_banner(
        self,
        assess_test_client,
        mock_get_fund,
        mock_get_funds,
        mock_get_round,
        mock_get_application_metadata,
        mock_get_assessor_tasklist_state,
        mock_get_scoring_system,
        mock_get_calculate_overall_score_percentage,
        mock_competed_cof_fund,
    ):
        response = assess_test_client.get("/assess/application/uncompeted_app")
        assert response.status_code == 200
        soup = BeautifulSoup(response.data, "html.parser")
        assert any(
            "The applicant has made changes following your change request." in p.text
            for p in soup.find_all("p", class_="govuk-notification-banner__heading")
        ), "Text does not match"

    def test_get_file_with_short_id(
        self,
        assess_test_client,
        mocker,
        mock_get_funds,
        mock_get_fund,
        mock_get_application_metadata,
    ):
        token = create_valid_token(test_lead_assessor_claims)
        assess_test_client.set_cookie("fsd_user_token", token)
        mocker.patch(
            "pre_award.assess.assessments.routes.get_file_for_download_from_aws",
            return_value=("some file contents", "mock_mimetype"),
        )
        with mock.patch("pre_award.assess.assessments.routes.download_file", return_value="") as mock_download_file:
            assess_test_client.get("/assess/application/abc123/export/business_plan.txt?short_id=QWERTY")  # noqa
            mock_download_file.assert_called_once_with(
                "some file contents",
                "mock_mimetype",
                "QWERTY_business_plan.txt",
            )

    def test_get_file_without_short_id(
        self,
        assess_test_client,
        mocker,
        mock_get_funds,
        mock_get_fund,
        mock_get_application_metadata,
    ):
        token = create_valid_token(test_lead_assessor_claims)
        assess_test_client.set_cookie("fsd_user_token", token)
        mocker.patch(
            "pre_award.assess.assessments.routes.get_file_for_download_from_aws",
            return_value=("some file contents", "mock_mimetype"),
        )
        with mock.patch("pre_award.assess.assessments.routes.download_file", return_value="") as mock_download_file:
            assess_test_client.get("/assess/application/abc123/export/business_plan.txt")
            mock_download_file.assert_called_once_with("some file contents", "mock_mimetype", "business_plan.txt")

    def test_get_file(self, assess_test_client):
        from pre_award.assess.assessments.routes import download_file

        response = download_file("file_data", "text/plain", "file_name.abc")
        assert "text/plain" in response.content_type
        assert "attachment;filename=file_name.abc" == response.headers.get("Content-Disposition")

    @pytest.mark.application_id("resolved_app")
    @pytest.mark.sub_criteria_id("test_sub_criteria_id")
    def test_change_request_success_page(
        self,
        assess_test_client,
        request,
        mock_get_sub_criteria,
        mock_get_fund,
        mock_get_funds,
        mock_get_round,
        mock_get_application_metadata,
        mock_get_assessor_tasklist_state,
        mock_competed_cof_fund,
    ):
        application_id = request.node.get_closest_marker("application_id").args[0]
        sub_criteria_id = request.node.get_closest_marker("sub_criteria_id").args[0]

        token = create_valid_token(test_lead_assessor_claims)
        assess_test_client.set_cookie("fsd_user_token", token)

        response = assess_test_client.get(
            f"/assess/application_id/{application_id}/sub_criteria_id/{sub_criteria_id}/theme_id/test_theme_id/request_change/success"
        )
        assert 200 == response.status_code
        assert b"Your request for changes has been sent" in response.data
        assert b"Back to application" in response.data

    @pytest.mark.application_id("resolved_app")
    @pytest.mark.sub_criteria_id("test_sub_criteria_id")
    def test_submit_change_request(
        self,
        assess_test_client,
        request,
        mocker,
        mock_get_sub_criteria,
        mock_get_sub_criteria_theme,
        mock_get_fund,
        mock_get_funds,
        mock_get_round,
        mock_get_application_metadata,
        mock_get_assessor_tasklist_state,
        mock_competed_cof_fund,
    ):
        application_id = request.node.get_closest_marker("application_id").args[0]
        sub_criteria_id = request.node.get_closest_marker("sub_criteria_id").args[0]

        token = create_valid_token(test_lead_assessor_claims)
        assess_test_client.set_cookie("fsd_user_token", token)
        response = assess_test_client.get(
            f"/assess/application_id/{application_id}/sub_criteria_id/{sub_criteria_id}/theme_id/test_theme_id/request_change"
        )
        assert 200 == response.status_code
        assert b"What changes are needed?" in response.data

        mock_submit_response = {
            "application_id": application_id,
            "flag_type": "RAISED",
            "field_ids": ["JCACTy"],
            "section": [sub_criteria_id],
            "is_change_request": True,
        }

        submit_mock = mocker.patch(
            "pre_award.assess.assessments.routes.submit_change_request", return_value=mock_submit_response
        )
        mocker.patch("pre_award.assess.assessments.routes.is_first_change_request_for_date", return_value=True)
        mocker.patch("pre_award.assess.assessments.routes.update_assessment_record_status")
        mocker.patch("pre_award.assess.assessments.routes.notify_applicant_changes_requested")
        mocker.patch("pre_award.assess.assessments.routes.mark_application_with_requested_changes")
        post_data = {"field_ids": ["JCACTy"], "reason_JCACTy": "testing"}

        response = assess_test_client.post(
            f"/assess/application_id/{application_id}/sub_criteria_id/{sub_criteria_id}/theme_id/test_theme_id/request_change",
            data=post_data,
            follow_redirects=True,
        )
        submit_mock.assert_called_once_with(
            application_id=application_id,
            flag_type="RAISED",
            user_id="lead",
            justification="testing",
            field_ids=["JCACTy"],
            section=[sub_criteria_id],
            is_change_request=True,
        )
        assert 200 == response.status_code
        assert b"Your request for changes has been sent" in response.data

    @pytest.mark.application_id("resolved_app")
    @pytest.mark.sub_criteria_id("test_sub_criteria_id")
    @pytest.mark.parametrize("sub_criteria_status", [Status.CHANGE_REQUESTED.name])
    def test_prevent_acceptance_and_request_change_when_sub_status_change_requested(
        self,
        sub_criteria_status,
        assess_test_client,
        request,
        mock_get_sub_criteria,
        mock_get_sub_criteria_theme,
        mock_get_fund,
        mock_get_funds,
        mock_get_round,
        mock_get_application_metadata,
        mock_get_assessor_tasklist_state,
        mock_uncompeted_pfn_fund,
        expect_flagging,
    ):
        application_id = request.node.get_closest_marker("application_id").args[0]
        sub_criteria_id = request.node.get_closest_marker("sub_criteria_id").args[0]

        token = create_valid_token(test_lead_assessor_claims)
        assess_test_client.set_cookie("fsd_user_token", token)
        mock_get_assessor_tasklist_state[0].return_value["criterias"][0]["sub_criterias"][0]["status"] = (
            sub_criteria_status
        )

        mock_get_assessor_tasklist_state[1].return_value.is_qa_complete = False

        for criteria in mock_get_assessor_tasklist_state[1].return_value.criterias:
            for sub in criteria.sub_criterias:
                if sub.id == sub_criteria_id:
                    sub.status = "CHANGE_REQUESTED"

        post_data = {"field_ids": ["JCACTy"], "reason_JCACTy": "testing"}

        response = assess_test_client.post(
            f"/assess/application_id/{application_id}/sub_criteria_id/{sub_criteria_id}/theme_id/test_theme_id/request_change",
            data=post_data,
            follow_redirects=True,
        )
        assert 403 == response.status_code
        assert b"Access Denied" in response.data

        response = assess_test_client.get(
            f"/assess/application_id/{application_id}/sub_criteria_id/{sub_criteria_id}/score"  # noqa
        )
        assert 403 == response.status_code
        assert b"Access Denied" in response.data

    @pytest.mark.application_id("resolved_app")
    @pytest.mark.sub_criteria_id("test_sub_criteria_id")
    @pytest.mark.parametrize("sub_criteria_status", [Status.COMPLETED.name])
    def test_prevent_acceptance_and_request_change_when_is_qa_complete(
        self,
        sub_criteria_status,
        assess_test_client,
        request,
        mock_get_sub_criteria,
        mock_get_sub_criteria_theme,
        mock_get_fund,
        mock_get_funds,
        mock_get_round,
        mock_get_application_metadata,
        mock_get_assessor_tasklist_state,
        mock_uncompeted_pfn_fund,
        expect_flagging,
    ):
        application_id = request.node.get_closest_marker("application_id").args[0]
        sub_criteria_id = request.node.get_closest_marker("sub_criteria_id").args[0]

        token = create_valid_token(test_lead_assessor_claims)
        assess_test_client.set_cookie("fsd_user_token", token)
        mock_get_assessor_tasklist_state[0].return_value["criterias"][0]["sub_criterias"][0]["status"] = (
            sub_criteria_status
        )
        post_data = {"field_ids": ["JCACTy"], "reason_JCACTy": "testing"}

        response = assess_test_client.post(
            f"/assess/application_id/{application_id}/sub_criteria_id/{sub_criteria_id}/theme_id/test_theme_id/request_change",
            data=post_data,
            follow_redirects=True,
        )
        assert 403 == response.status_code
        assert b"Access Denied" in response.data

        response = assess_test_client.get(
            f"/assess/application_id/{application_id}/sub_criteria_id/{sub_criteria_id}/score"  # noqa
        )
        assert 403 == response.status_code
        assert b"Access Denied" in response.data


@pytest.mark.parametrize(
    "file_extension, content_type",
    [
        ("txt", "text/plain; charset=utf-8"),
        ("csv", "text/csv; charset=utf-8"),
    ],
)
def test_download_application_answers(
    assess_test_client,
    mock_get_funds,
    mock_get_application_metadata,
    mock_get_fund,
    mock_get_round,
    mock_get_application_json,
    file_extension,
    content_type,
    mocks_for_file_export_download,
):
    token = create_valid_token(test_lead_assessor_claims)
    assess_test_client.set_cookie("fsd_user_token", token)
    url = f"/assess/application/123/export/456/answers.{file_extension}"
    response = assess_test_client.get(url)

    assert response.status_code == 200

    assert response.headers["Content-Type"] == content_type
    assert response.headers["Content-Disposition"] == f"attachment;filename=456_answers.{file_extension}"


def test_download_application_answers_invalid_file_type(
    assess_test_client,
    mock_get_funds,
    mock_get_application_metadata,
    mock_get_round,
    mock_get_fund,
    mock_get_application_json,
    mocks_for_file_export_download,
):
    token = create_valid_token(test_lead_assessor_claims)
    assess_test_client.set_cookie("fsd_user_token", token)
    response = assess_test_client.get("/assess/application/123/export/456/answers.invalid")
    assert response.status_code == 404
