# ruff: noqa: E501

scored_criteria = [
    {
        "id": "skills_and_experience",
        "name": "Your skills and experience",
        "weighting": 0.15,
        "sub_criteria": [
            {
                "id": "staff_and_volunteers_and_cuurent_service",
                "name": "Staff and volunteers and current service",
                "themes": [
                    {
                        "id": "staff_and_volunteers",
                        "name": "Staff and volunteers",
                        "answers": [
                            {
                                "field_id": "bcJWbJ",
                                "form_name": "staff-and-volunteers-ns",
                                "field_type": "numberField",
                                "presentation_type": "integer",
                                "question": "How many staff members are currently employed in your organisation?",
                            },
                            {
                                "field_id": "pwPYdF",
                                "form_name": "staff-and-volunteers-ns",
                                "field_type": "numberField",
                                "presentation_type": "integer",
                                "question": "How many volunteers are actively involved in your organisation?",
                            },
                            {
                                "field_id": "VXKVmM",
                                "form_name": "staff-and-volunteers-ns",
                                "field_type": "textField",
                                "presentation_type": "text",
                                "question": "What percentage of your employed staff work part-time?",
                            },
                            {
                                "field_id": "wOUNbF",
                                "form_name": "staff-and-volunteers-ns",
                                "field_type": "numberField",
                                "presentation_type": "text",
                                "question": "For part-time employees, what is their average full-time equivalency (FTE)?",
                            },
                        ],
                    },
                    {
                        "id": "current_service",
                        "name": "Current service",
                        "answers": [
                            {
                                "field_id": "QOlbCV",
                                "form_name": "current-services-ns",
                                "field_type": "yesNoField",
                                "presentation_type": "text",
                                "question": "Have you provided a night shelter or emergency accommodation on or after 1 April 2019?",
                            },
                            {
                                "field_id": "affVbH",
                                "form_name": "current-services-ns",
                                "field_type": "yesNoField",
                                "presentation_type": "text",
                                "question": "Is the night shelter or emergency accommodation communal?",
                            },
                            {
                                "field_id": "ttEOXi",
                                "form_name": "current-services-ns",
                                "field_type": "yesNoField",
                                "presentation_type": "text",
                                "question": "Is the night shelter or emergency accommodation single room accommodation?",
                            },
                            {
                                "field_id": "dSdeYa",
                                "form_name": "current-services-ns",
                                "field_type": "numberField",
                                "presentation_type": "integer",
                                "question": "How many bed spaces did the night shelter or emergency accommodation provide from 1 April 2022 to 31 March 2023?",
                            },
                            {
                                "field_id": "gXvnZA",
                                "form_name": "current-services-ns",
                                "field_type": "yesNoField",
                                "presentation_type": "text",
                                "question": "Is the night shelter or emergency accommodation used for SWEP (severe weather emergency protocol)?",
                            },
                            {
                                "field_id": "vStFMu",
                                "form_name": "current-services-ns",
                                "field_type": "yesNoField",
                                "presentation_type": "text",
                                "question": "Do you accept referrals from the local authority or other agencies for available bed spaces?",
                            },
                            {
                                "field_id": "YyMRdP",
                                "form_name": "current-services-ns",
                                "field_type": "numberField",
                                "presentation_type": "integer",
                                "question": "How many nights did the night shelter or emergency accommodation open from 1 April 2022 to 31 March 2023?",
                            },
                            {
                                "field_id": "STfdvD",
                                "form_name": "current-services-ns",
                                "field_type": "yesNoField",
                                "presentation_type": "text",
                                "question": "Do you currently provide day provision?",
                            },
                            {
                                "field_id": "bCXNtj",
                                "form_name": "current-services-ns",
                                "field_type": "monthYearField",
                                "presentation_type": "text",
                                "question": "When did you start providing day provision?",
                            },
                            {
                                "field_id": "ULPcAU",
                                "form_name": "current-services-ns",
                                "field_type": "checkboxesField",
                                "presentation_type": "list",
                                "question": "Which day provision services are you currently providing?",
                            },
                            {
                                "field_id": "zwQHCl",
                                "form_name": "current-services-ns",
                                "field_type": "freeTextField",
                                "presentation_type": "free_text",
                                "question": "Which other day provision do you currently provide?",
                            },
                            {
                                "field_id": "GBfYfn",
                                "form_name": "current-services-ns",
                                "field_type": "yesNoField",
                                "presentation_type": "text",
                                "question": "Do you currently provide any other services?",
                            },
                            {
                                "field_id": "wViAiU",
                                "form_name": "current-services-ns",
                                "field_type": "freeTextField",
                                "presentation_type": "free_text",
                                "question": "What other services are you currently providing?",
                            },
                        ],
                    },
                ],
            },
            {
                "id": "targeted_criteria_current",
                "name": "Targeted criteria",
                "themes": [
                    {
                        "id": "targeted_criteria_current",
                        "name": "Targeted criteria",
                        "answers": [
                            {
                                "field_id": "umAyqH",
                                "form_name": "current-services-ns",
                                "field_type": "yesNoField",
                                "presentation_type": "text",
                                "question": "Do you currently provide specialist support?",
                            },
                            {
                                "field_id": "JCUQcR",
                                "form_name": "current-services-ns",
                                "field_type": "checkboxesField",
                                "presentation_type": "list",
                                "question": "Who do you currently provide targeted specialist support to?",
                            },
                            {
                                "field_id": "bTSizq",
                                "form_name": "current-services-ns",
                                "field_type": "freeTextField",
                                "presentation_type": "free_text",
                                "question": "Which other specialist support will your proposal provide?",
                            },
                        ],
                    },
                ],
            },
        ],
    },
    {
        "id": "your_proposal",
        "name": "Your proposal",
        "weighting": 0.40,
        "sub_criteria": [
            {
                "id": "proposal_summary_and_milestones",
                "name": "Proposal summary and milestones",
                "themes": [
                    {
                        "id": "proposal_summary",
                        "name": "Proposal summary",
                        "answers": [
                            {
                                "field_id": "pWFwci",
                                "form_name": "objectives-and-activities-ns",
                                "field_type": "freeTextField",
                                "presentation_type": "free_text",
                                "question": "Give a brief summary of your proposal, including what you hope to achieve",
                            },
                            {
                                "field_id": "kRxOHF",
                                "form_name": "objectives-and-activities-ns",
                                "field_type": "multiInputField",
                                "presentation_type": "table",
                                "question": [
                                    "Objectives and activities",
                                    {
                                        "FbWEBY": {
                                            "column_title": "Objective",
                                            "type": "textField",
                                        },
                                        "RXrpzV": {
                                            "column_title": "Activities that will help you achieve the objective",
                                            "type": "multilineTextField",
                                        },
                                    },
                                ],
                            },
                        ],
                    },
                    {
                        "id": "milestones",
                        "name": "Milestones",
                        "answers": [
                            {
                                "field_id": "sXlkAm",
                                "form_name": "project-milestones-ns",
                                "field_type": "multiInputField",
                                "presentation_type": "table",
                                "question": [
                                    "Proposal milestones",
                                    {
                                        "fFIuPP": {
                                            "column_title": "Milestone",
                                            "type": "multilineTextField",
                                        },
                                        "PrulfI": {
                                            "column_title": "When will you reach this milestone?",
                                            "type": "MonthYearField",
                                        },
                                    },
                                ],
                            }
                        ],
                    },
                ],
            },
            {
                "id": "your_local_area_need",
                "name": "Your local area need",
                "themes": [
                    {
                        "id": "your_local_area_need",
                        "name": "Your local area need",
                        "answers": [
                            {
                                "field_id": "nMfGTS",
                                "form_name": "local-need-and-support-ns",
                                "field_type": "freeTextField",
                                "presentation_type": "free_text",
                                "question": "Tell us why your proposal is needed in your area",
                            },
                            {
                                "field_id": "nURkuc",
                                "form_name": "local-need-and-support-ns",
                                "field_type": "textField",
                                "presentation_type": "text",
                                "question": "What is the local authority of where your proposal will be based?",
                            },
                            {
                                "field_id": "lFTgWk",
                                "form_name": "local-need-and-support-ns",
                                "field_type": "yesNoField",
                                "presentation_type": "text",
                                "question": "Do you have the local authority's support and endorsement for your proposal?",
                            },
                            {
                                "field_id": "mIGfuL",
                                "form_name": "local-need-and-support-ns",
                                "field_type": "clientSideFileUploadField",
                                "presentation_type": "s3bucketPath",
                                "question": "Upload letter of endorsement from your local authority (optional)",
                                "path": "local-authority-support",
                            },
                        ],
                    },
                ],
            },
            {
                "id": "proposed_services",
                "name": "Proposed services",
                "themes": [
                    {
                        "id": "proposed_services",
                        "name": "Proposed services",
                        "answers": [
                            {
                                "field_id": "lOliDH",
                                "form_name": "proposed-services-ns",
                                "field_type": "freeTextField",
                                "presentation_type": "free_text",
                                "question": "Tell us how your proposal will transform your existing services",
                            },
                            {
                                "field_id": "dWxxdq",
                                "form_name": "proposed-services-ns",
                                "field_type": "yesNoField",
                                "presentation_type": "text",
                                "question": "Do you plan to use this funding to make any changes to the existing night shelter or emergency accommodation?",
                            },
                            {
                                "field_id": "UEndmh",
                                "form_name": "proposed-services-ns",
                                "field_type": "numberField",
                                "presentation_type": "integer",
                                "question": "How many single rooms will you provide with the funding?",
                            },
                            {
                                "field_id": "jzzBDS",
                                "form_name": "proposed-services-ns",
                                "field_type": "yesNoField",
                                "presentation_type": "text",
                                "question": "Do you plan to use this funding to make any changes to the existing day provision?",
                            },
                            {
                                "field_id": "bGCkPI",
                                "form_name": "proposed-services-ns",
                                "field_type": "checkboxesField",
                                "presentation_type": "list",
                                "question": "Which additional day provision will your proposal provide?",
                            },
                            {
                                "field_id": "brLcqY",
                                "form_name": "proposed-services-ns",
                                "field_type": "freeTextField",
                                "presentation_type": "free_text",
                                "question": "Which other additional day provision will your proposal provide?",
                            },
                            {
                                "field_id": "bCQWFN",
                                "form_name": "proposed-services-ns",
                                "field_type": "yesNoField",
                                "presentation_type": "text",
                                "question": "Will you provide any other additional services?",
                            },
                            {
                                "field_id": "kPvpzG",
                                "form_name": "proposed-services-ns",
                                "field_type": "freeTextField",
                                "presentation_type": "free_text",
                                "question": "Which other services will you use the funding to provide?",
                            },
                        ],
                    },
                ],
            },
            {
                "id": "targeted_criteria_proposed",
                "name": "Targeted criteria",
                "themes": [
                    {
                        "id": "targeted_criteria_proposed",
                        "name": "Targeted criteria",
                        "answers": [
                            {
                                "field_id": "xYNpHc",
                                "form_name": "proposed-services-ns",
                                "field_type": "yesNoField",
                                "presentation_type": "text",
                                "question": "Will your proposal provide additional specialist support?",
                            },
                            {
                                "field_id": "RKPpEV",
                                "form_name": "proposed-services-ns",
                                "field_type": "checkboxesField",
                                "presentation_type": "list",
                                "question": "Who will your proposal provide targeted specialist support to?",
                            },
                            {
                                "field_id": "HTGgzg",
                                "form_name": "proposed-services-ns",
                                "field_type": "freeTextField",
                                "presentation_type": "free_text",
                                "question": "Who will your proposal provide specialist support to?",
                            },
                        ],
                    },
                ],
            },
            {
                "id": "working_in_partnership",
                "name": "Working in partnership",
                "themes": [
                    {
                        "id": "working_in_partnership",
                        "name": "Working in partnership",
                        "answers": [
                            {
                                "field_id": "qMRHPz",
                                "form_name": "working-in-partnership-ns",
                                "field_type": "freeTextField",
                                "presentation_type": "free_text",
                                "question": "Describe your important local partners and how they will support your proposal",
                            }
                        ],
                    },
                ],
            },
            {
                "id": "proposal_sustainability",
                "name": "Proposal sustainability",
                "themes": [
                    {
                        "id": "proposal_sustainability",
                        "name": "Proposal sustainability",
                        "answers": [
                            {
                                "field_id": "PEMJEy",
                                "form_name": "proposal-sustainability-ns",
                                "field_type": "freeTextField",
                                "presentation_type": "free_text",
                                "question": "How will this funding support the longer-term sustainability of your proposal beyond the funding period?",
                            },
                        ],
                    },
                ],
            },
        ],
    },
    {
        "id": "outputs_and_outcomes",
        "name": "Outputs and outcomes",
        "weighting": 0.15,
        "sub_criteria": [
            {
                "id": "proposal_support",
                "name": "Proposal support",
                "themes": [
                    {
                        "id": "proposal_support",
                        "name": "Proposal support",
                        "answers": [
                            {
                                "field_id": "cYEiGS",
                                "form_name": "outputs-and-outcomes-ns",
                                "field_type": "numberField",
                                "presentation_type": "integer",
                                "question": "How many people will the proposal support with the funding? 1 April 2023 to 31 March 2024",
                            },
                            {
                                "field_id": "ZZisap",
                                "form_name": "outputs-and-outcomes-ns",
                                "field_type": "numberField",
                                "presentation_type": "integer",
                                "question": "How many people will the proposal support with the funding? 1 April 2024 to 31 March 2025",
                            },
                        ],
                    },
                ],
            },
            {
                "id": "restricted_eligibility",
                "name": "Restricted eligibility",
                "themes": [
                    {
                        "id": "restricted_eligibility",
                        "name": "Restricted eligibility",
                        "answers": [
                            {
                                "field_id": "ZJCVjE",
                                "form_name": "outputs-and-outcomes-ns",
                                "field_type": "numberField",
                                "presentation_type": "integer",
                                "question": "How many people with restricted eligibility will the proposal support? 1 April 2023 to 31 March 2024",
                            },
                            {
                                "field_id": "dboegN",
                                "form_name": "outputs-and-outcomes-ns",
                                "field_type": "numberField",
                                "presentation_type": "integer",
                                "question": "How many people with restricted eligibility will the proposal support? 1 April 2024 to 31 March 2025",
                            },
                        ],
                    },
                ],
            },
        ],
    },
    {
        "id": "risk_and_deliverability",
        "name": "Risk and Deliverability",
        "weighting": 0.15,
        "sub_criteria": [
            {
                "id": "risk_to_the_proposal",
                "name": "Risk to the proposal",
                "themes": [
                    {
                        "id": "risk_to_the_proposal",
                        "name": "Risk to the proposal",
                        "answers": [
                            {
                                "field_id": "xDpgOK",
                                "form_name": "risk-and-deliverability-ns",
                                "field_type": "multiInputField",
                                "presentation_type": "table",
                                "question": [
                                    "Risks to the proposal",
                                    {
                                        "dmKRCF": {
                                            "column_title": "Risk",
                                            "type": "multilineTextField",
                                        },
                                        "GVoNOE": {
                                            "column_title": "Likelihood",
                                            "type": "RadiosField",
                                        },
                                        "SRHsAx": {
                                            "column_title": "Proposed mitigation",
                                            "type": "multilineTextField",
                                        },
                                    },
                                ],
                            },
                        ],
                    },
                ],
            }
        ],
    },
    {
        "id": "value_for_money",
        "name": "Value for money",
        "weighting": 0.15,
        "sub_criteria": [
            {
                "id": "funding_required_building_works_and_match_funding",
                "name": "Funding required, building works and match funding",
                "themes": [
                    {
                        "id": "funding_required",
                        "name": "Funding required",
                        "answers": [
                            {
                                "field_id": "NxVqXd",
                                "form_name": "funding-required-ns",
                                "field_type": "radiosField",
                                "presentation_type": "text",
                                "question": "Which funding are you applying for?",
                            },
                            {
                                "field_id": ["pVBwci", "GRWtfV"],
                                "form_name": "funding-required-ns",
                                "field_type": "numberField",
                                "branched_field": 1,
                                "presentation_type": "grouped_fields",
                                "question": [
                                    "How much revenue are you applying for? 1 April 2023 to 31 March 2024",
                                    "How much revenue are you applying for? 1 April 2023 to 31 March 2024",
                                ],
                            },
                            {
                                "field_id": ["zvPzXN", "WDouQc"],
                                "branched_field": 1,
                                "presentation_type": "grouped_fields",
                                "form_name": "funding-required-ns",
                                "field_type": "numberField",
                                "question": [
                                    "How much revenue are you applying for? 1 April 2024 to 31 March 2025",
                                    "How much revenue are you applying for? 1 April 2024 to 31 March 2025",
                                ],
                            },
                            {
                                "field_id": "mCbbyN",
                                "form_name": "funding-required-ns",
                                "field_type": "multiInputField",
                                "presentation_type": "table",
                                "question": [
                                    "Revenue funding (add another)",
                                    {
                                        "dpDFgB": {
                                            "column_title": "Item of expenditure",
                                            "type": "textField",
                                        },
                                        "iZdZrr": {
                                            "column_title": "Amount",
                                            "type": "numberField",
                                        },
                                        "leIxEX": {
                                            "column_title": "Financial year",
                                            "type": "RadiosField",
                                        },
                                        "TrTaZQ": {
                                            "column_title": "How the expenditure is calculated (optional)",
                                            "type": "textField",
                                        },
                                    },
                                ],
                            },
                            {
                                "field_id": ["SGjmSM", "QUCvFy"],
                                "form_name": "funding-required-ns",
                                "field_type": "numberField",
                                "branched_field": 1,
                                "presentation_type": "grouped_fields",
                                "question": [
                                    "How much capital are you applying for? 1 April 2023 to 31 March 2024",
                                    "How much capital are you applying for? 1 April 2023 to 31 March 2024",
                                ],
                            },
                            {
                                "field_id": ["wTdyhk", "pppiYl"],
                                "form_name": "funding-required-ns",
                                "field_type": "numberField",
                                "branched_field": 1,
                                "presentation_type": "grouped_fields",
                                "question": [
                                    "How much capital are you applying for? 1 April 2024 to 31 March 2025",
                                    "How much capital are you applying for? 1 April 2024 to 31 March 2025",
                                ],
                            },
                            {
                                "field_id": "XsAoTv",
                                "form_name": "funding-required-ns",
                                "field_type": "multiInputField",
                                "presentation_type": "table",
                                "question": [
                                    "Capital costs (add another)",
                                    {
                                        "cpFthG": {
                                            "column_title": "Item of expenditure",
                                            "type": "textField",
                                        },
                                        "JtBjFp": {
                                            "column_title": "Amount",
                                            "type": "numberField",
                                        },
                                        "mmwzGc": {
                                            "column_title": "Financial year",
                                            "type": "RadiosField",
                                        },
                                        "pMffVz": {
                                            "column_title": "How the expenditure is calculated (optional)",
                                            "type": "textField",
                                        },
                                    },
                                ],
                            },
                        ],
                    },
                    {
                        "id": "building_works",
                        "name": "Building works",
                        "answers": [
                            {
                                "field_id": "lifPop",
                                "form_name": "building-works-ns",
                                "field_type": "yesNoField",
                                "presentation_type": "text",
                                "question": "Will you use the funding to conduct building works?",
                            },
                            {
                                "field_id": "fmcTtE",
                                "form_name": "building-works-ns",
                                "field_type": "numberField",
                                "presentation_type": "integer",
                                "question": "Number of new single room units (optional)",
                            },
                            {
                                "field_id": "xGnWEW",
                                "form_name": "building-works-ns",
                                "field_type": "radiosField",
                                "presentation_type": "text",
                                "question": "Do you need planning approval for your proposal?",
                            },
                            {
                                "field_id": "KhISvR",
                                "form_name": "building-works-ns",
                                "field_type": "yesNoField",
                                "presentation_type": "text",
                                "question": "Have you made an application for planning permission?",
                            },
                            {
                                "field_id": "lkwQrI",
                                "form_name": "building-works-ns",
                                "field_type": "textField",
                                "presentation_type": "text",
                                "question": "What's your planning application number?",
                            },
                            {
                                "field_id": "YFPgTB",
                                "form_name": "building-works-ns",
                                "field_type": "yesNoField",
                                "presentation_type": "text",
                                "question": "Have you received any pre-application planning advice?",
                            },
                            {
                                "field_id": "mADkNz",
                                "form_name": "building-works-ns",
                                "field_type": "multilineTextField",
                                "presentation_type": "list",
                                "question": "Give a brief summary of the advice you received",
                            },
                            {
                                "field_id": "AYDIPX",
                                "form_name": "building-works-ns",
                                "field_type": "yesNoField",
                                "presentation_type": "text",
                                "question": "Will you procure a construction contract for the building works?",
                            },
                            {
                                "field_id": "nyusrL",
                                "form_name": "building-works-ns",
                                "field_type": "yesNoField",
                                "presentation_type": "text",
                                "question": "Will you use any professional advisors for the proposal?",
                            },
                            {
                                "field_id": "SQEpBt",
                                "form_name": "building-works-ns",
                                "field_type": "multiInputField",
                                "presentation_type": "table",
                                "question": [
                                    "Details of professional advisors",
                                    {
                                        "cbYcqS": {
                                            "column_title": "What is their job role?",
                                            "type": "textField",
                                        },
                                        "muRwiL": {
                                            "column_title": "Organisation name",
                                            "type": "textField",
                                        },
                                    },
                                ],
                            },
                            {
                                "field_id": "rYAgMN",
                                "form_name": "building-works-ns",
                                "field_type": "yesNoField",
                                "presentation_type": "text",
                                "question": "Will you be hiring contractors to complete the building works?",
                            },
                            {
                                "field_id": "TtBDIZ",
                                "form_name": "building-works-ns",
                                "field_type": "yesNoField",
                                "presentation_type": "text",
                                "question": "Do you know which contractors will be conducting the work?",
                            },
                            {
                                "field_id": "UDhjLS",
                                "form_name": "building-works-ns",
                                "field_type": "multiInputField",
                                "presentation_type": "table",
                                "question": [
                                    "Which contractors will you use to carry out this work?",
                                    {
                                        "CZZYvE": {
                                            "column_title": "Which contractors will you use to carry out this work?",
                                            "type": "textField",
                                        },
                                    },
                                ],
                            },
                            {
                                "field_id": "NOMwBb",
                                "form_name": "building-works-ns",
                                "field_type": "clientSideFileUploadField",
                                "presentation_type": "s3bucketPath",
                                "question": "Upload cost estimate",
                                "path": "upload-cost-estimate",
                            },
                            {
                                "field_id": "aTxAPP",
                                "form_name": "building-works-ns",
                                "field_type": "clientSideFileUploadField",
                                "presentation_type": "s3bucketPath",
                                "question": "Upload a condition survey",
                                "path": "upload-a-condition-survey",
                            },
                            {
                                "field_id": "NlDVCg",
                                "form_name": "building-works-ns",
                                "field_type": "clientSideFileUploadField",
                                "presentation_type": "s3bucketPath",
                                "question": "Upload buildings and contents insurance certificate",
                                "path": "upload-buildings-and-contents-insurance-certificate",
                            },
                            {
                                "field_id": "RXIYZY",
                                "form_name": "building-works-ns",
                                "field_type": "yesNoField",
                                "presentation_type": "text",
                                "question": "Do you own the premises?",
                            },
                            {
                                "field_id": "dOyKiO",
                                "form_name": "building-works-ns",
                                "field_type": "clientSideFileUploadField",
                                "presentation_type": "s3bucketPath",
                                "question": "Upload a copy of the land registry title",
                                "path": "upload-a-copy-of-the-land-registry-title",
                            },
                            {
                                "field_id": "rMvZDG",
                                "form_name": "building-works-ns",
                                "field_type": "clientSideFileUploadField",
                                "presentation_type": "s3bucketPath",
                                "question": "Upload the land owner's consent",
                                "path": "upload-the-land-owners-consent",
                            },
                            {
                                "field_id": "wQqPSZ",
                                "form_name": "building-works-ns",
                                "field_type": "clientSideFileUploadField",
                                "presentation_type": "s3bucketPath",
                                "question": "Upload a copy of the lease agreement",
                                "path": "upload-a-copy-of-the-lease-agreement",
                            },
                            {
                                "field_id": "GLOpmu",
                                "form_name": "building-works-ns",
                                "field_type": "clientSideFileUploadField",
                                "presentation_type": "s3bucketPath",
                                "question": "Upload correspondence from your landlord to show that lease renewal discussions have started",
                                "path": "upload-correspondence-from-your-landlord-to-show-that-lease-renewal-discussions-have-started",
                            },
                            {
                                "field_id": "kQJIbS",
                                "form_name": "building-works-ns",
                                "field_type": "clientSideFileUploadField",
                                "presentation_type": "s3bucketPath",
                                "question": "Upload heads of terms outlining new lease agreement",
                                "path": "upload-heads-of-terms-outlining-new-lease-agreement",
                            },
                            {
                                "field_id": "skBfqS",
                                "form_name": "building-works-ns",
                                "field_type": "yesNoField",
                                "presentation_type": "text",
                                "question": "Is the building listed?",
                            },
                            {
                                "field_id": "abdbzq",
                                "form_name": "building-works-ns",
                                "field_type": "clientSideFileUploadField",
                                "presentation_type": "s3bucketPath",
                                "question": "Upload listed building consent",
                                "path": "upload-listed-building-consent",
                            },
                        ],
                    },
                    {
                        "id": "match_funding",
                        "name": "Match funding",
                        "answers": [
                            {
                                "field_id": "nxpXlE",
                                "form_name": "match-funding-ns",
                                "field_type": "yesNoField",
                                "presentation_type": "text",
                                "question": "Will you use match funding for this proposal?",
                            },
                            {
                                "field_id": "uuyBff",
                                "form_name": "match-funding-ns",
                                "field_type": "multiInputField",
                                "presentation_type": "table",
                                "question": [
                                    "Match funding (add another)",
                                    {
                                        "AfAKxk": {
                                            "column_title": "Funding source",
                                            "type": "textField",
                                        },
                                        "CrcLtW": {
                                            "column_title": "Amount",
                                            "type": "numberField",
                                        },
                                        "ndySbC": {
                                            "column_title": "Financial year",
                                            "type": "RadiosField",
                                        },
                                        "pATWyM": {
                                            "column_title": "Which type of funding is it?",
                                            "type": "RadiosField",
                                        },
                                        "sIFBGc": {
                                            "column_title": "Is the funding secured?",
                                            "type": "yesNoField",
                                        },
                                    },
                                ],
                            },
                        ],
                    },
                ],
            }
        ],
    },
]
