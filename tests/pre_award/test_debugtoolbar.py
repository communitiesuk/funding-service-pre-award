import pytest

from pre_award.config.envs.default import DefaultConfig


@pytest.mark.parametrize(
    "flask_env, should_initialise",
    (
        ("development", True),
        ("dev", False),
        ("test", False),
        ("prod", False),
        ("production", False),
    ),
)
def test_flask_debugtoolbar_initialisation(mocker, flask_env, should_initialise):
    from app import create_app

    mock_toolbar = mocker.patch("app.toolbar.init_app")

    mocker.patch.object(DefaultConfig, "FLASK_ENV", flask_env)

    create_app()

    assert mock_toolbar.called is should_initialise
