def test_healthchecks_endpoint(flask_test_client):
    response = flask_test_client.get("/healthcheck")

    expected_dict = {
        "checks": [{"check_flask_running": "OK"}, {"check_db": "OK"}, {"check_redis": "OK"}],
        "version": "123123",
    }

    assert 200 == response.status_code, "Unexpected status code"
    assert expected_dict == response.json, "Unexpected json body"
