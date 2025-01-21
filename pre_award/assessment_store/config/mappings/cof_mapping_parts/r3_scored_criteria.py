# ruff: noqa: E501

scored_criteria = [
    {
        "id": "strategic_case",
        "name": "Strategic case",
        "weighting": 0.53,
        "sub_criteria": [
            {
                "id": "community_use",
                "name": "Community use",
                "themes": [
                    {
                        "id": "community_use",
                        "name": "Community use",
                        "answers": [
                            {
                                "field_id": "Ieudgn",
                                "form_name": "community-use-cof-r3-w1",
                                "field_type": "freeTextField",
                                "presentation_type": "free_text",
                                "question": "Explain how the community will be better served with the asset under community ownership",
                            },
                            {
                                "field_id": "zTcrYo",
                                "form_name": "community-use-cof-r3-w1",
                                "field_type": "freeTextField",
                                "presentation_type": "free_text",
                                "question": "Who in the community currently uses the asset, or has used it in the past?",
                            },
                            {
                                "field_id": "bEWpAj",
                                "form_name": "project-information-cof-r3-w1",
                                "field_type": "freeTextField",
                                "presentation_type": "free_text",
                                "question": "Tell us how the asset is currently being used, or how it has been used before, and why it's important to the community",
                            },
                        ],
                    },
                    {
                        "id": "risk_loss_impact",
                        "name": "Risk and impact of loss",
                        "answers": [
                            {
                                "field_id": "NGSXHE",
                                "form_name": "community-use-cof-r3-w1",
                                "field_type": "freeTextField",
                                "presentation_type": "free_text",
                                "question": "Why will the asset be lost without community intervention?",
                            },
                            {
                                "field_id": "whlRYS",
                                "form_name": "community-use-cof-r3-w1",
                                "field_type": "freeTextField",
                                "presentation_type": "free_text",
                                "question": "Tell us how losing the asset would affect, or has already affected, people in the community",
                            },
                            {
                                "field_id": "KQlOaJ",
                                "form_name": "asset-information-cof-r3-w1",
                                "field_type": "checkboxesField",
                                "presentation_type": "list",
                                "question": "Why is the asset at risk of closure?",
                            },
                        ],
                    },
                ],
            },
            {
                "id": "engagement",
                "name": "Engagement",
                "themes": [
                    {
                        "id": "engaging-the-community",
                        "name": "Engaging the community",
                        "answers": [
                            {
                                "field_id": "azCutK",
                                "form_name": "community-engagement-cof-r3-w1",
                                "field_type": "freeTextField",
                                "presentation_type": "free_text",
                                "question": "Tell us how you have engaged with the community about your intention to take ownership of the asset",
                            },
                            {
                                "field_id": "jAhuWN",
                                "form_name": "community-engagement-cof-r3-w1",
                                "field_type": "freeTextField",
                                "presentation_type": "free_text",
                                "question": "Describe your fundraising activities?",
                            },
                        ],
                    },
                    {
                        "id": "local-support",
                        "name": "Local support",
                        "answers": [
                            {
                                "field_id": "GGBgBY",
                                "form_name": "community-engagement-cof-r3-w1",
                                "field_type": "freeTextField",
                                "presentation_type": "free_text",
                                "question": "Tell us how your project supports any wider local plans",
                            },
                            {
                                "field_id": "tDVPnl",
                                "form_name": "local-support-cof-r3-w1",
                                "field_type": "freeTextField",
                                "presentation_type": "free_text",
                                "question": "Tell us about the local support for your project",
                            },
                            {
                                "field_id": "bDWjTN",
                                "form_name": "local-support-cof-r3-w1",
                                "field_type": "clientSideFileUploadField",
                                "presentation_type": "s3bucketPath",
                                "question": "Upload supporting evidence (optional)",
                                "path": "your-support-for-the-project",
                            },
                        ],
                    },
                ],
            },
            {
                "id": "benefits",
                "name": "Benefits",
                "themes": [
                    {
                        "id": "delivering_and_sustaining_benefits",
                        "name": "Delivering and sustaining benefits",
                        "answers": [
                            {
                                "field_id": "pqYxJO",
                                "form_name": "community-benefits-cof-r3-w1",
                                "field_type": "checkboxesField",
                                "presentation_type": "list",
                                "question": "What community benefits do you expect to deliver with this project?",
                            },
                            {
                                "field_id": "lgfiGB",
                                "form_name": "community-benefits-cof-r3-w1",
                                "field_type": "freeTextField",
                                "presentation_type": "free_text",
                                "question": "Tell us about these benefits in detail, and how the asset's activities will help deliver them",
                            },
                            {
                                "field_id": "zKKouR",
                                "form_name": "community-benefits-cof-r3-w1",
                                "field_type": "freeTextField",
                                "presentation_type": "free_text",
                                "question": "Explain how you plan to deliver and sustain these benefits over time",
                            },
                        ],
                    },
                    {
                        "id": "benefitting_the_whole_community",
                        "name": "Benefitting the whole community",
                        "answers": [
                            {
                                "field_id": "ZyIQGI",
                                "form_name": "community-benefits-cof-r3-w1",
                                "field_type": "freeTextField",
                                "presentation_type": "free_text",
                                "question": "Tell us how you'll make sure the whole community benefits from the asset",
                            },
                        ],
                    },
                ],
            },
            {
                "id": "environmental_sustainability",
                "name": "Environmental sustainability",
                "themes": [
                    {
                        "id": "environmental-considerations",
                        "name": "Environmental considerations",
                        "answers": [
                            {
                                "field_id": "dypuJs",
                                "form_name": "environmental-sustainability-cof-r3-w1",
                                "field_type": "freeTextField",
                                "presentation_type": "free_text",
                                "question": "Tell us how you have considered the environmental sustainability of your project",
                            }
                        ],
                    }
                ],
            },
        ],
    },
    {
        "id": "management_case",
        "name": "Management case",
        "weighting": 0.47,
        "sub_criteria": [
            {
                "id": "funding_breakdown",
                "name": "Funding breakdown",
                "themes": [
                    {
                        "id": "funding_requested",
                        "name": "Funding requested",
                        "answers": [
                            {
                                "field_id": "ABROnB",
                                "form_name": "funding-required-cof-r3-w1",
                                "field_type": "numberField",
                                "presentation_type": "currency",
                                "question": "Capital funding",
                            },
                            {
                                "field_id": "cLDRvN",
                                "form_name": "funding-required-cof-r3-w1",
                                "field_type": "numberField",
                                "presentation_type": "currency",
                                "question": "Revenue funding (optional)",
                            },
                            {
                                "field_id": "qQLyXL",
                                "form_name": "funding-required-cof-r3-w1",
                                "field_type": "multiInputField",
                                "presentation_type": "table",
                                "question": [
                                    "Capital costs",
                                    {
                                        "GLQlOh": {
                                            "column_title": "Describe the cost",
                                            "type": "textField",
                                        },
                                        "JtwkMy": {
                                            "column_title": "Amount",
                                            "type": "numberField",
                                        },
                                    },
                                ],
                            },
                            {
                                "field_id": "DOvZvB",
                                "form_name": "funding-required-cof-r3-w1",
                                "field_type": "yesNoField",
                                "presentation_type": "text",
                                "question": "Have you secured any match funding yet?",
                            },
                            {
                                "field_id": "MopCmv",
                                "form_name": "funding-required-cof-r3-w1",
                                "field_type": "multiInputField",
                                "presentation_type": "table",
                                "question": [
                                    "Secured match funding",
                                    {
                                        "JKqLWU": {
                                            "column_title": "Source of secured funding",
                                            "type": "textField",
                                        },
                                        "LVJcDC": {
                                            "column_title": "Amount",
                                            "type": "numberField",
                                        },
                                    },
                                ],
                            },
                            {
                                "field_id": "DmgsiG",
                                "form_name": "funding-required-cof-r3-w1",
                                "field_type": "yesNoField",
                                "presentation_type": "text",
                                "question": "Do you have any match funding identified but not yet secured?",
                            },
                            {
                                "field_id": "vEOdBS",
                                "form_name": "funding-required-cof-r3-w1",
                                "field_type": "multiInputField",
                                "presentation_type": "table",
                                "question": [
                                    "Unsecured match funding",
                                    {
                                        "iMJdfs": {
                                            "column_title": "Source of unsecured match funding",
                                            "type": "textField",
                                        },
                                        "THOdae": {
                                            "column_title": "Amount",
                                            "type": "numberField",
                                        },
                                    },
                                ],
                            },
                            {
                                "field_id": "XPDbsl",
                                "form_name": "funding-required-cof-r3-w1",
                                "field_type": "freeTextField",
                                "presentation_type": "free_text",
                                "question": "Tell us how the revenue funding you've requested will help run the asset",
                            },
                        ],
                    }
                ],
            },
            {
                "id": "financial_&_risk_forecasts",
                "name": "Financial & risk forecasts",
                "themes": [
                    {
                        "id": "feasiblilty",
                        "name": "Feasiblilty",
                        "answers": [
                            {
                                "field_id": "iSbwDM",
                                "form_name": "feasibility-cof-r3-w1",
                                "field_type": "freeTextField",
                                "presentation_type": "free_text",
                                "question": "Tell us about the feasibility studies you have carried out for your project",
                            },
                            {
                                "field_id": "jFPlEJ",
                                "form_name": "feasibility-cof-r3-w1",
                                "field_type": "yesNoField",
                                "presentation_type": "text",
                                "question": "Do you need to do any further feasibility work?",
                            },
                            {
                                "field_id": "WWdVTC",
                                "form_name": "feasibility-cof-r3-w1",
                                "field_type": "freeTextField",
                                "presentation_type": "free_text",
                                "question": "Describe the feasibility work you still need to complete",
                            },
                        ],
                    },
                    {
                        "id": "risk",
                        "name": "Risk",
                        "answers": [
                            {
                                "field_id": "EODncR",
                                "form_name": "risk-cof-r3-w1",
                                "field_type": "clientSideFileUploadField",
                                "presentation_type": "s3bucketPath",
                                "question": "Risks to your project (document upload)",
                                "path": "your-project-risk-register",
                            },
                        ],
                    },
                    {
                        "id": "income_&_running_costs",
                        "name": "Income & running costs",
                        "answers": [
                            {
                                "field_id": "qXNkfr",
                                "form_name": "operational-costs-cof-r3-w1",
                                "field_type": "freeTextField",
                                "presentation_type": "free_text",
                                "question": "Describe your cash flow for the running of the asset",
                            },
                            {
                                "field_id": "qQSVEn",
                                "form_name": "operational-costs-cof-r3-w1",
                                "field_type": "yesNoField",
                                "presentation_type": "text",
                                "question": "If successful, will you use your funding in the next 12 months?",
                            },
                            {
                                "field_id": "MSNJQD",
                                "form_name": "operational-costs-cof-r3-w1",
                                "field_type": "multiInputField",
                                "presentation_type": "table",
                                "question": [
                                    "Income sources",
                                    {
                                        "AJEWXD": {
                                            "column_title": "Source",
                                            "type": "textField",
                                        },
                                        "cHFrIp": {
                                            "column_title": "Amount",
                                            "type": "numberField",
                                        },
                                    },
                                ],
                            },
                            {
                                "field_id": "NPgwcH",
                                "form_name": "operational-costs-cof-r3-w1",
                                "field_type": "multiInputField",
                                "presentation_type": "table",
                                "question": [
                                    "Running costs of the asset",
                                    {
                                        "IIdfRj": {
                                            "column_title": "Running cost",
                                            "type": "textField",
                                        },
                                        "wlGQua": {
                                            "column_title": "Amount",
                                            "type": "numberField",
                                        },
                                    },
                                ],
                            },
                        ],
                    },
                ],
            },
            {
                "id": "skills_&_resources",
                "name": "Skills & resources",
                "themes": [
                    {
                        "id": "previous_experience",
                        "name": "Previous experience",
                        "answers": [
                            {
                                "field_id": "BBlCko",
                                "form_name": "organisation-information-cof-r3-w1",
                                "field_type": "yesNoField",
                                "presentation_type": "text",
                                "question": "Have you delivered projects like this before?",
                            },
                            {
                                "field_id": "wxCszQ",
                                "form_name": "organisation-information-cof-r3-w1",
                                "field_type": "freeTextField",
                                "presentation_type": "free_text",
                                "question": "Describe your previous projects",
                            },
                            {
                                "field_id": "QJFQgi",
                                "form_name": "organisation-information-cof-r3-w1",
                                "field_type": "freeTextField",
                                "presentation_type": "free_text",
                                "question": "Describe your previous projects - Project 2",
                            },
                            {
                                "field_id": "DGNWqE",
                                "form_name": "organisation-information-cof-r3-w1",
                                "field_type": "freeTextField",
                                "presentation_type": "free_text",
                                "question": "Describe your previous projects - Project 3",
                            },
                            {
                                "field_id": "AfWrEq",
                                "form_name": "skills-and-resources-cof-r3-w1",
                                "field_type": "freeTextField",
                                "presentation_type": "free_text",
                                "question": "Describe any relevant experience you have delivering similar projects or running an asset",
                            },
                        ],
                    },
                    {
                        "id": "governance_and_structures",
                        "name": "Governance and structures",
                        "answers": [
                            {
                                "field_id": "ReomFo",
                                "form_name": "community-representation-cof-r3-w1",
                                "field_type": "freeTextField",
                                "presentation_type": "free_text",
                                "question": "List the members of your board",
                            },
                            {
                                "field_id": "fjVmOt",
                                "form_name": "community-representation-cof-r3-w1",
                                "field_type": "freeTextField",
                                "presentation_type": "free_text",
                                "question": "Tell us about your governance and membership structures",
                            },
                        ],
                    },
                    {
                        "id": "recruitment",
                        "name": "Recruitment",
                        "answers": [
                            {
                                "field_id": "yHXVSA",
                                "form_name": "skills-and-resources-costs-cof-r3-w1",
                                "field_type": "freeTextField",
                                "presentation_type": "free_text",
                                "question": "Roles you’ll recruit to help you run the asset",
                            },
                        ],
                    },
                ],
            },
            {
                "id": "Representation_inclusiveness_&_integration",
                "name": "Representation, inclusiveness & integration",
                "themes": [
                    {
                        "id": "representing_community_views",
                        "name": "Representing community views",
                        "answers": [
                            {
                                "field_id": "GETNxN",
                                "form_name": "community-representation-cof-r3-w1",
                                "field_type": "freeTextField",
                                "presentation_type": "free_text",
                                "question": "Explain how you'll consider the views of the community in the running of the asset",
                            },
                        ],
                    },
                    {
                        "id": "accessibility_and_inclusivity",
                        "name": "Accessibility and inclusivity",
                        "answers": [
                            {
                                "field_id": "lQEkep",
                                "form_name": "inclusiveness-and-integration-cof-r3-w1",
                                "field_type": "freeTextField",
                                "presentation_type": "free_text",
                                "question": "Describe anything that might prevent people from using the asset or participating in its running",
                            },
                            {
                                "field_id": "mgIesb",
                                "form_name": "inclusiveness-and-integration-cof-r3-w1",
                                "field_type": "freeTextField",
                                "presentation_type": "free_text",
                                "question": "Tell us how the asset will be accountable to local people, and involve them in its running",
                            },
                        ],
                    },
                ],
            },
        ],
    },
]
