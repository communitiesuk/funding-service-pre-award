# ruff: noqa: E501

scored_sections = [
    {
        "id": "skills-and-experience",
        "weighting": 0.1,
        "name": "Skills and experience",
        "sub_criteria": [
            {
                "id": "skills-and-experience",
                "name": "Skills and experience",
                "themes": [
                    {
                        "id": "skills-and-experience",
                        "name": "Skills and experience",
                        "answers": [
                            {
                                "field_id": "uiRSYP",
                                "form_name": "ehcf-apply-skills-and-experience",
                                "field_type": "freeTextField",
                                "presentation_type": "text",
                                "question": "What are your organisation's objectives?",
                            },
                            {
                                "field_id": "AznHmY",
                                "form_name": "ehcf-apply-skills-and-experience",
                                "field_type": "freeTextField",
                                "presentation_type": "text",
                                "question": "What are your organisation's key activities?",
                            },
                            {
                                "field_id": "tTDkMm",
                                "form_name": "ehcf-apply-skills-and-experience",
                                "field_type": "freeTextField",
                                "presentation_type": "text",
                                "question": "Tell us about how your organisation has worked on similar previous projects.",
                            },
                        ],
                    }
                ],
            },
        ],
    },
    {
        "id": "ehcf-proposal-challenges",
        "weighting": 0.1,
        "name": "Proposal - Challenges",
        "sub_criteria": [
            {
                "id": "ehcf-proposal-challenges",
                "name": "Proposal - Challenges",
                "themes": [
                    {
                        "id": "ehcf-proposal-challenges",
                        "name": "Proposal - Challenges",
                        "answers": [
                            {
                                "field_id": "XCriZS",
                                "form_name": "ehcf-apply-proposal",
                                "field_type": "freeTextField",
                                "presentation_type": "text",
                                "question": "What challenges are you trying to address?",
                            },
                        ],
                    }
                ],
            },
        ],
    },
    {
        "id": "ehcf-proposal-project",
        "weighting": 0.3,
        "name": "Proposal - Project",
        "sub_criteria": [
            {
                "id": "ehcf-proposal-project",
                "name": "Proposal - Project",
                "themes": [
                    {
                        "id": "ehcf-proposal-project",
                        "name": "Proposal - Project",
                        "answers": [
                            {
                                "field_id": "MLxEMD",
                                "form_name": "ehcf-apply-proposal",
                                "field_type": "freeTextField",
                                "presentation_type": "text",
                                "question": "Tell us about your project.",
                            },
                        ],
                    }
                ],
            },
        ],
    },
    {
        "id": "deliverability-and-risks-milestones-project-plan-and-governance",
        "weighting": 0.25,
        "name": "Deliverability - Milestones, project plan and governance",
        "sub_criteria": [
            {
                "id": "deliverability-and-risks-milestones-project-plan-and-governance",
                "name": "Deliverability - Milestones, project plan and governance",
                "themes": [
                    {
                        "id": "deliverability-and-risks-milestones-project-plan-and-governance",
                        "name": "Deliverability - Milestones, project plan and governance",
                        "answers": [
                            {
                                "field_id": "puuNXQ",
                                "form_name": "ehcf-apply-deliverability-and-risks",
                                "field_type": "multiInputField",
                                "presentation_type": "table",
                                "question": [
                                    "What are your milestones?",
                                    {
                                        "OLCquZ": {
                                            "column_title": "Milestone",
                                            "type": "textField",
                                        },
                                        "vwkoml": {
                                            "column_title": "Date",
                                            "type": "DatePartsField",
                                        },
                                    },
                                ],
                            },
                            {
                                "field_id": "YXCLSe",
                                "form_name": "ehcf-apply-deliverability-and-risks",
                                "field_type": "clientSideFileUploadField",
                                "presentation_type": "s3bucketPath",
                                "question": "Upload your project plan showing key milestones",
                                "path": "upload-your-project-plan-showing-key-milestones",
                            },
                            {
                                "field_id": "HpgEVW",
                                "form_name": "ehcf-apply-deliverability-and-risks",
                                "field_type": "freeTextField",
                                "presentation_type": "text",
                                "question": "How will your project be managed?",
                            },
                        ],
                    }
                ],
            },
        ],
    },
    {
        "id": "deliverability-risk-management",
        "weighting": 0.05,
        "name": "Deliverability - Risk management",
        "sub_criteria": [
            {
                "id": "deliverability-risk-management",
                "name": "Deliverability - Risk management",
                "themes": [
                    {
                        "id": "deliverability-risk-management",
                        "name": "Deliverability - Risk management",
                        "answers": [
                            {
                                "field_id": "vEdcYf",
                                "form_name": "ehcf-apply-deliverability-and-risks",
                                "field_type": "multiInputField",
                                "presentation_type": "table",
                                "question": [
                                    "What risks are there to delivering your proposed project?",
                                    {
                                        "iJXHsl": {
                                            "column_title": "Risk",
                                            "type": "textField",
                                        },
                                        "fBmIqk": {
                                            "column_title": "Mitigation",
                                            "type": "textField",
                                        },
                                    },
                                ],
                            },
                            {
                                "field_id": "WdZCga",
                                "form_name": "ehcf-apply-deliverability-and-risks",
                                "field_type": "yesNoField",
                                "presentation_type": "text",
                                "question": "Does your proposed project include building works?",
                            },
                            {
                                "field_id": "PsOYFJ",
                                "form_name": "ehcf-apply-deliverability-and-risks",
                                "field_type": "radiosField",
                                "presentation_type": "text",
                                "question": "What is the ownership of the property?",
                            },
                            {
                                "field_id": "IRlgaq",
                                "form_name": "ehcf-apply-deliverability-and-risks",
                                "field_type": "textField",
                                "presentation_type": "text",
                                "question": "Who is the landlord?",
                            },
                            {
                                "field_id": "UKCuvb",
                                "form_name": "ehcf-apply-deliverability-and-risks",
                                "field_type": "datePartsField",
                                "presentation_type": "text",
                                "question": "When does the lease or licence expire?",
                            },
                            {
                                "field_id": "AbOWfn",
                                "form_name": "ehcf-apply-deliverability-and-risks",
                                "field_type": "freeTextField",
                                "presentation_type": "text",
                                "question": "Tell us about the purchase",
                            },
                            {
                                "field_id": "PMDKKL",
                                "form_name": "ehcf-apply-deliverability-and-risks",
                                "field_type": "freeTextField",
                                "presentation_type": "text",
                                "question": "Tell us about the lease",
                            },
                            {
                                "field_id": "tTuHtk",
                                "form_name": "ehcf-apply-deliverability-and-risks",
                                "field_type": "freeTextField",
                                "presentation_type": "text",
                                "question": "Have you engaged professional advisors on this project?",
                            },
                        ],
                    }
                ],
            },
        ],
    },
    {
        "id": "cost-and-value-for-money",
        "weighting": 0.1,
        "name": "Cost and value for money",
        "sub_criteria": [
            {
                "id": "cost-and-value-for-money",
                "name": "Cost and value for money",
                "themes": [
                    {
                        "id": "cost-and-value-for-money",
                        "name": "Cost and value for money",
                        "answers": [
                            {
                                "field_id": "ddPcod",
                                "form_name": "ehcf-apply-cost-and-value-for-money",
                                "field_type": "numberField",
                                "presentation_type": "text",
                                "question": "How much total funding are you applying for?",
                            },
                            {
                                "field_id": "vwpHzc",
                                "form_name": "ehcf-apply-cost-and-value-for-money",
                                "field_type": "radiosField",
                                "presentation_type": "text",
                                "question": "What type of funding are you applying for? ",
                            },
                            {
                                "field_id": "xVmfqS",
                                "form_name": "ehcf-apply-cost-and-value-for-money",
                                "field_type": "clientSideFileUploadField",
                                "presentation_type": "s3bucketPath",
                                "question": "<h3>Upload a budget for your project</h3>",
                                "path": "upload-a-budget-for-your-project-TvdQMR",
                            },
                            ### Revenue funding only
                            {
                                "field_id": "AltolX",
                                "form_name": "ehcf-apply-cost-and-value-for-money",
                                "field_type": "numberField",
                                "presentation_type": "text",
                                "question": """<h3><u>REVENUE FUNDING ONLY</u></h3>
                                                <h4>How much revenue funding are you applying for?</h4>Year 1
                                            """,
                            },
                            {
                                "field_id": "iFjBTZ",
                                "form_name": "ehcf-apply-cost-and-value-for-money",
                                "field_type": "numberField",
                                "presentation_type": "text",
                                "question": "Year 2",
                            },
                            {
                                "field_id": "hDxhyT",
                                "form_name": "ehcf-apply-cost-and-value-for-money",
                                "field_type": "numberField",
                                "presentation_type": "text",
                                "question": "Year 3",
                            },
                            ### Capital funding only
                            {
                                "field_id": "XFFfSR",
                                "form_name": "ehcf-apply-cost-and-value-for-money",
                                "field_type": "numberField",
                                "presentation_type": "text",
                                "question": """<h3><u>CAPITAL FUNDING ONLY</u></h3>
                                                <h4>How much capital funding are you applying for?</h4>
                                            """,
                            },
                            {
                                "field_id": "tTYUMj",
                                "form_name": "ehcf-apply-cost-and-value-for-money",
                                "field_type": "textField",
                                "presentation_type": "text",
                                "question": "Which year are you applying for?",
                            },
                            ### Both revenue and capital funding
                            {
                                "field_id": "MqmNSK",
                                "form_name": "ehcf-apply-cost-and-value-for-money",
                                "field_type": "numberField",
                                "presentation_type": "text",
                                "question": """<h3><u>BOTH REVENUE AND CAPITAL FUNDING</u></h3>
                                                <h4>How much revenue and capital funding are you applying for?</h4>
                                                Year 1
                                            """,
                            },
                            {
                                "field_id": "ithfkK",
                                "form_name": "ehcf-apply-cost-and-value-for-money",
                                "field_type": "numberField",
                                "presentation_type": "text",
                                "question": "Year 2",
                            },
                            {
                                "field_id": "UpaXDj",
                                "form_name": "ehcf-apply-cost-and-value-for-money",
                                "field_type": "numberField",
                                "presentation_type": "text",
                                "question": "Year 3",
                            },
                            {
                                "field_id": "ANkbOG",
                                "form_name": "ehcf-apply-cost-and-value-for-money",
                                "field_type": "numberField",
                                "presentation_type": "text",
                                "question": "How much capital funding are you applying for?",
                            },
                            {
                                "field_id": "ZlklVZ",
                                "form_name": "ehcf-apply-cost-and-value-for-money",
                                "field_type": "textField",
                                "presentation_type": "text",
                                "question": "Which year are you applying for?",
                            },
                        ],
                    }
                ],
            },
        ],
    },
    {
        "id": "outcomes-and-measuring-impact",
        "weighting": 0.1,
        "name": "Outcomes and measuring impact",
        "sub_criteria": [
            {
                "id": "outcomes-and-measuring-impact",
                "name": "Outcomes and measuring impact",
                "themes": [
                    {
                        "id": "outcomes-and-measuring-impact",
                        "name": "Outcomes and measuring impact",
                        "answers": [
                            {
                                "field_id": "ffVtZC",
                                "form_name": "ehcf-apply-outcomes-and-measuring-impact",
                                "field_type": "freeTextField",
                                "presentation_type": "text",
                                "question": "How will this project improve how partners work together to respond to local need?",
                            },
                            {
                                "field_id": "WaRxZy",
                                "form_name": "ehcf-apply-outcomes-and-measuring-impact",
                                "field_type": "freeTextField",
                                "presentation_type": "text",
                                "question": "Describe the measurable positive impacts your project is expected to have",
                            },
                        ],
                    }
                ],
            },
        ],
    },
]
