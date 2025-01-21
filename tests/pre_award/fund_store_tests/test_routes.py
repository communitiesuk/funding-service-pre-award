import pytest

from pre_award.fund_store.api.routes import filter_fund_by_lang, filter_round_by_lang


@pytest.mark.parametrize(
    "fund_data, lang_key, expected",
    [
        (
            {
                "name_json": {"en": "English Name", "fr": "French Name"},
                "title_json": {"en": "English Title", "fr": "French Title"},
                "description_json": {
                    "en": "English Description",
                    "fr": "French Description",
                },
            },
            "en",
            {
                "description": "English Description",
                "description_json": {
                    "en": "English Description",
                    "fr": "French Description",
                },
                "name": "English Name",
                "name_json": {"en": "English Name", "fr": "French Name"},
                "title": "English Title",
                "title_json": {"en": "English Title", "fr": "French Title"},
            },
        ),
        (
            {
                "name_json": {"en": "English Name", "fr": "French Name"},
                "title_json": {"en": "English Title", "fr": "French Title"},
                "description_json": {
                    "en": "English Description",
                    "fr": "French Description",
                },
            },
            "fr",
            {
                "description": "French Description",
                "description_json": {
                    "en": "English Description",
                    "fr": "French Description",
                },
                "name": "French Name",
                "name_json": {"en": "English Name", "fr": "French Name"},
                "title": "French Title",
                "title_json": {"en": "English Title", "fr": "French Title"},
            },
        ),
        (
            [
                {
                    "name_json": {"en": "English Name", "fr": "French Name"},
                    "title_json": {"en": "English Title", "fr": "French Title"},
                    "description_json": {
                        "en": "English Description",
                        "fr": "French Description",
                    },
                },
                {
                    "name_json": {
                        "en": "Another English Name",
                        "fr": "Another French Name",
                    },
                    "title_json": {
                        "en": "Another English Title",
                        "fr": "Another French Title",
                    },
                    "description_json": {
                        "en": "Another English Description",
                        "fr": "Another French Description",
                    },
                },
            ],
            "en",
            [
                {
                    "description": "English Description",
                    "description_json": {
                        "en": "English Description",
                        "fr": "French Description",
                    },
                    "name": "English Name",
                    "name_json": {"en": "English Name", "fr": "French Name"},
                    "title": "English Title",
                    "title_json": {"en": "English Title", "fr": "French Title"},
                },
                {
                    "description": "Another English Description",
                    "description_json": {
                        "en": "Another English Description",
                        "fr": "Another French Description",
                    },
                    "name": "Another English Name",
                    "name_json": {
                        "en": "Another English Name",
                        "fr": "Another French Name",
                    },
                    "title": "Another English Title",
                    "title_json": {
                        "en": "Another English Title",
                        "fr": "Another French Title",
                    },
                },
            ],
        ),
        (
            [
                {
                    "name_json": {"en": "English Name", "fr": "French Name"},
                    "title_json": {"en": "English Title", "fr": "French Title"},
                    "description_json": {
                        "en": "English Description",
                        "fr": "French Description",
                    },
                },
                {
                    "name_json": {
                        "en": "Another English Name",
                        "fr": "Another French Name",
                    },
                    "title_json": {
                        "en": "Another English Title",
                        "fr": "Another French Title",
                    },
                    "description_json": {
                        "en": "Another English Description",
                        "fr": "Another French Description",
                    },
                },
            ],
            "fr",
            [
                {
                    "description": "French Description",
                    "description_json": {
                        "en": "English Description",
                        "fr": "French Description",
                    },
                    "name": "French Name",
                    "name_json": {"en": "English Name", "fr": "French Name"},
                    "title": "French Title",
                    "title_json": {"en": "English Title", "fr": "French Title"},
                },
                {
                    "description": "Another French Description",
                    "description_json": {
                        "en": "Another English Description",
                        "fr": "Another French Description",
                    },
                    "name": "Another French Name",
                    "name_json": {
                        "en": "Another English Name",
                        "fr": "Another French Name",
                    },
                    "title": "Another French Title",
                    "title_json": {
                        "en": "Another English Title",
                        "fr": "Another French Title",
                    },
                },
            ],
        ),
        ("Not a dictionary or a list", "en", "Not a dictionary or a list"),
    ],
)
def test_filter_fund_by_lang(fund_data, lang_key, expected):
    assert filter_fund_by_lang(fund_data, lang_key) == expected


@pytest.mark.parametrize(
    "round_data, lang_key, expected",
    [
        (
            {
                "title_json": {"en": "English Title", "fr": "French Title"},
                "instructions_json": {"en": "English Instructions", "fr": "French Instructions"},
                "application_guidance_json": {
                    "en": "English Application Guidance",
                    "fr": "French Application Guidance",
                },
                "contact_us_banner_json": {
                    "en": "English banner",
                    "fr": "French banner",
                },
            },
            "en",
            {
                "title": "English Title",
                "title_json": {"en": "English Title", "fr": "French Title"},
                "instructions": "English Instructions",
                "instructions_json": {"en": "English Instructions", "fr": "French Instructions"},
                "application_guidance": "English Application Guidance",
                "application_guidance_json": {
                    "en": "English Application Guidance",
                    "fr": "French Application Guidance",
                },
                "contact_us_banner": "English banner",
                "contact_us_banner_json": {
                    "en": "English banner",
                    "fr": "French banner",
                },
            },
        ),
        (
            {
                "title_json": {"en": "English Title", "fr": "French Title"},
                "instructions_json": {"en": "English Instructions", "fr": "French Instructions"},
                "application_guidance_json": {
                    "en": "English Application Guidance",
                    "fr": "French Application Guidance",
                },
                "contact_us_banner_json": {
                    "en": "English banner",
                    "fr": "French banner",
                },
            },
            "fr",
            {
                "title": "French Title",
                "title_json": {"en": "English Title", "fr": "French Title"},
                "instructions": "French Instructions",
                "instructions_json": {"en": "English Instructions", "fr": "French Instructions"},
                "application_guidance": "French Application Guidance",
                "application_guidance_json": {
                    "en": "English Application Guidance",
                    "fr": "French Application Guidance",
                },
                "contact_us_banner": "French banner",
                "contact_us_banner_json": {
                    "en": "English banner",
                    "fr": "French banner",
                },
            },
        ),
        (
            [
                {
                    "title_json": {"en": "English Title", "fr": "French Title"},
                    "instructions_json": {"en": "English Instructions", "fr": "French Instructions"},
                    "application_guidance_json": {
                        "en": "English Application Guidance",
                        "fr": "French Application Guidance",
                    },
                    "contact_us_banner_json": {
                        "en": "English banner",
                        "fr": "French banner",
                    },
                },
                {
                    "title_json": {
                        "en": "Another English Title",
                        "fr": "Another French Title",
                    },
                    "instructions_json": {"en": "Another English Instructions", "fr": "Another French Instructions"},
                    "application_guidance_json": {
                        "en": "Another English Application Guidance",
                        "fr": "Another French Application Guidance",
                    },
                    "contact_us_banner_json": {
                        "en": "Another English banner",
                        "fr": "Another French banner",
                    },
                },
            ],
            "en",
            [
                {
                    "title": "English Title",
                    "title_json": {"en": "English Title", "fr": "French Title"},
                    "instructions": "English Instructions",
                    "instructions_json": {"en": "English Instructions", "fr": "French Instructions"},
                    "application_guidance": "English Application Guidance",
                    "application_guidance_json": {
                        "en": "English Application Guidance",
                        "fr": "French Application Guidance",
                    },
                    "contact_us_banner": "English banner",
                    "contact_us_banner_json": {
                        "en": "English banner",
                        "fr": "French banner",
                    },
                },
                {
                    "title": "Another English Title",
                    "title_json": {
                        "en": "Another English Title",
                        "fr": "Another French Title",
                    },
                    "instructions": "Another English Instructions",
                    "instructions_json": {"en": "Another English Instructions", "fr": "Another French Instructions"},
                    "application_guidance": "Another English Application Guidance",
                    "application_guidance_json": {
                        "en": "Another English Application Guidance",
                        "fr": "Another French Application Guidance",
                    },
                    "contact_us_banner": "Another English banner",
                    "contact_us_banner_json": {
                        "en": "Another English banner",
                        "fr": "Another French banner",
                    },
                },
            ],
        ),
        (
            [
                {
                    "title_json": {"en": "English Title", "fr": "French Title"},
                    "instructions_json": {"en": "English Instructions", "fr": "French Instructions"},
                    "application_guidance_json": {
                        "en": "English Application Guidance",
                        "fr": "French Application Guidance",
                    },
                    "contact_us_banner_json": {
                        "en": "English banner",
                        "fr": "French banner",
                    },
                },
                {
                    "title_json": {
                        "en": "Another English Title",
                        "fr": "Another French Title",
                    },
                    "instructions_json": {"en": "Another English Instructions", "fr": "Another French Instructions"},
                    "application_guidance_json": {
                        "en": "Another English Application Guidance",
                        "fr": "Another French Application Guidance",
                    },
                    "contact_us_banner_json": {
                        "en": "Another English banner",
                        "fr": "Another French banner",
                    },
                },
            ],
            "fr",
            [
                {
                    "title": "French Title",
                    "title_json": {"en": "English Title", "fr": "French Title"},
                    "instructions": "French Instructions",
                    "instructions_json": {"en": "English Instructions", "fr": "French Instructions"},
                    "application_guidance": "French Application Guidance",
                    "application_guidance_json": {
                        "en": "English Application Guidance",
                        "fr": "French Application Guidance",
                    },
                    "contact_us_banner": "French banner",
                    "contact_us_banner_json": {
                        "en": "English banner",
                        "fr": "French banner",
                    },
                },
                {
                    "title": "Another French Title",
                    "title_json": {
                        "en": "Another English Title",
                        "fr": "Another French Title",
                    },
                    "instructions": "Another French Instructions",
                    "instructions_json": {"en": "Another English Instructions", "fr": "Another French Instructions"},
                    "application_guidance": "Another French Application Guidance",
                    "application_guidance_json": {
                        "en": "Another English Application Guidance",
                        "fr": "Another French Application Guidance",
                    },
                    "contact_us_banner": "Another French banner",
                    "contact_us_banner_json": {
                        "en": "Another English banner",
                        "fr": "Another French banner",
                    },
                },
            ],
        ),
        ("Not a dictionary or a list", "en", "Not a dictionary or a list"),
    ],
)
def test_filter_round_by_lang(round_data, lang_key, expected):
    assert filter_round_by_lang(round_data, lang_key) == expected
