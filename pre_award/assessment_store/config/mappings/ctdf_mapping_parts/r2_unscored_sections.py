# ruff: noqa: E501

unscored_sections = [
    {
        "id": "organisation_info",
        "name": "Organisation Information",
        "sub_criteria": [
            {
                "id": "org_details",
                "name": "Organisation Details",
                "themes": [
                    {
                        "id": "general_details",
                        "name": "General Details",
                        "answers": [
                            {
                                "field_id": "orgName",
                                "form_name": "ctdf-r2-organisation-information",
                                "field_type": "textField",
                                "presentation_type": "text",
                                "question": "Organisation Name",
                            },
                            {
                                "field_id": "hasAltName",
                                "form_name": "ctdf-r2-organisation-information",
                                "field_type": "yesNoField",
                                "presentation_type": "text",
                                "question": "Has Alternative Name",
                            },
                            {
                                "field_id": "altName1",
                                "form_name": "ctdf-r2-organisation-information",
                                "field_type": "textField",
                                "presentation_type": "text",
                                "question": "Alternative Name 1",
                            },
                            {
                                "field_id": "altName2",
                                "form_name": "ctdf-r2-organisation-information",
                                "field_type": "textField",
                                "presentation_type": "text",
                                "question": "Alternative Name 2",
                            },
                            {
                                "field_id": "orgAddress",
                                "form_name": "ctdf-r2-organisation-information",
                                "field_type": "ukAddressField",
                                "presentation_type": "text",
                                "question": "Address",
                            },
                        ],
                    },
                    {
                        "id": "org_type_info",
                        "name": "Organisation Type Information",
                        "answers": [
                            {
                                "field_id": "orgType",
                                "form_name": "ctdf-r2-organisation-information",
                                "field_type": "radiosField",
                                "presentation_type": "text",
                                "question": "Organisation Type",
                            },
                            {
                                "field_id": "charityNumber",
                                "form_name": "ctdf-r2-organisation-information",
                                "field_type": "textField",
                                "presentation_type": "text",
                                "question": "Charity Number",
                            },
                            {
                                "field_id": "charityRegDate",
                                "form_name": "ctdf-r2-organisation-information",
                                "field_type": "datePartsField",
                                "presentation_type": "text",
                                "question": "Charity Registration Date",
                            },
                            {
                                "field_id": "cicNumber",
                                "form_name": "ctdf-r2-organisation-information",
                                "field_type": "textField",
                                "presentation_type": "text",
                                "question": "CIC Number",
                            },
                            {
                                "field_id": "cicAssetLock",
                                "form_name": "ctdf-r2-organisation-information",
                                "field_type": "freeTextField",
                                "presentation_type": "text",
                                "question": "CIC Asset Lock",
                            },
                            {
                                "field_id": "laName",
                                "form_name": "ctdf-r2-organisation-information",
                                "field_type": "textField",
                                "presentation_type": "text",
                                "question": "Local Authority Name",
                            },
                            {
                                "field_id": "laType",
                                "form_name": "ctdf-r2-organisation-information",
                                "field_type": "radiosField",
                                "presentation_type": "text",
                                "question": "Local Authority Type",
                            },
                            {
                                "field_id": "otherOrgType",
                                "form_name": "ctdf-r2-organisation-information",
                                "field_type": "textField",
                                "presentation_type": "text",
                                "question": "Other Organisation Type",
                            },
                            {
                                "field_id": "hasGoverningDoc",
                                "form_name": "ctdf-r2-organisation-information",
                                "field_type": "yesNoField",
                                "presentation_type": "text",
                                "question": "Has Governing Document",
                            },
                        ],
                    },
                ],
            },
        ],
    },
    {
        "id": "declarations",
        "name": "Declarations",
        "sub_criteria": [
            {
                "id": "declarations_sub",
                "name": "Declarations",
                "themes": [
                    {
                        "id": "all_declarations",
                        "name": "All Declarations",
                        "answers": [
                            {
                                "field_id": "accuracyDeclaration",
                                "form_name": "ctdf-r2-declarations",
                                "field_type": "checkboxesField",
                                "presentation_type": "list",
                                "question": "Accuracy Declaration",
                            },
                            {
                                "field_id": "authorityDeclaration",
                                "form_name": "ctdf-r2-declarations",
                                "field_type": "checkboxesField",
                                "presentation_type": "list",
                                "question": "Authority Declaration",
                            },
                            {
                                "field_id": "termsDeclaration",
                                "form_name": "ctdf-r2-declarations",
                                "field_type": "checkboxesField",
                                "presentation_type": "list",
                                "question": "Terms Declaration",
                            },
                            {
                                "field_id": "dataDeclaration",
                                "form_name": "ctdf-r2-declarations",
                                "field_type": "checkboxesField",
                                "presentation_type": "list",
                                "question": "Data Declaration",
                            },
                        ],
                    },
                ],
            },
        ],
    },
    {
        "id": "supporting_documents",
        "name": "Supporting Documents",
        "sub_criteria": [
            {
                "id": "uploaded_files",
                "name": "Uploaded Files",
                "themes": [
                    {
                        "id": "uploads",
                        "name": "Uploads",
                        "answers": [
                            {
                                "field_id": "supportingDocs",
                                "form_name": "ctdf-r2-supporting-evidence",
                                "field_type": "clientSideFileUploadField",
                                "presentation_type": "file",
                                "question": "Supporting Documents",
                            },
                        ],
                    },
                ],
            },
        ],
    },
]
