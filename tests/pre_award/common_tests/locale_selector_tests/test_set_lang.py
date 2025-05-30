from unittest.mock import ANY, Mock

from pre_award.common.locale_selector.set_lang import LanguageSelector


def test_set_lang(app):
    mock_app = Mock()
    set_lang = LanguageSelector(mock_app)
    mock_app.add_url_rule.assert_called_with("/language/<locale>", view_func=ANY, host=ANY)
    with app.test_client() as flask_test_client:
        with flask_test_client.application.test_request_context():
            response = set_lang.select_language("cy")
            response_cookie = response.headers.get("Set-Cookie")
            assert response_cookie is not None, "No cookie set for language"
            assert response_cookie.split(";")[0] == ("language" + "=cy")
