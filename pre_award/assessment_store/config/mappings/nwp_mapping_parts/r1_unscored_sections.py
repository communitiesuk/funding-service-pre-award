# ruff: noqa: E501

unscored_sections = [
    {
        "id": "unscored",
        "name": "Unscored",
        "sub_criteria": [
            {
                "id": "organisation_details",
                "name": "Organisation details",
                "themes": [
                    {
                        "id": "organisation_details_theme",
                        "name": "Organisation details",
                        "answers": [
                            {
                                "field_id": "GtoolQ",
                                "form_name": "nwp-r1-organisation-details",
                                "field_type": "textField",
                                "presentation_type": "text",
                                "question": "Give the official name registered with companies house or trading standards.",
                            },
                            {
                                "field_id": "JwFyrI",
                                "form_name": "organisation-details.json",
                                "field_type": "textField",
                                "presentation_type": "text",
                                "question": "Give any alternative names that your organisation is known by.",
                            },
                        ],
                    }
                ],
            },
        ],
    },
]
