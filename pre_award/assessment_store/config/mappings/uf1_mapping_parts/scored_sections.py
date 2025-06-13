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
                            {
                                "field_id": "WFRgIa",
                                "form_name": "uf1-organisation-information",
                                "field_type": "checkboxesField",
                                "presentation_type": "text",
                                "question": "Which categories of pre-approved interventions do you plan to fund?",
                            },
                        ],
                    }
                ],
            },
        ],
    }
]
