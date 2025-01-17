# ruff: noqa: E501

scored_criteria = [
    {
        "id": "strategic_case",
        "name": "Strategic case",
        "weighting": 0.30,
        "sub_criteria": [
            {
                "id": "benefits",
                "name": "Benefits",
                "themes": [
                    {
                        "id": "community_use",
                        "name": "Community use",
                        "answers": [
                            {
                                "field_id": "kxgWTy",
                                "form_name": "community-use",
                                "field_type": "multilineTextField",
                                "presentation_type": "text",
                                "question": "Who in the community uses the asset, or has used it in the past, and who benefits from it?",
                            },
                            {
                                "field_id": "wudRxx",
                                "form_name": "project-information",
                                "field_type": "multilineTextField",
                                "presentation_type": "text",
                                "question": "Tell us how the asset is currently being used, or how it has been used before, and why it's important to the community",
                            },
                        ],
                    },
                    {
                        "id": "risk_loss_impact",
                        "name": "Risk and impact of loss",
                        "answers": [
                            {
                                "field_id": "TlGjXb",
                                "form_name": "project-information",
                                "field_type": "multilineTextField",
                                "presentation_type": "text",
                                "question": "Explain why the asset is at risk of being lost to the community, or why it has already been lost",
                            },
                            {
                                "field_id": "UDTxqC",
                                "form_name": "asset-information",
                                "field_type": "checkboxesField",
                                "presentation_type": "list",
                                "question": "Why is the asset at risk of closure?",
                            },
                            {
                                "field_id": "GNhrIs",
                                "form_name": "community-use",
                                "field_type": "multilineTextField",
                                "presentation_type": "text",
                                "question": "Tell us how losing the asset would affect, or has already affected, people in the community",
                            },
                            {
                                "field_id": "qsZLjZ",
                                "form_name": "community-use",
                                "field_type": "multilineTextField",
                                "presentation_type": "text",
                                "question": "Why will the asset be lost without community intervention?",
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
                                "field_id": "HJBgvw",
                                "form_name": "community-engagement",
                                "field_type": "multilineTextField",
                                "presentation_type": "text",
                                "question": "Tell us how you have engaged with the community about your intention to take ownership of the asset, and explain how this has shaped your project plans",
                            },
                            {
                                "field_id": "JCACTy",
                                "form_name": "community-engagement",
                                "field_type": "yesNoField",
                                "presentation_type": "text",
                                "question": "Have you done any fundraising in the community?",
                                # Yes-No determines dpLyQh
                            },
                            {
                                "field_id": "dpLyQh",
                                "form_name": "community-engagement",
                                "field_type": "multilineTextField",
                                "presentation_type": "text",
                                "question": "Describe your fundraising activities",
                                # Determined by Yes-No JCACTy
                            },
                        ],
                    },
                    {
                        "id": "local-support",
                        "name": "Local support",
                        "answers": [
                            {
                                "field_id": "NZKHOp",
                                "form_name": "community-engagement",
                                "field_type": "multilineTextField",
                                "presentation_type": "text",
                                "question": "Tell us how your project supports any wider local plans",
                            },
                            {
                                "field_id": "KqoaJL",
                                "form_name": "local-support",
                                "field_type": "yesNoField",
                                "presentation_type": "text",
                                "question": "Are you confident there is local support for your project?",
                                # Yes-No determines KqoaJL
                            },
                            {
                                "field_id": "BFbzux",
                                "form_name": "local-support",
                                "field_type": "multilineTextField",
                                "presentation_type": "text",
                                "question": "Tell us more about the local support for your project",
                                # Determined by Yes-No KqoaJL
                            },
                            {
                                "field_id": "EEBFao",
                                "form_name": "local-support",
                                "field_type": "fileUploadField",
                                "presentation_type": "file",
                                "question": "Upload supporting evidence (optional)",
                            },
                        ],
                    },
                ],
            },
            {
                "id": "environmental_sustainability",
                "name": "Environmental Sustainability",
                "themes": [
                    {
                        "id": "environmental-considerations",
                        "name": "Environmental considerations",
                        "answers": [
                            {
                                "field_id": "CvVZJv",
                                "form_name": "environmental-sustainability",
                                "field_type": "multilineTextField",
                                "presentation_type": "text",
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
        "weighting": 0.30,
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
                                # These 2 fields are capital and revenue funding respectively
                                "field_id": ["JzWvhj", "jLIgoi"],
                                "form_name": "",
                                "field_type": "numberField",
                                "presentation_type": "grouped_fields",
                                "question": [
                                    "Total funding request",
                                    "Total funding request",
                                ],
                            },
                            {
                                "field_id": "NdFwgy",
                                "form_name": "funding-required",
                                "field_type": "multiInputField",
                                "presentation_type": "heading",
                                "question": "Capital costs",
                            },
                            {
                                "field_id": "NdFwgy",
                                "form_name": "funding-required",
                                "field_type": "textField",
                                "presentation_type": "description",
                                "question": "Describe the cost",
                            },
                            {
                                "field_id": "NdFwgy",
                                "form_name": "funding-required",
                                "field_type": "numberField",
                                "presentation_type": "amount",
                                "question": "Amount",
                            },
                            # {
                            #     "field_id": "NdFwgy",
                            #     "form_name": "funding-required",
                            #     "field_type": "multiInputField",
                            #     "presentation_type": "table",
                            #     "question": [
                            #         "Capital costs",
                            #         {
                            #             "kSZqfv": {
                            #                 "column_title": "Describe the cost",
                            #                 "type": "textField",
                            #             },
                            #             "zJAnwc": {
                            #                 "column_title": "Amount in pounds",
                            #                 "type": "numberField",
                            #             },
                            #         }
                            #     ],
                            # },
                            {
                                "field_id": "NWTKzQ",
                                "form_name": "funding-required",
                                "field_type": "yesNoField",
                                "presentation_type": "text",
                                "question": "Are you applying for revenue funding from the Community Ownership Fund?",
                            },
                            {
                                "field_id": "NyudvF",
                                "form_name": "funding-required",
                                "field_type": "multiInputField",
                                "presentation_type": "heading",
                                "question": "Revenue costs",
                            },
                            {
                                "field_id": "NyudvF",
                                "form_name": "funding-required",
                                "field_type": "textField",
                                "presentation_type": "description",
                                "question": "Describe the cost",
                            },
                            {
                                "field_id": "NyudvF",
                                "form_name": "funding-required",
                                "field_type": "numberField",
                                "presentation_type": "amount",
                                "question": "Amount",
                            },
                            # {
                            #     "field_id": "NyudvF",
                            #     "form_name": "funding-required",
                            #     "field_type": "multiInputField",
                            #     "presentation_type": "table",
                            #     "question": [
                            #         "Revenue costs",
                            #         {
                            #             "TkDxmD": {
                            #                 "column_title": "Describe the cost",
                            #                 "type": "textField",
                            #             },
                            #             "zbqnvm": {
                            #                 "column_title": "Amount in pounds",
                            #                 "type": "numberField",
                            #             },
                            #         },
                            #     ],
                            # },
                            {
                                "field_id": "DIZZOC",
                                "form_name": "funding-required",
                                "field_type": "yesNoField",
                                "presentation_type": "text",
                                "question": "Have you secured any match funding yet?",
                            },
                            {
                                "field_id": "abkrwo",
                                "form_name": "funding-required",
                                "field_type": "multiInputField",
                                "presentation_type": "heading",
                                "question": "Secured match funding",
                            },
                            {
                                "field_id": "abkrwo",
                                "form_name": "funding-required",
                                "field_type": "textField",
                                "presentation_type": "description",
                                "question": "Source of funding",
                            },
                            {
                                "field_id": "abkrwo",
                                "form_name": "funding-required",
                                "field_type": "numberField",
                                "presentation_type": "amount",
                                "question": "Amount",
                            },
                            # {
                            #     "field_id": "abkrwo",
                            #     "form_name": "funding-required",
                            #     "field_type": "multiInputField",
                            #     "presentation_type": "table",
                            #     "question": [
                            #         "Secured match funding",
                            #         {
                            #             "kietnW": {
                            #                 "column_title": "Source of secured funding",
                            #                 "type": "textField",
                            #             },
                            #             "lwrCQz": {
                            #                 "column_title": "Amount in pounds",
                            #                 "type": "numberField",
                            #             },
                            #         },
                            #     ],
                            # },
                            {
                                "field_id": "RvbwSX",
                                "form_name": "funding-required",
                                "field_type": "yesNoField",
                                "presentation_type": "text",
                                "question": "Do you have any match funding identified but not yet secured?",
                            },
                            {
                                "field_id": "AOLYnV",
                                "form_name": "funding-required",
                                "field_type": "multiInputField",
                                "presentation_type": "heading",
                                "question": "Unsecured match funding",
                            },
                            {
                                "field_id": "AOLYnV",
                                "form_name": "funding-required",
                                "field_type": "textField",
                                "presentation_type": "description",
                                "question": "Source of funding",
                            },
                            {
                                "field_id": "AOLYnV",
                                "form_name": "funding-required",
                                "field_type": "numberField",
                                "presentation_type": "amount",
                                "question": "Amount",
                            },
                            # {
                            #     "field_id": "AOLYnV",
                            #     "form_name": "funding-required",
                            #     "field_type": "multiInputField",
                            #     "presentation_type": "table",
                            #     "question": [
                            #         "Unsecured match funding",
                            #         {
                            #             "FwPOFx": {
                            #                 "column_title": "Source of unsecured match funding",
                            #                 "type": "textField",
                            #             },
                            #             "SPGORz": {
                            #                 "column_title": "Amount in pounds",
                            #                 "type": "numberField",
                            #             },
                            #         },
                            #     ],
                            # },
                            {
                                "field_id": "fnIdkJ",
                                "form_name": "funding-required",
                                "field_type": "numberField",
                                "presentation_type": "text",
                                "question": "Asset value",
                            },
                            {
                                "field_id": "oaIntA",
                                "form_name": "funding-required",
                                "field_type": "yesNoField",
                                "presentation_type": "text",
                                "question": "If successful, will you use your funding in the next 12 months? (Y/N)",
                            },
                        ],
                    }
                ],
            },
            {
                "id": "financial_and_risk_forecasts",
                "name": "Financial and risk forecasts",
                "themes": [
                    {
                        "id": "feasibility",
                        "name": "Feasibility",
                        "answers": [
                            {
                                "field_id": "ieRCkI",
                                "form_name": "feasibility",
                                "field_type": "multilineTextField",
                                "presentation_type": "text",
                                "question": "Tell us about the feasibility studies you have carried out for your project",
                            },
                            {
                                "field_id": "aAeszH",
                                "form_name": "feasibility",
                                "field_type": "yesNoField",
                                "presentation_type": "text",
                                "question": "Do you need to do any further feasibility work?",
                            },
                        ],
                    },
                    {
                        "id": "risk",
                        "name": "Risk",
                        "answers": [
                            {
                                "field_id": "ozgwXq",
                                "form_name": "risk",
                                "field_type": "fileUploadField",
                                "presentation_type": "file",
                                "question": "Risks to your project (document upload)",
                            },
                        ],
                    },
                    {
                        "id": "income_and_running_costs",
                        "name": "Income and running costs",
                        "answers": [
                            {
                                "field_id": "WDDkVB",
                                "form_name": "project-costs",
                                "field_type": "multilineTextField",
                                "presentation_type": "text",
                                "question": "Summarise your cash flow for the running of the asset",
                            },
                            {
                                "field_id": "TzOokX",
                                "form_name": "project-costs",
                                "field_type": "multiInputField",
                                "presentation_type": "heading",
                                "question": "Sources of income",
                            },
                            {
                                "field_id": "TzOokX",
                                "form_name": "project-costs",
                                "field_type": "multiInputField",
                                "presentation_type": "description",
                                "question": "Income source",
                            },
                            {
                                "field_id": "TzOokX",
                                "form_name": "project-costs",
                                "field_type": "multiInputField",
                                "presentation_type": "amount",
                                "question": "Amount",
                            },
                            # {
                            #     "field_id": "TzOokX",
                            #     "form_name": "project-costs",
                            #     "field_type": "multiInputField",
                            #     "presentation_type": "table",
                            #     "question": [
                            #         "Sources of income",
                            #         {
                            #             "GpLJDu": {
                            #                 "column_title": "Source",
                            #                 "type": "textField",
                            #             },
                            #             "RRzTlc": {
                            #                 "column_title": "Amount in pounds",
                            #                 "type": "numberField",
                            #             },
                            #         },
                            #     ],
                            # },
                            {
                                "field_id": "fbFeEx",
                                "form_name": "project-costs",
                                "field_type": "multiInputField",
                                "presentation_type": "heading",
                                "question": "Running costs",
                            },
                            {
                                "field_id": "fbFeEx",
                                "form_name": "project-costs",
                                "field_type": "multiInputField",
                                "presentation_type": "description",
                                "question": "Running costs",
                            },
                            {
                                "field_id": "fbFeEx",
                                "form_name": "project-costs",
                                "field_type": "multiInputField",
                                "presentation_type": "amount",
                                "question": "Amount",
                            },
                            # {
                            #     "field_id": "fbFeEx",
                            #     "form_name": "project-costs",
                            #     "field_type": "multiInputField",
                            #     "presentation_type": "table",
                            #     "question": [
                            #         "Running costs",
                            #         {
                            #             "BZIEKw": {
                            #                 "column_title": "Running cost",
                            #                 "type": "textField",
                            #             },
                            #             "XbgRGb": {
                            #                 "column_title": "Amount in pounds",
                            #                 "type": "numberField",
                            #             },
                            #         },
                            #     ],
                            # },
                        ],
                    },
                ],
            },
            {
                "id": "skills_and_resources",
                "name": "Skills and resources",
                "themes": [
                    {
                        "id": "previous_experience",
                        "name": "Previous experience",
                        "answers": [
                            {
                                "field_id": "BBlCko",
                                "form_name": "organisation-information",
                                "field_type": "yesNoField",
                                "presentation_type": "text",
                                "question": "Have you delivered projects like this before? (Y/N)",
                            },
                            {
                                "field_id": ["wxCszQ", "QJFQgi", "DGNWqE"],
                                "form_name": "organisation-information",
                                "field_type": "multilineTextField",
                                "presentation_type": "grouped_fields",
                                "question": [
                                    "Describe your previous projects",
                                    "Describe your previous projects",
                                ],
                            },
                            {
                                "field_id": "CBIWnt",
                                "form_name": "skills-and-resources",
                                "field_type": "yesNoField",
                                "presentation_type": "text",
                                "question": "Do you have experience of managing a community asset?",
                            },
                            {
                                "field_id": "QWveYc",
                                "form_name": "skills-and-resources",
                                "field_type": "multilineTextField",
                                "presentation_type": "text",
                                "question": "Describe any experience you have with community assets similar to this",
                            },
                        ],
                    },
                    {
                        "id": "governance_and_structures",
                        "name": "Governance and structures",
                        "answers": [
                            {
                                "field_id": "JnvsPq",
                                "form_name": "community-representation",
                                "field_type": "multilineTextField",
                                "presentation_type": "text",
                                "question": "List the members of your board",
                            },
                            {
                                "field_id": "yMCivI",
                                "form_name": "community-representation",
                                "field_type": "multilineTextField",
                                "presentation_type": "text",
                                "question": "Tell us about your governance and membership structures",
                            },
                        ],
                    },
                    {
                        "id": "recruitment",
                        "name": "Recruitment",
                        "answers": [
                            {
                                "field_id": "vKnMPG",
                                "form_name": "skills-and-resources",
                                "field_type": "yesNoField",
                                "presentation_type": "text",
                                "question": "Do you have plans to recruit people to help you manage the asset?",
                            },
                            {
                                "field_id": "VNjRgZ",
                                "form_name": "skills-and-resources",
                                "field_type": "multilineTextField",
                                "presentation_type": "text",
                                "question": "Tells us about the roles you'll recruit",
                            },
                        ],
                    },
                ],
            },
            {
                "id": "representation_inclusiveness_and_integration",
                "name": "Representation, inclusiveness and integration",
                "themes": [
                    {
                        "id": "representing_community_views",
                        "name": "Representing community views",
                        "answers": [
                            {
                                "field_id": "NUZOvS",
                                "form_name": "community-representation",
                                "field_type": "multilineTextField",
                                "presentation_type": "text",
                                "question": "Explain how you'll consider the views of the community in the running of the asset",
                            },
                        ],
                    },
                    {
                        "id": "accessibility_and_inclusivity",
                        "name": "Accessibility and inclusivity",
                        "answers": [
                            {
                                "field_id": "YbfbSC",
                                "form_name": "inclusiveness-and-integration",
                                "field_type": "multilineTextField",
                                "presentation_type": "text",
                                "question": "Describe anything that might prevent people from using the asset or participating in its running",
                            },
                            {
                                "field_id": "KuhSWw",
                                "form_name": "inclusiveness-and-integration",
                                "field_type": "multilineTextField",
                                "presentation_type": "text",
                                "question": "Tell us how you'll make your project accessible and inclusive to everyone in the community",
                            },
                            {
                                "field_id": "bkJsiO",
                                "form_name": "inclusiveness-and-integration",
                                "field_type": "multilineTextField",
                                "presentation_type": "text",
                                "question": "Describe how the project will bring people together from all over the community",
                            },
                        ],
                    },
                ],
            },
        ],
    },
    {
        "id": "potential_to_deliver_community_benefit",
        "name": "Potential to deliver community benefit",
        "weighting": 0.30,
        "sub_criteria": [
            {
                "id": "community-benefits",
                "name": "How the community benefits	",
                "themes": [
                    {
                        "id": "delivering_and_sustaining_benefits",
                        "name": "Delivering and sustaining benefits",
                        "answers": [
                            {
                                "field_id": "SrtVAs",
                                "form_name": "inclusiveness_and_integration",
                                "field_type": "multilineTextField",
                                "presentation_type": "text",
                                "question": "Describe the planned activities or services that will take place at the asset",
                            },
                            {
                                "field_id": "QjJtbs",
                                "form_name": "community_benefits",
                                "field_type": "checkboxesField",
                                "presentation_type": "list",
                                "question": "What community benefits do you expect to deliver with this project?",
                            },
                            {
                                "field_id": "gDTsgG",
                                "form_name": "community_benefits",
                                "field_type": "multilineTextField",
                                "presentation_type": "text",
                                "question": "Tell us about these benefits in detail, and explain how you'll measure the benefits it'll bring for the community",
                            },
                            {
                                "field_id": "kYjJFy",
                                "form_name": "community_benefits",
                                "field_type": "multilineTextField",
                                "presentation_type": "text",
                                "question": "Explain how you plan to sustain, and potentially expand, these benefits over time",
                            },
                        ],
                    }
                ],
            },
            {
                "id": "how-the-asset-will-be-inclusive",
                "name": "How the asset will be inclusive",
                "themes": [
                    {
                        "id": "benefitting_the_whole_community",
                        "name": "Benefitting the whole community",
                        "answers": [
                            {
                                "field_id": "UbjYqE",
                                "form_name": "community_benefits",
                                "field_type": "multilineTextField",
                                "presentation_type": "text",
                                "question": "Tell us how you'll make sure the whole community benefits from the asset",
                            },
                        ],
                    },
                ],
            },
        ],
    },
    {
        "id": "added_value_of_the_community_asset",
        "name": "Added value of the community asset",
        "weighting": 0.10,
        "sub_criteria": [
            {
                "id": "value-to-the-community",
                "name": "Value to the community",
                "themes": [
                    {
                        "id": "addressing_community_challenges",
                        "name": "Addressing community challenges",
                        "answers": [
                            {
                                "field_id": "oOPUXI",
                                "form_name": "value-to-the-community",
                                "field_type": "multilineTextField",
                                "presentation_type": "text",
                                "question": "Tell us about your local community as a whole",
                            },
                            {
                                "field_id": "NKOmNL",
                                "form_name": "value-to-the-community",
                                "field_type": "multilineTextField",
                                "presentation_type": "text",
                                "question": "Describe any specific challenges your community faces, and how the asset will address these",
                            },
                        ],
                    }
                ],
            }
        ],
    },
]
