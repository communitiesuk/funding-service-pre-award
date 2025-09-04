from flask import Flask

from pre_award.apply.helpers import format_rehydrate_payload


def test_format_rehydrate_payload_test_change_request_filter(app: Flask) -> None:
    change_requests = {
        "abc": ["message 1", "message 2"],
        "def": ["message 3", "message 4"],
        "123": ["message 5", "message 6"],
    }

    form_data = {
        "name": "sf-r1-organisation-name-sample",
        "questions": [
            {
                "category": "FabDefault",
                "fields": [
                    {
                        "answer": "Answer 1",
                        "key": "abc",
                        "title": "Organisation name",
                        "type": "text",
                    },
                    {
                        "answer": False,
                        "key": "aaa",
                        "title": "Does your organisation use any  other names?",
                        "type": "list",
                    },
                ],
                "question": "Organisation name",
                "status": "COMPLETED",
            },
        ],
        "status": "CHANGE_REQUESTED",
    }

    formatted_data = format_rehydrate_payload(
        form_data=form_data,
        application_id="abc",
        returnUrl="https://test.test",
        form_name="test_form",
        markAsCompleteEnabled=True,
        change_requests=change_requests,
    )

    expected_change_requests = {
        "abc": ["message 1", "message 2"],
    }

    assert formatted_data["metadata"]["change_requests"] == expected_change_requests


def test_format_rehydrate_payload_test_change_request_filter_when_none(app: Flask) -> None:
    form_data = {
        "name": "sf-r1-organisation-name-sample",
        "questions": [
            {
                "category": "FabDefault",
                "fields": [
                    {
                        "answer": "Answer 1",
                        "key": "abc",
                        "title": "Organisation name",
                        "type": "text",
                    },
                    {
                        "answer": False,
                        "key": "aaa",
                        "title": "Does your organisation use any  other names?",
                        "type": "list",
                    },
                ],
                "question": "Organisation name",
                "status": "COMPLETED",
            },
        ],
        "status": "CHANGE_REQUESTED",
    }

    formatted_data = format_rehydrate_payload(
        form_data=form_data,
        application_id="abc",
        returnUrl="https://test.test",
        form_name="test_form",
        markAsCompleteEnabled=True,
        change_requests=None,
    )

    assert formatted_data["metadata"]["change_requests"] is None


def test_format_rehydrate_payload_test_all_change_requests_filtered_out(app: Flask) -> None:
    change_requests = {
        "abc": ["message 1", "message 2"],
        "def": ["message 3", "message 4"],
        "123": ["message 5", "message 6"],
    }

    form_data = {
        "name": "sf-r1-organisation-name-sample",
        "questions": [
            {
                "category": "FabDefault",
                "fields": [
                    {
                        "answer": "Answer 1",
                        "key": "000",
                        "title": "Organisation name",
                        "type": "text",
                    },
                    {
                        "answer": False,
                        "key": "aaa",
                        "title": "Does your organisation use any  other names?",
                        "type": "list",
                    },
                ],
                "question": "Organisation name",
                "status": "COMPLETED",
            },
        ],
        "status": "CHANGE_REQUESTED",
    }

    formatted_data = format_rehydrate_payload(
        form_data=form_data,
        application_id="abc",
        returnUrl="https://test.test",
        form_name="test_form",
        markAsCompleteEnabled=True,
        change_requests=change_requests,
    )

    assert formatted_data["metadata"]["change_requests"] is None


def test_format_rehydrate_payload_test_adds_is_resubmission(app: Flask) -> None:
    formatted_data = format_rehydrate_payload(
        form_data={},
        application_id="abc",
        returnUrl="https://test.test",
        form_name="test_form",
        markAsCompleteEnabled=True,
        change_requests=None,
        is_resubmission=True,
    )

    assert formatted_data["metadata"]["is_resubmission"] is True
