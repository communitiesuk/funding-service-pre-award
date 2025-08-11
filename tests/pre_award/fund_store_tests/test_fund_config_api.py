"""
Tests for fund config API endpoint
"""

from unittest.mock import patch


def test_fund_config_endpoint_missing_data(flask_test_client, app):
    """Test endpoint with missing required fields"""
    app.config["FLASK_ENV"] = "development"

    # Test with missing required field
    response = flask_test_client.post("/fund/fund-config", json={"short_name": "TEST"})
    assert response.status_code == 400
    assert "Missing required field: rounds" in response.get_json()["error"]


def test_fund_config_endpoint_success(flask_test_client, app):
    """Test successful fund config processing"""
    app.config["FLASK_ENV"] = "development"

    test_data = {"short_name": "TEST", "rounds": {"r1": {"short_name": "r1", "sections_config": [], "base_path": 1001}}}

    with patch("pre_award.fund_store.api.routes.process_fund_config") as mock_process:
        mock_process.return_value = {"success": True, "message": "Success"}

        response = flask_test_client.post("/fund/fund-config", json=test_data)

        assert response.status_code == 201
        response_data = response.get_json()
        assert "Success" in response_data["message"]
        assert "fund_short_name" in response_data
        assert "python_file_created" not in response_data


def test_fund_config_endpoint_service_error(flask_test_client, app):
    """Test handling of service errors"""
    app.config["FLASK_ENV"] = "development"

    test_data = {"short_name": "TEST", "rounds": {"r1": {"short_name": "r1", "sections_config": [], "base_path": 1001}}}

    with patch("pre_award.fund_store.api.routes.process_fund_config") as mock_process:
        mock_process.return_value = {"success": False, "message": "Service error"}

        response = flask_test_client.post("/fund/fund-config", json=test_data)

        assert response.status_code == 500
        assert "Service error" in response.get_json()["error"]
