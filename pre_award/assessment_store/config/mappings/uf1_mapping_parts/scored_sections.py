# ruff: noqa: E501

scored_sections = [
    {
        "id": "project_details",
        "weighting": 1.0,
        "name": "Project details",
        "sub_criteria": [
            {
                "id": "project_details",
                "name": "Project details",
                "themes": [
                    {
                        "id": "project_details",
                        "name": "Project details",
                        "answers": [
                            {
                                "field_id": "VcyKVN",
                                "form_name": "uf1-project-details",
                                "field_type": "textField",
                                "presentation_type": "text",
                                "question": "Project name",
                            },
                            {
                                "field_id": "KJtdhs",
                                "form_name": "uf1-project-details",
                                "field_type": "freeTextField",
                                "presentation_type": "text",
                                "question": "Project overview",
                            },
                            {
                                "field_id": "SqqyyB",
                                "form_name": "uf1-project-details",
                                "field_type": "clientSideFileUploadField",
                                "presentation_type": "s3bucketPath",
                                "question": "Upload the quote for the project",
                                "path": "upload-file",
                            },
                            {
                                # These 2 fields are capital and revenue funding respectively
                                "field_id": ["YQGJbm", "VmCcNW"],
                                "form_name": "",
                                "field_type": "numberField",
                                "presentation_type": "grouped_fields",
                                "question": [
                                    "2026-27",
                                    "2027-28",
                                ],
                            },
                            {
                                "field_id": "ZaxlkA",
                                "form_name": "uf1-project-details",
                                "field_type": "multiInputField",
                                "presentation_type": "table",
                                "question": [
                                    "Programme delivery funding - revenue",
                                    {
                                        "YQGJbm": {
                                            "column_title": "2026-27",
                                            "type": "numberField",
                                        },
                                        "VmCcNW": {
                                            "column_title": "2027-28",
                                            "type": "numberField",
                                        },
                                        "pCCkfZ": {
                                            "column_title": "2028-29",
                                            "type": "numberField",
                                        },
                                        "aaOhAH": {
                                            "column_title": "2029-30",
                                            "type": "numberField",
                                        },
                                        "ehgQSG": {
                                            "column_title": "2030-31",
                                            "type": "numberField",
                                        },
                                        "mmMPXd": {
                                            "column_title": "2031-32",
                                            "type": "numberField",
                                        },
                                    },
                                ],
                            },
                            {
                                "field_id": "ZaxlkA",
                                "form_name": "funding-required-cof",
                                "field_type": "multiInputField",
                                "presentation_type": "table",
                                "question": [
                                    "",
                                    {
                                        "iLMwbk": {
                                            "column_title": "2032-33",
                                            "type": "numberField",
                                        },
                                        "ThaiNt": {
                                            "column_title": "2033-34",
                                            "type": "numberField",
                                        },
                                        "ROCfYU": {
                                            "column_title": "2034-35",
                                            "type": "numberField",
                                        },
                                        "qMNUxP": {
                                            "column_title": "2035-36",
                                            "type": "numberField",
                                        },
                                        "mmMPXd": {
                                            "column_title": "2036-37",
                                            "type": "numberField",
                                        },
                                        "ROCfYUa": {
                                            "column_title": "2037-38",
                                            "type": "numberField",
                                        },
                                    },
                                ],
                            },
                            {
                                "field_id": "igStco",
                                "form_name": "uf1-project-details",
                                "field_type": "multiInputField",
                                "presentation_type": "table",
                                "question": [
                                    "Programme delivery funding - capital",
                                    {
                                        "JoEKPs": {
                                            "column_title": "2026-27",
                                            "type": "numberField",
                                        },
                                        "MaHzlK": {
                                            "column_title": "2027-28",
                                            "type": "numberField",
                                        },
                                        "cSAvLl": {
                                            "column_title": "2028-29",
                                            "type": "numberField",
                                        },
                                        "lXHVDo": {
                                            "column_title": "2029-30",
                                            "type": "numberField",
                                        },
                                        "yksYVj": {
                                            "column_title": "2030-31",
                                            "type": "numberField",
                                        },
                                    },
                                ],
                            },
                            {
                                "field_id": "igStco",
                                "form_name": "funding-required-cof",
                                "field_type": "multiInputField",
                                "presentation_type": "table",
                                "question": [
                                    "",
                                    {
                                        "foBOGa": {
                                            "column_title": "2031-32",
                                            "type": "numberField",
                                        },
                                        "BmNYxJ": {
                                            "column_title": "2032-33",
                                            "type": "numberField",
                                        },
                                        "UYiAHd": {
                                            "column_title": "2033-34",
                                            "type": "numberField",
                                        },
                                        "LzXJTJ": {
                                            "column_title": "2034-35",
                                            "type": "numberField",
                                        },
                                        "LwEzPI": {
                                            "column_title": "2035-36",
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
                "id": "organisation_information",
                "name": "Organisation information",
                "themes": [
                    {
                        "id": "organisation_information",
                        "name": "Organisation information",
                        "answers": [
                            {
                                "field_id": "yptqZX",
                                "form_name": "uf1-organisation-information",
                                "field_type": "textField",
                                "presentation_type": "text",
                                "question": "Organisation name",
                            },
                            {
                                "field_id": "BIxPht",
                                "form_name": "uf1-organisation-information",
                                "field_type": "yesNoField",
                                "presentation_type": "text",
                                "question": "Does your organisation use any  other names?",
                            },
                            {
                                "field_id": "Ianpnw",
                                "form_name": "uf1-organisation-information",
                                "field_type": "textField",
                                "presentation_type": "text",
                                "question": "Alternative name 1",
                            },
                            {
                                "field_id": "CTyQWf",
                                "form_name": "uf1-organisation-information",
                                "field_type": "textField",
                                "presentation_type": "text",
                                "question": "Alternative name 2",
                            },
                            {
                                "field_id": "XWsTKi",
                                "form_name": "uf1-organisation-information",
                                "field_type": "textField",
                                "presentation_type": "text",
                                "question": "Alternative name 3",
                            },
                        ],
                    }
                ],
            },
        ],
    }
]
