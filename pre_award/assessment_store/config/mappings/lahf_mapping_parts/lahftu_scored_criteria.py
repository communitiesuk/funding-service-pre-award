# ruff: noqa: E501

scored_sections = [
    {
        "id": "adaptation_requirements_suitability",
        "weighting": 0.3,
        "name": "Adaptation requirements - Suitability of proposed adaptations",
        "sub_criteria": [
            {
                "id": "adaptation_suitability",
                "name": "Suitability of proposed adaptations",
                "themes": [
                    {
                        "id": "adaptation_suitability",
                        "name": "Suitability of proposed adaptations",
                        "answers": [
                            {
                                "field_id": "uvAgKD",
                                "form_name": "lahf-lahftu-adaptation-requirements",
                                "field_type": "freeTextField",
                                "presentation_type": "text",
                                "question": "Tell us what adaptations are required on the property.",
                            },
                        ],
                    }
                ],
            },
        ],
    },
    {
        "id": "adaptation_requirements_cost_assessment",
        "weighting": 0.3,
        "name": "Adaptation requirements - Cost assessment",
        "sub_criteria": [
            {
                "id": "cost_assessment",
                "name": "Cost assessment",
                "themes": [
                    {
                        "id": "cost_assessment",
                        "name": "Cost assessment",
                        "answers": [
                            {
                                "field_id": "DdMauS",
                                "form_name": "lahf-lahftu-adaptation-requirements",
                                "field_type": "numberField",
                                "presentation_type": "text",
                                "question": "How much funding are you applying for in total?",
                            },
                            {
                                "field_id": "vSyica",
                                "form_name": "lahf-lahftu-adaptation-requirements",
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
                                "form_name": "lahf-lahftu-adaptation-requirements",
                                "field_type": "clientSideFileUploadField",
                                "presentation_type": "s3bucketPath",
                                "question": "Upload itemised quotes listing the costs and installation fees associated with the adaptations.",
                                "path": "upload-itemised-quotes-listing-the-costs-and-installation-fees-associated-with-the-adaptations",
                            },
                            {
                                "field_id": "dIadTN",
                                "form_name": "lahf-lahftu-adaptation-requirements",
                                "field_type": "yesNoField",
                                "presentation_type": "text",
                                "question": "Are you requesting funding to cover void rent costs?",
                            },
                            {
                                "field_id": "CuwIiM",
                                "form_name": "lahf-lahftu-adaptation-requirements",
                                "field_type": "clientSideFileUploadField",
                                "presentation_type": "s3bucketPath",
                                "question": "Upload evidence of rent forgone, including the relevant time period.",
                                "path": "upload-evidence-of-rent-forgone-including-the-relevant-time-period",
                            },
                            {
                                "field_id": "Czqzcm",
                                "form_name": "lahf-lahftu-adaptation-requirements",
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
    {
        "id": "delivery_timeline_feasibility",
        "weighting": 0.4,
        "name": "Delivery timeline - Timeline feasibility",
        "sub_criteria": [
            {
                "id": "timeline_feasibility",
                "name": "Timeline feasibility",
                "themes": [
                    {
                        "id": "timeline_feasibility",
                        "name": "Timeline feasibility",
                        "answers": [
                            {
                                "field_id": "LQoFlz",
                                "form_name": "lahf-lahftu-key-dates",
                                "field_type": "datePartsField",
                                "presentation_type": "text",
                                "question": "Target commencement date",
                            },
                            {
                                "field_id": "QXDTBI",
                                "form_name": "lahf-lahftu-key-dates",
                                "field_type": "datePartsField",
                                "presentation_type": "text",
                                "question": "Target completion date",
                            },
                            {
                                "field_id": "JIuDIp",
                                "form_name": "lahf-lahftu-key-dates",
                                "field_type": "datePartsField",
                                "presentation_type": "text",
                                "question": "Estimated move-in date",
                            },
                        ],
                    }
                ],
            },
        ],
    },
]
