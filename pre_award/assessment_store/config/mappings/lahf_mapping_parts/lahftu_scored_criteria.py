# ruff: noqa: E501

scored_sections = [
    {
        "id": "occupational_therapy_report",
        "weighting": 0.4,
        "name": "Occupational therapy report",
        "sub_criteria": [
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
        ],
    },
    {
        "id": "property_details",
        "weighting": 0.3,
        "name": "Property details",
        "sub_criteria": [
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
                                "presentation_type": "integer",
                                "question": "Number of Bedrooms",
                            },
                            {
                                "field_id": "XRMMJp",
                                "form_name": "lahf-lahftu-property-details",
                                "field_type": "numberField",
                                "presentation_type": "integer",
                                "question": "Number of Bathrooms",
                            },
                            {
                                "field_id": "upqiVf",
                                "form_name": "lahf-lahftu-property-details",
                                "field_type": "radiosField",
                                "presentation_type": "text",
                                "question": "What is the current status of the property?",
                            },
                            {
                                "field_id": "NXsAYk",
                                "form_name": "lahf-lahftu-property-details",
                                "field_type": "freeTextField",
                                "presentation_type": "text",
                                "question": "Tell us how the property would meet the household's adaptation or accessibility requirements.",
                            },
                        ],
                    }
                ],
            },
        ],
    },
    {
        "id": "funding_requests",
        "weighting": 0.3,
        "name": "Funding requests",
        "sub_criteria": [
            {
                "id": "funding_requests",
                "name": "Funding requests",
                "themes": [
                    {
                        "id": "funding_requests",
                        "name": "Funding requests",
                        "answers": [
                            {
                                "field_id": "DdMauS",
                                "form_name": "lahf-lahftu-funding-requests",
                                "field_type": "numberField",
                                "presentation_type": "text",
                                "question": "How much funding are you applying for in total?",
                            },
                            {
                                "field_id": "vSyica",
                                "form_name": "lahf-lahftu-funding-requests",
                                "field_type": "multiInputField",
                                "presentation_type": "table",
                                "question": [
                                    "Give a detailed breakdown of the costs for which funding is being requested.",
                                    {
                                        "jEhzec": {
                                            "column_title": "Brief description",
                                            "type": "textField",
                                        },
                                        "MUtVpb": {
                                            "column_title": "Amount of funding requested",
                                            "type": "numberField",
                                        },
                                    },
                                ],
                            },
                            {
                                "field_id": "LbqcYE",
                                "form_name": "lahf-lahftu-funding-requests",
                                "field_type": "clientSideFileUploadField",
                                "presentation_type": "s3bucketPath",
                                "question": "Upload evidence to support the funding you are applying for.",
                                "path": "upload-evidence-to-support-the-funding-you-are-applying-for",
                            },
                            {
                                "field_id": "dIadTN",
                                "form_name": "lahf-lahftu-funding-requests",
                                "field_type": "yesNoField",
                                "presentation_type": "text",
                                "question": "Are you requesting funding to cover void rent costs?",
                            },
                            {
                                "field_id": "ySXgFg",
                                "form_name": "lahf-lahftu-funding-requests",
                                "field_type": "numberField",
                                "presentation_type": "text",
                                "question": "How much funding in total are you requesting to cover void costs?",
                            },
                            {
                                "field_id": "wDWTMQ",
                                "form_name": "lahf-lahftu-funding-requests",
                                "field_type": "datePartsField",
                                "presentation_type": "text",
                                "question": "Start date",
                            },
                            {
                                "field_id": "qsulAz",
                                "form_name": "lahf-lahftu-funding-requests",
                                "field_type": "datePartsField",
                                "presentation_type": "text",
                                "question": "End date",
                            },
                            {
                                "field_id": "CuwIiM",
                                "form_name": "lahf-lahftu-funding-requests",
                                "field_type": "clientSideFileUploadField",
                                "presentation_type": "s3bucketPath",
                                "question": "Upload evidence of rent forgone, including the relevant time period.",
                                "path": "upload-evidence-of-rent-forgone-including-the-relevant-time-period",
                            },
                            {
                                "field_id": "Czqzcm",
                                "form_name": "lahf-lahftu-funding-requests",
                                "field_type": "freeTextField",
                                "presentation_type": "text",
                                "question": "Any additional information about the evidence uploaded (optional)",
                            },
                        ],
                    }
                ],
            },
        ],
    },
]
