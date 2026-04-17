from unittest.mock import Mock

import pytest
import requests
from flask import Flask

from pre_award.assess.services.data_services import (
    get_all_fund_short_codes,
    get_application_overviews,
    get_comments,
    get_data,
    get_fund,
    get_round,
)
from pre_award.assess.services.models.fund import Fund
from tests.pre_award.assess_tests.api_data.test_data import mock_api_results


class TestDataOperations:
    test_app = Flask("app")

    def test_get_fund(self, mocker):
        mock_fund_result = mock_api_results["fund_store/funds/{fund_id}"]
        get_data_mock = mocker.patch(
            "pre_award.assess.services.data_services.get_data",
            return_value=mock_fund_result,
        )
        arg = "test-fund"
        with self.test_app.app_context():
            fund = get_fund(arg)
        assert fund, "No fund returned"
        assert "Funding Service Design Unit Test Fund" == fund.name, "Wrong fund title"
        assert arg in get_data_mock.call_args.args[0]

    def test_get_round(self, mocker):
        mock_round_result = mock_api_results["fund_store/funds/{fund_id}/rounds/{round_id}"]
        get_data_mock = mocker.patch(
            "pre_award.assess.services.data_services.get_data",
            return_value=mock_round_result,
        )
        args = ("test-fund", "test-round")
        with self.test_app.app_context():
            round = get_round(*args)
        assert round, "No round returned"
        assert "Test round" == round.title, "Wrong round title"
        assert all(arg in get_data_mock.call_args.args[0] for arg in args)

    def test_get_application_overviews(self, mocker):
        mock_fund_result = mock_api_results["assessment_store/application_overviews/{fund_id}/{round_id}?"]
        get_data_mock = mocker.patch(
            "pre_award.assess.services.data_services.get_data",
            return_value=mock_fund_result,
        )

        with self.test_app.app_context():
            params = {
                "search_term": "",
                "search_in": "project_name,short_id",
                "asset_type": "ALL",
                "status": "ALL",
                "local_authority": "ALL",
            }
            args = ("test-fund", "test-round")
            result = get_application_overviews(*args, params)
        assert result, "No result returned"
        assert 4 == len(result), "wrong number of application overviews"
        assert all(arg in get_data_mock.call_args.args[0] for arg in args)

    def test_get_application_overviews_search_with_params(self, mocker):
        mock_overview_result = mock_api_results[
            "assessment_store/application_overviews/{fund_id}/{round_id}?"
            "search_term=Project+S&search_in=project_name%2Cshort_id&"
            "asset_type=gallery&local_authority=wokefield&status=STOPPED"
        ]
        get_data_mock = mocker.patch(
            "pre_award.assess.services.data_services.get_data",
            return_value=mock_overview_result,
        )

        with self.test_app.app_context():
            params = {
                "search_term": "Project S",
                "search_in": "project_name,short_id",
                "asset_type": "ALL",
                "status": "ALL",
                "local_authority": "ALL",
            }
            args = ("test-fund", "test-round")
            result = get_application_overviews(*args, params)
        assert result, "No result returned"
        assert result[0]["short_id"] == "FS"
        assert result[0]["project_name"] == "Project In prog and Stop"
        assert 1 == len(result), "wrong number of application overviews"
        assert all(arg in get_data_mock.call_args.args[0] for arg in args)

    def test_get_comments(self, mocker):
        mock_comments_result = mock_api_results["assessment_store/comment?"]
        get_data_mock = mocker.patch(
            "pre_award.assess.services.data_services.get_data",
            return_value=mock_comments_result,
        )
        args = ("resolved_app", "test_sub_criteria_id", "test_theme_id")
        with self.test_app.app_context():
            comments = get_comments(*args)
        assert 5 == len(comments), "wrong number of comments"
        assert all(arg in get_data_mock.call_args.args[0] for arg in args)


@pytest.mark.parametrize(
    "mock_get_all_funds_response,exp_result",
    [
        (
            [Fund(short_name="F1", id="id", description="hello fund", name="Fund 1")],
            {"F1"},
        ),
        (
            [
                Fund(short_name="F1", id="id", description="hello fund", name="Fund 1"),
                Fund(short_name="F2", id="id", description="hello fund", name="Fund 2"),
            ],
            {"F1", "F2"},
        ),
        ({}, {}),
    ],
)
def test_get_all_fund_short_codes(mock_get_all_funds_response, exp_result, mocker):
    mocker.patch(
        "pre_award.assess.services.data_services.get_funds",
        return_value=mock_get_all_funds_response,
    )
    result = get_all_fund_short_codes()
    assert result == exp_result


_ENDPOINT = "http://example.test/x"


def _json_response(payload, status=200):
    response = Mock()
    response.status_code = status
    response.headers = {"Content-Type": "application/json"}
    response.json.return_value = payload
    return response


class TestGetDataRetry:
    test_app = Flask("app")

    def test_returns_json_on_first_success(self, mocker):
        get_mock = mocker.patch(
            "pre_award.assess.services.data_services.requests.get",
            return_value=_json_response({"ok": True}),
        )
        with self.test_app.app_context():
            assert get_data(_ENDPOINT) == {"ok": True}
        assert get_mock.call_count == 1

    @pytest.mark.parametrize("failures_before_success", [1, 2])
    def test_retries_connection_error_until_success(self, mocker, failures_before_success):
        get_mock = mocker.patch(
            "pre_award.assess.services.data_services.requests.get",
            side_effect=[requests.exceptions.ConnectionError("stale")] * failures_before_success
            + [_json_response({"ok": True})],
        )
        with self.test_app.app_context():
            assert get_data(_ENDPOINT) == {"ok": True}
        assert get_mock.call_count == failures_before_success + 1

    def test_returns_none_after_three_connection_errors(self, mocker):
        get_mock = mocker.patch(
            "pre_award.assess.services.data_services.requests.get",
            side_effect=requests.exceptions.ConnectionError("always"),
        )
        with self.test_app.app_context():
            assert get_data(_ENDPOINT) is None
        assert get_mock.call_count == 3

    def test_does_not_retry_other_request_exceptions(self, mocker):
        get_mock = mocker.patch(
            "pre_award.assess.services.data_services.requests.get",
            side_effect=requests.exceptions.ReadTimeout("read timed out"),
        )
        with self.test_app.app_context():
            assert get_data(_ENDPOINT) is None
        assert get_mock.call_count == 1

    def test_payload_is_preserved_across_retry(self, mocker):
        get_mock = mocker.patch(
            "pre_award.assess.services.data_services.requests.get",
            side_effect=[
                requests.exceptions.ConnectionError("stale"),
                _json_response({"ok": True}),
            ],
        )
        with self.test_app.app_context():
            assert get_data(_ENDPOINT, {"a": "b"}) == {"ok": True}
        assert get_mock.call_args_list[0] == get_mock.call_args_list[1]
