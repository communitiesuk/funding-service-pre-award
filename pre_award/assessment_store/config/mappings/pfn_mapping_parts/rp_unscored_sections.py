# ruff: noqa: E501

unscored_sections = [
    {
        "id": "unscored",
        "name": "Unscored",
        "sub_criteria": [
            {
                "id": "place_and_secondary_contact_information",
                "name": "Place and secondary contact information",
                "themes": [
                    {
                        "id": "place_and_secondary_contact_information",
                        "name": "Place and secondary contact information",
                        "answers": [
                            {
                                "field_id": "lrRGwN",
                                "form_name": "pfn-rp-place-and-secondary-contact-information",
                                "field_type": "textField",
                                "presentation_type": "text",
                                "question": "Place",
                            },
                            {
                                "field_id": "UNlQWk",
                                "form_name": "pfn-rp-place-and-secondary-contact-information",
                                "field_type": "textField",
                                "presentation_type": "text",
                                "question": "Local authority",
                            },
                            {
                                "field_id": "fAlBnc",
                                "form_name": "pfn-rp-place-and-secondary-contact-information",
                                "field_type": "textField",
                                "presentation_type": "text",
                                "question": "Country",
                            },
                            {
                                "field_id": "YGzHEh",
                                "form_name": "pfn-rp-place-and-secondary-contact-information",
                                "field_type": "textField",
                                "presentation_type": "text",
                                "question": "Full name",
                            },
                            {
                                "field_id": "PAFzPq",
                                "form_name": "pfn-rp-place-and-secondary-contact-information",
                                "field_type": "textField",
                                "presentation_type": "text",
                                "question": "Organisation",
                            },
                            {
                                "field_id": "kxHEjr",
                                "form_name": "pfn-rp-place-and-secondary-contact-information",
                                "field_type": "textField",
                                "presentation_type": "text",
                                "question": "Role",
                            },
                            {
                                "field_id": "nfSIJu",
                                "form_name": "pfn-rp-place-and-secondary-contact-information",
                                "field_type": "emailAddressField",
                                "presentation_type": "text",
                                "question": "Email address",
                            },
                            {
                                "field_id": "KDdOxr",
                                "form_name": "pfn-rp-place-and-secondary-contact-information",
                                "field_type": "telephoneNumberField",
                                "presentation_type": "text",
                                "question": "Contact number",
                            },
                        ],
                    },
                ],
            },
            {
                "id": "projects",
                "name": "Projects",
                "themes": [
                    {
                        "id": "projects",
                        "name": "Projects",
                        "answers": [
                            {
                                "field_id": "wmpvjb",
                                "form_name": "pfn-rp-projects",
                                "field_type": "yesNoField",
                                "presentation_type": "text",
                                "question": "Can you provide details of any projects you have identified for funding? ",
                            },
                            {
                                "field_id": "dEyfRq",
                                "form_name": "pfn-rp-projects",
                                "field_type": "multiInputField",
                                "presentation_type": "table",
                                "question": [
                                    "Tell us about your project.",
                                    {
                                        "AeuWAj": {
                                            "column_title": "Project name",
                                            "type": "textField",
                                        },
                                        "tXQbHW": {
                                            "column_title": "Brief description of project",
                                            "type": "textField",
                                        },
                                        "ojLAmd": {
                                            "column_title": "Primary intervention",
                                            "type": "radiosField",
                                        },
                                        "YzhoTC": {
                                            "column_title": "Project status",
                                            "type": "radiosField",
                                        },
                                        "qaHSDG": {
                                            "column_title": "Name of delivery organisation",
                                            "type": "textField",
                                        },
                                    },
                                ],
                            },
                            {
                                "field_id": "dEyfRq",
                                "form_name": "pfn-rp-projects",
                                "field_type": "multiInputField",
                                "presentation_type": "table",
                                "question": [
                                    "",
                                    {
                                        "GeundE": {
                                            "column_title": "Type of organisation",
                                            "type": "textField",
                                        },
                                        "nYQcxZ": {
                                            "column_title": "Amount of funding allocated from the Plan for Neighbourhoods programme",
                                            "type": "numberField",
                                        },
                                        "EhzAeB": {
                                            "column_title": "Other sources of project funding",
                                            "type": "multilineTextField",
                                        },
                                        "HbiXPn": {
                                            "column_title": "Total project budget",
                                            "type": "numberField",
                                        },
                                    },
                                ],
                            },
                        ],
                    }
                ],
            },
            {
                "id": "additional-support",
                "name": "Additional support",
                "themes": [
                    {
                        "id": "additional-support",
                        "name": "Additional support",
                        "answers": [
                            {
                                "field_id": "NKLAZE",
                                "form_name": "pfn-rp-additional-support",
                                "field_type": "checkboxesField",
                                "presentation_type": "text",
                                "question": "Tell us which areas of support you may be interested in.",
                            },
                            {
                                "field_id": "BzezVX",
                                "form_name": "pfn-rp-additional-support",
                                "field_type": "textField",
                                "presentation_type": "text",
                                "question": "Other (please specify)",
                            },
                        ],
                    }
                ],
            },
        ],
    },
]
