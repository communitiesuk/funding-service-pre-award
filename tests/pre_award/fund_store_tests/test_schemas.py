import pytest

from pre_award.fund_store.db.models import FormName
from pre_award.fund_store.db.models.section import Section
from pre_award.fund_store.db.schemas.section import (
    SECTION_SCHEMA_MAP,
    EnglishSectionSchema,
    WelshSectionSchema,
)

section = Section(
    id=1,
    title_json={"en": "English Title", "cy": "Welsh Title"},
    form_name=[FormName(form_name_json={"en": "English Form Name", "cy": "Welsh Form Name"})],
    children=[
        Section(
            id=1,
            title_json={"en": "English Child Section 1", "cy": "Welsh Child Section"},
            path="1.1",
        ),
        Section(
            id=3,
            title_json={"en": "English Child Section 3", "cy": "Welsh Child Section"},
            path="1.3",
        ),
        Section(
            id=2,
            title_json={"en": "English Child Section 2", "cy": "Welsh Child Section"},
            path="1.2",
        ),
    ],
)

expected_en = {
    "children": [
        {
            "children": [],
            "fields": [],
            "form_name": None,
            "id": 1,
            "path": "1.1",
            "requires_feedback": None,
            "title": "English Child Section 1",
            "title_json": {
                "cy": "Welsh Child Section",
                "en": "English Child Section 1",
            },
            "weighting": None,
        },
        {
            "children": [],
            "fields": [],
            "form_name": None,
            "id": 2,
            "path": "1.2",
            "requires_feedback": None,
            "title": "English Child Section 2",
            "title_json": {
                "cy": "Welsh Child Section",
                "en": "English Child Section 2",
            },
            "weighting": None,
        },
        {
            "children": [],
            "fields": [],
            "form_name": None,
            "id": 3,
            "path": "1.3",
            "requires_feedback": None,
            "title": "English Child Section 3",
            "title_json": {
                "cy": "Welsh Child Section",
                "en": "English Child Section 3",
            },
            "weighting": None,
        },
    ],
    "fields": [],
    "form_name": "English Form Name",
    "id": 1,
    "path": None,
    "requires_feedback": None,
    "title": "English Title",
    "title_json": {"cy": "Welsh Title", "en": "English Title"},
    "weighting": None,
}

expected_cy = {
    "children": [
        {
            "children": [],
            "fields": [],
            "form_name": None,
            "id": 1,
            "path": "1.1",
            "requires_feedback": None,
            "title": "Welsh Child Section",
            "title_json": {
                "cy": "Welsh Child Section",
                "en": "English Child Section 1",
            },
            "weighting": None,
        },
        {
            "children": [],
            "fields": [],
            "form_name": None,
            "id": 2,
            "path": "1.2",
            "requires_feedback": None,
            "title": "Welsh Child Section",
            "title_json": {
                "cy": "Welsh Child Section",
                "en": "English Child Section 2",
            },
            "weighting": None,
        },
        {
            "children": [],
            "fields": [],
            "form_name": None,
            "id": 3,
            "path": "1.3",
            "requires_feedback": None,
            "title": "Welsh Child Section",
            "title_json": {
                "cy": "Welsh Child Section",
                "en": "English Child Section 3",
            },
            "weighting": None,
        },
    ],
    "fields": [],
    "form_name": "Welsh Form Name",
    "id": 1,
    "path": None,
    "requires_feedback": None,
    "title": "Welsh Title",
    "title_json": {"cy": "Welsh Title", "en": "English Title"},
    "weighting": None,
}


@pytest.mark.parametrize(
    "section, lang_code, expected",
    [
        (section, "en", expected_en),
        (section, "cy", expected_cy),
    ],
)
def test_dump(section, lang_code, expected):
    schema = SECTION_SCHEMA_MAP[lang_code]()
    result = schema.dump(section)
    assert result == expected


def test_section_schema_map():
    assert SECTION_SCHEMA_MAP["en"] == EnglishSectionSchema
    assert SECTION_SCHEMA_MAP["cy"] == WelshSectionSchema
