from tests.unit.conftest import mock_fund, mock_round_open


def test_landing_route_success(apply_test_client, mock_get_round_success, templates_rendered):
    response = apply_test_client.get("/funding-round/ctdf/cr1")
    assert response.status_code == 200
    rendered_template = templates_rendered[0]
    assert "apply/landing.html" == rendered_template[0].name
    assert mock_fund == rendered_template[1]["fund"]
    assert mock_round_open == rendered_template[1]["round"]


def test_landing_route_404(apply_test_client, templates_rendered, mocker):
    mocker.patch("apply.routes.get_round", return_value=None)
    mocker.patch("app.find_fund_and_round_in_request", return_value=(None, None))
    response = apply_test_client.get("/funding-round/ctdf/cr1")
    assert response.status_code == 404
    rendered_template = templates_rendered[0]
    assert "apply/404.html" == rendered_template[0].name
