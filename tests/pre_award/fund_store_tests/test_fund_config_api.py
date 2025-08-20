"""
Tests for fund config API endpoint
"""

from unittest.mock import patch


def test_fund_config_endpoint_missing_data(flask_test_client, app):
    """Test endpoint with missing required fields"""
    app.config["FLASK_ENV"] = "development"

    # Test with missing required field
    response = flask_test_client.post("/fund/import-config", json={"fund_config": {"short_name": "TEST"}})
    assert response.status_code == 400
    assert "Missing required field: sections_config" in response.get_json()["error"]


def test_fund_config_endpoint_success(flask_test_client, app):
    """Test successful fund config processing"""
    app.config["FLASK_ENV"] = "development"

    test_data = {
        "sections_config": [],
        "fund_config": {"short_name": "TEST"},
        "round_config": [{"short_name": "r1", "base_path": 1001}],
        "base_path": "test_path",
    }

    with (
        patch("pre_award.fund_store.api.routes.transform_fund_configuration") as mock_convert,
        patch("pre_award.fund_store.api.routes.process_fund_config") as mock_process,
    ):
        mock_convert.return_value = {"TEST": {"short_name": "TEST"}}
        mock_process.return_value = {"success": True, "message": "Fund config processed successfully"}

        response = flask_test_client.post("/fund/import-config", json=test_data)

        assert response.status_code == 201
        response_data = response.get_json()
        assert "Fund config processed successfully" in response_data["message"]
        mock_convert.assert_called_once_with(test_data)
        mock_process.assert_called_once_with({"short_name": "TEST"})


def test_fund_config_endpoint_service_error(flask_test_client, app):
    """Test handling of service errors"""
    app.config["FLASK_ENV"] = "development"

    test_data = {
        "sections_config": [],
        "fund_config": {"short_name": "TEST"},
        "round_config": [{"short_name": "r1", "base_path": 1001}],
        "base_path": "test_path",
    }

    with (
        patch("pre_award.fund_store.api.routes.transform_fund_configuration") as mock_convert,
        patch("pre_award.fund_store.api.routes.process_fund_config") as mock_process,
    ):
        mock_convert.return_value = {"TEST": {"short_name": "TEST"}}
        mock_process.return_value = {"success": False, "message": "Database error"}

        response = flask_test_client.post("/fund/import-config", json=test_data)

        assert response.status_code == 500
        assert "Database error" in response.get_json()["error"]
