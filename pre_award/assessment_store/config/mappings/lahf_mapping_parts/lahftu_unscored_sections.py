# ruff: noqa: E501

unscored_sections = [
    {
        "id": "unscored",
        "name": "Unscored",
        "sub_criteria": [
            {
                "id": "local_authority_details",
                "name": "Local authority details",
                "themes": [
                    {
                        "id": "local_authority_details",
                        "name": "Local authority details",
                        "answers": [
                            {
                                "field_id": "svIchm",
                                "form_name": "lahf-lahftu-local-authority-details",
                                "field_type": "textField",
                                "presentation_type": "text",
                                "question": "What is the name of your local authority?",
                            },
                            {
                                "field_id": "vDsLGm",
                                "form_name": "lahf-lahftu-local-authority-details",
                                "field_type": "textField",
                                "presentation_type": "text",
                                "question": "Full name",
                            },
                            {
                                "field_id": "gNJDlH",
                                "form_name": "lahf-lahftu-local-authority-details",
                                "field_type": "textField",
                                "presentation_type": "text",
                                "question": "Role",
                            },
                            {
                                "field_id": "saBdpT",
                                "form_name": "lahf-lahftu-local-authority-details",
                                "field_type": "emailAddressField",
                                "presentation_type": "text",
                                "question": "Email address",
                            },
                        ],
                    }
                ],
            },
            {
                "id": "occupational_therapy_report",
                "name": "Occupational therapy report",
                "themes": [
                    {
                        "id": "occupational_therapy_report",
                        "name": "Occupational therapy report",
                        "answers": [
                            {
                                "field_id": "CesJKe",
                                "form_name": "lahf-lahftu-occupational-therapy-report",
                                "field_type": "datePartsField",
                                "presentation_type": "text",
                                "question": "What date was the occupational therapy assessment completed?",
                            },
                            {
                                "field_id": "ZDLjys",
                                "form_name": "lahf-lahftu-occupational-therapy-report",
                                "field_type": "clientSideFileUploadField",
                                "presentation_type": "s3bucketPath",
                                "question": "Upload the occupational therapy report",
                                "path": "upload-your-occupational-therapy-report",
                            },
                        ],
                    }
                ],
            },
            {
                "id": "property_details",
                "name": "Property details",
                "themes": [
                    {
                        "id": "property_details",
                        "name": "Property details",
                        "answers": [
                            {
                                "field_id": "qnaoFo",
                                "form_name": "lahf-lahftu-property-details",
                                "field_type": "ukAddressField",
                                "presentation_type": "address",
                                "question": "What is the address of the property?",
                            },
                            {
                                "field_id": "ZoWdNb",
                                "form_name": "lahf-lahftu-property-details",
                                "field_type": "numberField",
                                "presentation_type": "text",
                                "question": "Number of bedrooms",
                            },
                            {
                                "field_id": "XRMMJp",
                                "form_name": "lahf-lahftu-property-details",
                                "field_type": "numberField",
                                "presentation_type": "text",
                                "question": "Number of bathrooms",
                            },
                            {
                                "field_id": "YlnYVH",
                                "form_name": "lahf-lahftu-property-details",
                                "field_type": "numberField",
                                "presentation_type": "text",
                                "question": "Number of other rooms",
                            },
                            {
                                "field_id": "SpbeNL",
                                "form_name": "lahf-lahftu-property-details",
                                "field_type": "numberField",
                                "presentation_type": "text",
                                "question": "Number of floors",
                            },
                            {
                                "field_id": "upqiVf",
                                "form_name": "lahf-lahftu-property-details",
                                "field_type": "radiosField",
                                "presentation_type": "text",
                                "question": "What is the current status of the property?",
                            },
                        ],
                    }
                ],
            },
            {
                "id": "additional_information",
                "name": "Additional information",
                "themes": [
                    {
                        "id": "additional_information",
                        "name": "Additional information",
                        "answers": [
                            {
                                "field_id": "ANNmgX",
                                "form_name": "lahf-lahftu-additional-information",
                                "field_type": "freeTextField",
                                "presentation_type": "text",
                                "question": "Tell us any additional information that you feel is relevant to support this application (optional)",
                            },
                        ],
                    }
                ],
            },
        ],
    },
    {
        "id": "declarations",
        "name": "Declarations",
        "sub_criteria": [
            {
                "id": "declarations",
                "name": "Declarations",
                "themes": [
                    {
                        "id": "declarations",
                        "name": "Declarations",
                        "answers": [
                            {
                                "field_id": "MumnzN",
                                "form_name": "lahf-lahftu-declarations",
                                "field_type": "freeTextField",
                                "presentation_type": "text",
                                "question": "Confirm that you have read and agree with the following declarations.",
                            },
                            {
                                "field_id": "CzMnku",
                                "form_name": "lahf-lahftu-declarations",
                                "field_type": "checkboxesField",
                                "presentation_type": "text",
                                "question": "I confirm that I have read and agree with the declarations",
                            },
                        ],
                    },
                ],
            },
        ],
    },
]
