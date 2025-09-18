import re

import pytest
from bs4 import BeautifulSoup
from flask import render_template

from tests.unit.conftest import mock_fund, mock_round_closed, mock_round_open


@pytest.mark.parametrize("mock_round, window_closed_visible", [(mock_round_open, False), (mock_round_closed, True)])
def test_render_landing(apply_test_client, mock_round, window_closed_visible):
    result = render_template("apply/landing.html", fund=mock_fund, round=mock_round)
    assert result
    soup = BeautifulSoup(result, "html.parser")
    assert soup.find("span", {"class": "govuk-caption-xl"}, string="Crash Test Dummy Fund - " + mock_round.title)
    assert soup.find("h1", string="Start or continue an application for funding for crash test dummies")
    assert soup.find(
        "p",
        {"class": "govuk-body"},
        string=re.compile("This is a fake fund for testing so will not result in you getting any money!"),
    )
    assert soup.find(
        "strong",
        string=re.compile("Submission deadline:"),
    )

    assert "Enter your email address" in soup.find("a", role="button").text
    # Check things that do not apply to this fund are not displayed
    if window_closed_visible:
        assert soup.find(string=re.compile("Window closed"))
    else:
        assert not soup.find(string=re.compile("Window closed"))
    assert not soup.find(string=re.compile("This service is also available"))
