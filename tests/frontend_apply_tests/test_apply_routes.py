import pytest

from tests.frontend_apply_tests.conftest import mock_fund, mock_round_open


def test_landing_route_success(apply_test_client, mock_get_fund_and_round_success, templates_rendered):
    response = apply_test_client.get("/monolith/ctdf/cr1")
    assert response.status_code == 200
    rendered_template = templates_rendered[0]
    assert "apply/apply-landing.html.jinja" == rendered_template[0].name
    assert mock_fund == rendered_template[1]["fund"]
    assert mock_round_open == rendered_template[1]["round"]


@pytest.mark.parametrize("response_from_get_fund_round", [(mock_fund, None), (None, mock_round_open), (None, None)])
def test_landing_route_404(apply_test_client, templates_rendered, response_from_get_fund_round, mocker):
    mocker.patch("frontend.apply.routes.get_fund_and_round", return_value=response_from_get_fund_round)
    mocker.patch("app.find_fund_and_round_in_request", return_value=response_from_get_fund_round)
    response = apply_test_client.get("/monolith/ctdf/cr1")
    assert response.status_code == 404
    rendered_template = templates_rendered[0]
    assert "apply/404.html" == rendered_template[0].name
