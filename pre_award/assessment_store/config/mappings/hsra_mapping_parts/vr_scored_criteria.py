# ruff: noqa: E501

scored_criteria = [
    {
        "id": "designated-area-details",
        "name": "Designated area details",
        "weighting": 0.33,
        "sub_criteria": [
            {
                "id": "designated-area-details-hsra-vr",
                "name": "Designated area details",
                "themes": [
                    {
                        "id": "which-town-or-city-will-the-designated-area-be-located-in?",
                        "name": "Which town or city will the designated area be located in?",
                        "answers": [
                            {
                                "field_id": "frDgtU",
                                "form_name": "designated-area-details-hsra-vr",
                                "field_type": "textField",
                                "presentation_type": "text",
                                "question": "Which town or city will the designated area be located in?",
                            }
                        ],
                    },
                    {
                        "id": "tell-us-more-about-the-designated-area.",
                        "name": "Tell us more about the designated area.",
                        "answers": [
                            {
                                "field_id": "YMqcPf",
                                "form_name": "designated-area-details-hsra-vr",
                                "field_type": "multilineTextField",
                                "presentation_type": "text",
                                "question": "Tell us more about the designated area.",
                            }
                        ],
                    },
                ],
            },
        ],
    },
    {
        "id": "milestones",
        "name": "Milestones",
        "weighting": 0.33,
        "sub_criteria": [
            {
                "id": "milestones-hsra-vr",
                "name": "Milestones",
                "themes": [
                    {
                        "id": "when-do-you-expect-the-vacancy-register-to-be-completed?",
                        "name": "When do you expect the vacancy register to be completed?",
                        "answers": [
                            {
                                "field_id": "yvpmIv",
                                "form_name": "milestones-hsra-vr",
                                "field_type": "datePartsField",
                                "presentation_type": "text",
                                "question": "When do you expect the vacancy register to be completed?",
                            }
                        ],
                    },
                    {
                        "id": "when-do-you-expect-the-post-payment-assurance-form-to-be-submitted?",
                        "name": "When do you expect the post-payment assurance form to be submitted?",
                        "answers": [
                            {
                                "field_id": "KFjxBs",
                                "form_name": "milestones-hsra-vr",
                                "field_type": "datePartsField",
                                "presentation_type": "text",
                                "question": "When do you expect to submit your post-payment assurance form to be submitted?",
                            }
                        ],
                    },
                ],
            },
        ],
    },
    {
        "id": "project-costs",
        "name": "Project costs",
        "weighting": 0.33,
        "sub_criteria": [
            {
                "id": "project-costs-hsra-vr",
                "name": "Project costs",
                "themes": [
                    {
                        "id": "how-much-funding-are-you-applying-for?",
                        "name": "How much funding are you applying for?",
                        "answers": [
                            {
                                "field_id": "MIrLuu",
                                "form_name": "project-costs-hsra-vr",
                                "field_type": "numberField",
                                "presentation_type": "text",
                                "question": "How much funding are you applying for?",
                            }
                        ],
                    },
                    {
                        "id": "upload-the-quote-for-the-vacancy-register",
                        "name": "Upload the quote for the vacancy register",
                        "answers": [
                            {
                                "field_id": "SqqyyB",
                                "form_name": "project-costs-hsra-vr",
                                "field_type": "clientSideFileUploadField",
                                "presentation_type": "s3bucketPath",
                                "question": "Upload the quote for the vacancy register",
                                "path": "upload-the-quote-for-the-vacancy-register",
                            }
                        ],
                    },
                ],
            },
        ],
    },
]
