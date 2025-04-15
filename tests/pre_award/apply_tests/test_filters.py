import datetime
from datetime import datetime as dt

import pytest
from pytz import timezone

import pre_award.apply.filters as filters
from common.utils.filters import to_bst


def test_date_format_short_month(app):
    a_datetime = datetime.datetime(2020, 1, 1, 12, 0, 0)
    with app.test_request_context():
        assert filters.date_format_short_month(a_datetime) == "01 Jan 2020"


def test_datetime_format_short_month(app):
    a_datetime = datetime.datetime(2020, 1, 1, 12, 0, 0)
    with app.test_request_context():
        assert filters.datetime_format_short_month(a_datetime) == "01 Jan 2020 at 12:00pm"


@pytest.mark.parametrize(
    "input_date, expected",
    [
        ("2020-01-01T00:00:00", "01 January 2020 at midnight"),
        ("2020-01-01T12:00:00", "01 January 2020 at midday"),
        ("2020-01-01T05:30:00", "01 January 2020 at 5:30am"),
        ("2020-12-01T23:59:59", "01 December 2020 at 11:59pm"),
        ("2020-12-01T15:45:00", "01 December 2020 at 3:45pm"),
        ("2020-12-01T01:00:00", "01 December 2020 at 1:00am"),
    ],
)
def test_datetime_format(input_date, expected, app):
    with app.test_request_context():
        assert filters.datetime_format(input_date) == expected


@pytest.mark.parametrize(
    "input_date, expected",
    [
        (
            dt(2025, 1, 1, 0, 0, 0),
            timezone("Europe/London").localize(dt(2025, 1, 1, 0, 0, 0)),
        ),  # Standard time (when UTC == BST)
        (
            dt(2025, 12, 25, 18, 30, 0),
            timezone("Europe/London").localize(dt(2025, 12, 25, 18, 30, 0)),
        ),  # Standard time (when UTC == BST
        (
            dt(2025, 6, 1, 12, 0, 0),
            timezone("Europe/London").localize(dt(2025, 6, 1, 13, 0, 0)),
        ),  # When BST is one hour ahead of UTC
        (
            dt(2025, 9, 30, 1, 25, 0),
            timezone("Europe/London").localize(dt(2025, 9, 30, 2, 25, 0)),
        ),  # When BST is one hour ahead of UTC
        (
            timezone("UTC").localize(dt(2025, 1, 1, 12, 0, 0)),
            timezone("Europe/London").localize(dt(2025, 1, 1, 12, 0, 0)),
        ),  # Input with an existing UTC timezone when UTC == BST
        (
            timezone("UTC").localize(dt(2025, 6, 1, 12, 0, 0)),
            timezone("Europe/London").localize(dt(2025, 6, 1, 13, 0, 0)),
        ),  # Input with an existing UTC timezone when BST is one hour ahead of UTC
        (
            timezone("Europe/London").localize(dt(2025, 6, 1, 12, 0, 0)),
            timezone("Europe/London").localize(dt(2025, 6, 1, 12, 0, 0)),
        ),  # Input already in BST
        (None, None),
    ],
)
def test_to_bst(input_date, expected):
    assert to_bst(input_date) == expected


@pytest.mark.parametrize(
    "input_string, expected",
    [
        ("Testing_snake_case", "Testing Snake Case"),
        ("_Testing_snake_case", "Testing Snake Case"),
    ],
)
def test_snake_case_to_human(input_string, expected):
    assert filters.snake_case_to_human(input_string) == expected


@pytest.mark.parametrize(
    "input_string, expected",
    [
        ("testing-kebab-case", "Testing kebab case"),
        ("-testing-kebab-case", "Testing kebab case"),
    ],
)
def test_kebab_case_to_human(input_string, expected):
    assert filters.kebab_case_to_human(input_string) == expected


def test_status_translation(app):
    assert filters.status_translation("NOT_STARTED") == "Not Started"
