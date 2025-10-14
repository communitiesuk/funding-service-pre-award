import base64
import uuid
from unittest.mock import ANY
from uuid import uuid4

import pytest

from pre_award.application_store.config.key_report_mappings.cof_eoi_key_report_mapping import (
    COF_EOI_KEY_REPORT_MAPPING,
)
from pre_award.application_store.config.key_report_mappings.cof_key_report_mapping import (
    COF_KEY_REPORT_MAPPING,
)
from pre_award.application_store.config.key_report_mappings.cof_r2_key_report_mapping import (
    COF_R2_KEY_REPORT_MAPPING,
)
from pre_award.application_store.config.key_report_mappings.cof_r3w2_key_report_mapping import (
    COF_R3W2_KEY_REPORT_MAPPING,
)
from pre_award.application_store.config.key_report_mappings.mappings import (
    ROUND_ID_TO_KEY_REPORT_MAPPING,
)
from pre_award.application_store.config.key_report_mappings.model import (
    KeyReportMapping,
    extract_postcode,
)
from pre_award.application_store.db.models import Applications, Forms
from pre_award.application_store.db.models.application.enums import Status as ApplicationStatus
from pre_award.application_store.db.models.forms.enums import Status as FormStatus
from pre_award.application_store.db.queries.application import (
    check_change_requested_for_applications,
    create_application,
    create_qa_base64file,
    mark_application_with_requested_changes,
    process_files,
)
from pre_award.application_store.db.queries.application.queries import get_applications_by_references
from pre_award.application_store.db.queries.reporting.queries import (
    export_application_statuses_to_csv,
    map_application_key_fields,
)
from pre_award.application_store.external_services.aws import FileData
from pre_award.application_store.external_services.models.fund import Fund
from tests.pre_award.application_store_tests.seed_data.application_data import expected_application_json


@pytest.mark.parametrize(
    "requested_language,fund_supports_welsh,exp_language",
    [
        ("en", True, "en"),
        ("en", False, "en"),
        ("cy", True, "cy"),
        ("cy", False, "en"),
    ],
)
def test_create_application_language_choice(mocker, fund_supports_welsh, requested_language, exp_language):
    mock_fund = Fund(
        "Generated test fund no welsh",
        str(uuid4()),
        "TEST",
        "Testing fund",
        fund_supports_welsh,
        {"en": "English Fund Name", "cy": "Welsh Fund Name"},
        "COMPETED",
        [],
    )
    mocker.patch("pre_award.application_store.db.queries.application.queries.get_fund", return_value=mock_fund)
    mock_create_app_try = mocker.patch(
        "pre_award.application_store.db.queries.application.queries._create_application_try",
        return_value="new application",
    )

    create_application(account_id="test", fund_id="", round_id="", language=requested_language)
    mock_create_app_try.assert_called_once_with(
        account_id="test",
        fund_id=ANY,
        round_id=ANY,
        key=ANY,
        language=exp_language,
        reference=ANY,
        attempt=0,
    )


def test_application_map_contents_and_base64_convertor(mocker, app):
    """
    GIVEN: our service running with app_context fixture.
    WHEN: two separate methods on different classes chained together with given
     expected incoming JSON.
    THEN: we check if expected output is returned.
    """
    with app.app_context():
        expected_json = expected_application_json
        mock_fund = Fund(
            "Community Ownership Fund",
            str(uuid4()),
            "TEST",
            "Testing fund",
            False,
            {"en": "English Fund Name"},
            "COMPETED",
            [],
        )
        mocker.patch("pre_award.application_store.db.queries.application.queries.get_fund", return_value=mock_fund)
        expected_json = create_qa_base64file(expected_json["content"]["application"], True)

        assert "Jack-Simon" in base64.b64decode(expected_json["questions_file"]).decode()
        assert "Yes" in base64.b64decode(expected_json["questions_file"]).decode()
        assert "No" in base64.b64decode(expected_json["questions_file"]).decode()


@pytest.mark.parametrize(
    "application, all_application_files, expected",
    [
        pytest.param(
            Applications(forms=[Forms(json=[{"fields": [{"key": "not_a_file_component", "answer": None}]}])]),
            [FileData("app1", "form1", "path1", "component1", "file1.docx")],
            Applications(forms=[Forms(json=[{"fields": [{"key": "not_a_file_component", "answer": None}]}])]),
            id="Irrelevant components are ignored",
        ),
        pytest.param(
            Applications(
                forms=[
                    Forms(json=[{"fields": [{"key": "component1", "answer": None}]}]),
                    Forms(json=[{"fields": [{"key": "component2", "answer": None}]}]),
                ]
            ),
            [
                FileData("app1", "form1", "path1", "component1", "file1.docx"),
                FileData("app1", "form1", "path1", "component2", "file2.docx"),
            ],
            Applications(
                forms=[
                    Forms(json=[{"fields": [{"key": "component1", "answer": "file1.docx"}]}]),
                    Forms(json=[{"fields": [{"key": "component2", "answer": "file2.docx"}]}]),
                ]
            ),
            id="Multiple forms all work as expected",
        ),
        pytest.param(
            Applications(forms=[Forms(json=[{"fields": [{"key": "component1", "answer": None}]}])]),
            [FileData("app1", "form1", "path1", "component1", "file1.docx")],
            Applications(forms=[Forms(json=[{"fields": [{"key": "component1", "answer": "file1.docx"}]}])]),
            id="Single file available for a component",
        ),
        pytest.param(
            Applications(forms=[Forms(json=[{"fields": [{"key": "component1", "answer": None}]}])]),
            [
                FileData("app1", "form1", "path1", "component1", "file1.docx"),
                FileData("app1", "form1", "path2", "component1", "file2.pdf"),
                FileData("app1", "form1", "path3", "component1", "file3.txt"),
            ],
            Applications(
                forms=[
                    Forms(
                        json=[
                            {
                                "fields": [
                                    {
                                        "key": "component1",
                                        "answer": "file1.docx, file2.pdf, file3.txt",
                                    }
                                ]
                            }
                        ]
                    )
                ]
            ),
            id="Multiple files available for a component",
        ),
        pytest.param(
            Applications(
                forms=[
                    Forms(
                        json=[
                            {
                                "fields": [
                                    {"key": "component1", "answer": None},
                                    {"key": "component2", "answer": None},
                                ]
                            }
                        ]
                    )
                ]
            ),
            [
                FileData("app1", "form1", "path1", "component1", "file1.docx"),
                FileData("app1", "form1", "path2", "component1", "file2.pdf"),
                FileData("app1", "form1", "path3", "component2", "file3.txt"),
            ],
            Applications(
                forms=[
                    Forms(
                        json=[
                            {
                                "fields": [
                                    {
                                        "key": "component1",
                                        "answer": "file1.docx, file2.pdf",
                                    },
                                    {"key": "component2", "answer": "file3.txt"},
                                ]
                            }
                        ]
                    )
                ]
            ),
            id="Files available for multiple components",
        ),
    ],
)
def test_process_files(application, all_application_files, expected):
    """
    GIVEN an application object and a list of all files belonging to that application
    WHEN the process_files function is invoked with these parameters
    THEN the application object is expected to be updated with the relevant file information
    """
    result = process_files(application, all_application_files)
    for form, expected_form in zip(result.forms, expected.forms, strict=False):
        assert form.json == pytest.approx(expected_form.json)


@pytest.mark.parametrize(
    "data,lines_exp",
    [
        (
            [
                {
                    "fund_id": "111",
                    "rounds": [
                        {
                            "round_id": "r1r1r1",
                            "application_statuses": {
                                "NOT_STARTED": 1,
                                "IN_PROGRESS": 2,
                                "COMPLETED": 3,
                                "SUBMITTED": 4,
                                "CHANGE_REQUESTED": 0,
                                "CHANGE_RECEIVED": 0,
                            },
                        }
                    ],
                }
            ],
            ["111,r1r1r1,1,2,3,4,0,0"],
        ),
        (
            [
                {
                    "fund_id": "111",
                    "rounds": [
                        {
                            "round_id": "r1r1r1",
                            "application_statuses": {
                                "NOT_STARTED": 1,
                                "IN_PROGRESS": 2,
                                "COMPLETED": 3,
                                "SUBMITTED": 4,
                                "CHANGE_REQUESTED": 0,
                                "CHANGE_RECEIVED": 0,
                            },
                        },
                        {
                            "round_id": "r2",
                            "application_statuses": {
                                "NOT_STARTED": 2,
                                "IN_PROGRESS": 3,
                                "COMPLETED": 4,
                                "SUBMITTED": 5,
                                "CHANGE_REQUESTED": 0,
                                "CHANGE_RECEIVED": 0,
                            },
                        },
                    ],
                }
            ],
            ["111,r1r1r1,1,2,3,4,0,0", "111,r2,2,3,4,5,0,0"],
        ),
        (
            [
                {
                    "fund_id": "f1",
                    "rounds": [
                        {
                            "round_id": "r1",
                            "application_statuses": {
                                "NOT_STARTED": 1,
                                "IN_PROGRESS": 2,
                                "COMPLETED": 3,
                                "SUBMITTED": 4,
                                "CHANGE_REQUESTED": 0,
                                "CHANGE_RECEIVED": 0,
                            },
                        },
                        {
                            "round_id": "r2",
                            "application_statuses": {
                                "NOT_STARTED": 0,
                                "IN_PROGRESS": 0,
                                "COMPLETED": 0,
                                "SUBMITTED": 4,
                                "CHANGE_REQUESTED": 0,
                                "CHANGE_RECEIVED": 0,
                            },
                        },
                    ],
                },
                {
                    "fund_id": "f2",
                    "rounds": [
                        {
                            "round_id": "r1",
                            "application_statuses": {
                                "NOT_STARTED": 2,
                                "IN_PROGRESS": 2,
                                "COMPLETED": 1,
                                "SUBMITTED": 6,
                                "CHANGE_REQUESTED": 0,
                                "CHANGE_RECEIVED": 0,
                            },
                        },
                    ],
                },
            ],
            ["f1,r1,1,2,3,4,0,0", "f1,r2,0,0,0,4,0,0", "f2,r1,2,2,1,6,0,0"],
        ),
    ],
)
def test_application_status_csv(data, lines_exp):
    result = export_application_statuses_to_csv(data)
    assert result
    lines = result.readlines()
    assert (
        lines[0].decode().strip()
        == "fund_id,round_id,NOT_STARTED,IN_PROGRESS,COMPLETED,SUBMITTED,CHANGE_REQUESTED,CHANGE_RECEIVED"
    )
    idx = 1
    for line in lines_exp:
        assert lines[idx].decode().strip() == line
        idx += 1


@pytest.mark.parametrize(
    "input_str, expected_output",
    [
        # Valid postcodes
        ("SW1A 1AA", "SW1A 1AA"),
        ("BD23 1DN", "BD23 1DN"),
        ("W1A 0AX", "W1A 0AX"),
        ("GIR 0AA", "GIR 0AA"),  # special case for GIR 0AA
        # Invalid postcodes
        ("123456", None),
        ("ABCDEFG", None),
        ("XYZ 123", None),
        # Mixed strings
        ("My postcode is SW1A 1AA in London.", "SW1A 1AA"),
        ("The code is BD23 1DN for that location.", "BD23 1DN"),
        ("No postcode here.", None),
    ],
)
def test_extract_postcode(input_str, expected_output):
    assert extract_postcode(input_str) == expected_output


@pytest.mark.parametrize(
    "key_report_mapping, application, expected_output",
    [
        (
            COF_R2_KEY_REPORT_MAPPING,
            {
                "language": "en",
                "forms": [
                    {
                        "name": "organisation-information",
                        "questions": [
                            {
                                "fields": [
                                    {"key": "WWWWxy", "answer": "Ref1234"},
                                    {"key": "YdtlQZ", "answer": "OrgName"},
                                    {"key": "lajFtB", "answer": "Non-Profit"},
                                ]
                            }
                        ],
                    },
                    {
                        "name": "asset-information",
                        "questions": [
                            {
                                "fields": [
                                    {"key": "yaQoxU", "answer": "Building"},
                                ]
                            }
                        ],
                    },
                    {
                        "name": "project-information",
                        "questions": [
                            {
                                "fields": [
                                    {"key": "yEmHpp", "answer": "GIR 0AA"},
                                ]
                            }
                        ],
                    },
                    {
                        "name": "funding-required",
                        "questions": [
                            {
                                "fields": [
                                    {"key": "JzWvhj", "answer": 50000},
                                    {"key": "jLIgoi", "answer": 10000},
                                ]
                            }
                        ],
                    },
                    {
                        "name": "organisation-information-ns",
                        "questions": [
                            {
                                "fields": [
                                    {"key": "opFJRm", "answer": "OrgName NSTF"},
                                ]
                            }
                        ],
                    },
                ],
            },
            {
                "eoi_reference": "Ref1234",
                "organisation_name": "OrgName",
                "organisation_type": "Non-Profit",
                "asset_type": "Building",
                "geography": "GIR 0AA",
                "capital": 50000,
                "revenue": 10000,
                "organisation_name_nstf": "OrgName NSTF",
            },
        ),
        (
            COF_R3W2_KEY_REPORT_MAPPING,
            {
                "language": "en",
                "forms": [
                    {
                        "name": "applicant-information-cof-r3-w2",
                        "questions": [
                            {
                                "fields": [
                                    {"key": "NlHSBg", "answer": "test@test.com"},
                                ]
                            }
                        ],
                    },
                    {
                        "name": "organisation-information-cof-r3-w2",
                        "questions": [
                            {
                                "fields": [
                                    {"key": "WWWWxy", "answer": "Ref1234"},
                                    {"key": "YdtlQZ", "answer": "OrgName"},
                                    {"key": "lajFtB", "answer": "Non-Profit"},
                                ]
                            }
                        ],
                    },
                    {
                        "name": "asset-information-cof-r3-w2",
                        "questions": [
                            {
                                "fields": [
                                    {"key": "oXGwlA", "answer": "Building"},
                                    {"key": "aJGyCR", "answer": "Other"},
                                ]
                            }
                        ],
                    },
                    {
                        "name": "project-information-cof-r3-w2",
                        "questions": [
                            {
                                "fields": [
                                    {"key": "EfdliG", "answer": "GIR 0AA"},
                                    {"key": "apGjFS", "answer": "A name"},
                                ]
                            }
                        ],
                    },
                    {
                        "name": "funding-required-cof-r3-w2",
                        "questions": [
                            {
                                "fields": [
                                    {"key": "ABROnB", "answer": 50000},
                                    {
                                        "key": "tSKhQQ",
                                        "answer": [
                                            {"UyaAHw": 5000},
                                            {"UyaAHw": 5000},
                                        ],
                                    },
                                ]
                            }
                        ],
                    },
                ],
                "asset_type_other": "Other",
                "reference": "ref123",
                "id": "id123",
            },
            {
                "eoi_reference": "Ref1234",
                "applicant_email": "test@test.com",
                "organisation_name": "OrgName",
                "organisation_type": "Non-Profit",
                "asset_type": "Building",
                "asset_type_other": "Other",
                "geography": "GIR 0AA",
                "capital": 50000,
                "project_name": "A name",
                "ref": "ref123",
                "link": "id123",
                "revenue": 10000,
            },
        ),
    ],
)
def test_map_application_key_fields(key_report_mapping: KeyReportMapping, application, expected_output):
    result = map_application_key_fields(application, key_report_mapping.mapping, key_report_mapping.round_id)
    assert result == expected_output


@pytest.mark.parametrize(
    "round_id, exp_mapping",
    [
        (
            "c603d114-5364-4474-a0c4-c41cbf4d3bbd",
            COF_R2_KEY_REPORT_MAPPING.mapping,
        ),  # COF R2W2
        (
            "5cf439bf-ef6f-431e-92c5-a1d90a4dd32f",
            COF_R2_KEY_REPORT_MAPPING.mapping,
        ),  # COF R2W3
        (
            "e85ad42f-73f5-4e1b-a1eb-6bc5d7f3d762",
            COF_R2_KEY_REPORT_MAPPING.mapping,
        ),  # COF R3W1
        (
            "6af19a5e-9cae-4f00-9194-cf10d2d7c8a7",
            COF_R3W2_KEY_REPORT_MAPPING.mapping,
        ),  # COF R3W2
        (
            "4efc3263-aefe-4071-b5f4-0910abec12d2",
            COF_KEY_REPORT_MAPPING.mapping,
        ),  # COF R3W3
        (
            "33726b63-efce-4749-b149-20351346c76e",
            COF_KEY_REPORT_MAPPING.mapping,
        ),  # COF R4W1
        (
            "6a47c649-7bac-4583-baed-9c4e7a35c8b3",
            COF_EOI_KEY_REPORT_MAPPING.mapping,
        ),  # COF EOI
        ("asdf-wer-234-sdf-234", COF_R2_KEY_REPORT_MAPPING.mapping),  # any ID
    ],
)
def test_map_round_id_to_report_fields(round_id, exp_mapping):
    result = ROUND_ID_TO_KEY_REPORT_MAPPING[round_id]
    assert result == exp_mapping


@pytest.fixture
def application_with_forms(db):
    application_id = uuid4()

    forms = [
        Forms(
            application_id=application_id,
            status=FormStatus.COMPLETED,
            name="the-first-form",
            has_completed=True,
            json=[
                {
                    "category": "FabDefault",
                    "question": "Project name",
                    "fields": [{"key": "qwerty", "title": "Project name", "type": "text", "answer": "Hi hello"}],
                    "status": "COMPLETED",
                },
                {
                    "category": "FabDefault",
                    "question": "Project purpose",
                    "fields": [
                        {"key": "yuiopt", "title": "Project purpose", "type": "text", "answer": "No reason really"}
                    ],
                    "status": "COMPLETED",
                },
                {
                    "category": None,
                    "question": "MarkAsComplete",
                    "fields": [
                        {
                            "key": "markAsComplete",
                            "title": "Do you want to mark this section as complete?",
                            "type": "boolean",
                            "answer": True,
                        }
                    ],
                    "status": "COMPLETED",
                },
            ],
        ),
        Forms(
            application_id=application_id,
            status=FormStatus.COMPLETED,
            name="the-second-form",
            has_completed=True,
            json=[
                {
                    "category": "FabDefault",
                    "question": "Organisation name",
                    "fields": [
                        {
                            "key": "asdfgh",
                            "title": "Organisation name",
                            "type": "text",
                            "answer": "Fake Org",
                        }
                    ],
                    "status": "COMPLETED",
                },
                {
                    "category": None,
                    "question": "MarkAsComplete",
                    "fields": [
                        {
                            "key": "markAsComplete",
                            "title": "Do you want to mark this section as complete?",
                            "type": "boolean",
                            "answer": True,
                        }
                    ],
                    "status": "COMPLETED",
                },
            ],
        ),
    ]

    application = Applications(
        id=application_id,
        account_id=uuid4(),
        fund_id=uuid4(),
        round_id=uuid4(),
        key="ABCDEF",
        reference=f"TEST-R1-{uuid4()}",
        project_name="Some project",
        status=ApplicationStatus.COMPLETED,
        forms=forms,
    )

    db.session.add(application)
    db.session.commit()

    return application


@pytest.mark.parametrize(
    "fields_to_change",
    [
        ["qwerty", "asdfgh"],  # Multiple fields in multiple forms
        ["qwerty", "yuiopt"],  # Multiple fields in the same form
        ["asdfgh"],  # Single field in the second form only
        [],  # No fields to change
        ["abcdef"],  # Field that doesn't match anything
    ],
)
def test_mark_application_with_requested_changes_updates_forms_and_application(
    application_with_forms, fields_to_change, db
):
    application = application_with_forms
    application_id = application.id

    mark_application_with_requested_changes(application_id=application_id, field_ids=fields_to_change)

    updated_application = db.session.query(type(application)).get(application_id)
    updated_forms = updated_application.forms

    application_changed = False
    for form in updated_forms:
        has_matching_field = any(
            field["key"] in fields_to_change for category in form.json for field in category["fields"]
        )
        application_changed |= has_matching_field

        if has_matching_field:
            assert form.status == FormStatus.CHANGE_REQUESTED
            assert form.has_completed is False
            for category in form.json:
                for field in category["fields"]:
                    if field["key"] == "markAsComplete":
                        assert field["answer"] is False
        else:
            assert form.status == FormStatus.COMPLETED
            assert form.has_completed is True
            for category in form.json:
                for field in category["fields"]:
                    if field["key"] == "markAsComplete":
                        assert field["answer"] is True

    if application_changed:
        assert updated_application.status == ApplicationStatus.IN_PROGRESS
    else:
        assert updated_application.status == ApplicationStatus.COMPLETED


def test_check_change_requested_for_applications_no_change_requested(application_with_forms, db):
    applications = [application_with_forms]

    result = check_change_requested_for_applications(applications)
    assert result is False


def test_check_change_requested_for_applications(application_with_forms, db):
    applications = [application_with_forms]

    change_requested_form = application_with_forms.forms[0]
    change_requested_form.status = FormStatus.CHANGE_REQUESTED
    db.session.commit()

    result = check_change_requested_for_applications(applications)
    assert result is True


def test_get_applications_by_references_forms_toggle(db):
    """
    Test that get_applications_by_references returns applications with or without forms
    depending on the include_forms parameter.
    """

    # Create an application
    app_id = str(uuid.uuid4())
    unique_reference = f"TEST-REF-{uuid.uuid4()}"
    application = Applications(
        id=app_id,
        account_id="test-account",
        fund_id="test-fund",
        round_id="test-round",
        key="test-key",
        language=None,
        reference=unique_reference,
        project_name="Test Project",
        status="NOT_STARTED",
        is_deleted=False,
    )
    db.session.add(application)
    db.session.commit()

    # Create two forms linked to this application
    form1 = Forms(application_id=app_id, name="Test Form 20")
    form2 = Forms(application_id=app_id, name="Test Form 21")
    db.session.add_all([form1, form2])
    db.session.commit()

    # Test with include_forms=False (default)
    apps_no_forms = get_applications_by_references([unique_reference])
    assert unique_reference in apps_no_forms
    assert hasattr(apps_no_forms[unique_reference], "forms")
    # forms should not be loaded (should be an empty list or not loaded)
    assert apps_no_forms[unique_reference].forms == []
    db.session.expire(apps_no_forms[unique_reference])

    # Test with include_forms=True
    apps_with_forms = get_applications_by_references([unique_reference], include_forms=True)
    assert unique_reference in apps_with_forms
    assert hasattr(apps_with_forms[unique_reference], "forms")
    assert len(apps_with_forms[unique_reference].forms) == 2
    form_ids = {f.id for f in apps_with_forms[unique_reference].forms}
    assert form1.id in form_ids
    assert form2.id in form_ids

    db.session.delete(form1)
    db.session.delete(form2)
    db.session.delete(application)
    db.session.commit()
