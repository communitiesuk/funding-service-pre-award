# ruff: noqa: E501

scored_criteria = [
    {
        "id": "your-skills-and-experience",
        "name": "Your skills and experience",
        "weighting": 0.35,
        "sub_criteria": [
            {
                "id": "your-skills-and-experience",
                "name": "Your skills and experience",
                "themes": [
                    {
                        "id": "your-skills-and-experience",
                        "name": "Your skills and experience",
                        "answers": [
                            {
                                "field_id": "HrGXKi",
                                "form_name": "your-skills-and-experience-cyp",
                                "field_type": "yesNoField",
                                "presentation_type": "text",
                                "question": "Have you delivered projects like this before?",
                            },
                            {
                                "field_id": "qPcbJQ",
                                "form_name": "skills-and-experience-cyp",
                                "field_type": "freeTextField",
                                "presentation_type": "free_text",
                                "question": "Tell us about how you have worked on similar previous projects",
                            },
                        ],
                    },
                ],
            },
        ],
    },
    {
        "id": "your-project",
        "name": "Your project",
        "weighting": 0.40,
        "sub_criteria": [
            {
                "id": "outputs",
                "name": "Outputs",
                "themes": [
                    {
                        "id": "outputs",
                        "name": "Outputs",
                        "answers": [
                            {
                                "field_id": "MADkNZ",
                                "form_name": "outputs-and-outcomes-cyp",
                                "field_type": "freeTextField",
                                "presentation_type": "free_text",
                                "question": "Give a brief summary of your project, including what you hope to achieve",
                            },
                            {
                                "field_id": "fHodTO",
                                "form_name": "outputs-and-outcomes-cyp",
                                "field_type": "checkboxesField",
                                "presentation_type": "list",
                                "question": "What is the main focus of your project?",
                            },
                            {
                                "field_id": "vYYoAC",
                                "form_name": "outputs-and-outcomes-cyp",
                                "field_type": "checkboxesField",
                                "presentation_type": "list",
                                "question": "Which cohort will your project focus on?",
                            },
                            {
                                "field_id": "tAtJGz",
                                "form_name": "outputs-and-outcomes-cyp",
                                "field_type": "numberField",
                                "presentation_type": "integer",
                                "question": "How many fund recipients from the Ukraine schemes do you expect your project to support with the funding?",
                            },
                            {
                                "field_id": "tBwdYp",
                                "form_name": "outputs-and-outcomes-cyp",
                                "field_type": "numberField",
                                "presentation_type": "integer",
                                "question": "How many fund recipients from the Hong Kong British National (Overseas) cohort do you expect your project to support with the funding?",
                            },
                            {
                                "field_id": "rhmmaQ",
                                "form_name": "outputs-and-outcomes-cyp",
                                "field_type": "numberField",
                                "presentation_type": "integer",
                                "question": "How many fund recipients from the Afghan Citizens Resettlement Scheme do you expect your project to support with the funding?",
                            },
                        ],
                    },
                ],
            },
            {
                "id": "outcome",
                "name": "Outcome",
                "themes": [
                    {
                        "id": "outcome",
                        "name": "Outcome",
                        "answers": [
                            {
                                "field_id": "nbDkNZ",
                                "form_name": "outputs-and-outcomes-cyp",
                                "field_type": "freeTextField",
                                "presentation_type": "free_text",
                                "question": "How will you measure the outcome of your project?",
                            },
                        ],
                    },
                ],
            },
            {
                "id": "existing-work",
                "name": "Existing work",
                "themes": [
                    {
                        "id": "existing-work",
                        "name": "Existing work",
                        "answers": [
                            {
                                "field_id": "MbDkNZ",
                                "form_name": "existing-work-cyp",
                                "field_type": "freeTextField",
                                "presentation_type": "free_text",
                                "question": "How will you avoid duplicating existing work or projects in this area?",
                            },
                        ],
                    },
                ],
            },
            {
                "id": "project-milestones",
                "name": "Project milestones",
                "themes": [
                    {
                        "id": "project-milestones",
                        "name": "Project milestones",
                        "answers": [
                            {
                                "field_id": "tAoOKx",
                                "form_name": "project-milestones-cyp",
                                "field_type": "multiInputField",
                                "presentation_type": "table",
                                "question": [
                                    "Project milestones",
                                    {
                                        "HpLJDu": {
                                            "column_title": "Milestone",
                                            "type": "multilineTextField",
                                        },
                                        "LZbOBu": {
                                            "column_title": "When will you reach this milestone?",
                                            "type": "monthYearField",
                                        },
                                    },
                                ],
                            },
                        ],
                    },
                ],
            },
            {
                "id": "objectives-and-activities",
                "name": "Objectives and activities",
                "themes": [
                    {
                        "id": "objectives-and-activities",
                        "name": "Objectives and activities",
                        "answers": [
                            {
                                "field_id": "tAoPKx",
                                "form_name": "objectives-and-activities-cyp",
                                "field_type": "multiInputField",
                                "presentation_type": "table",
                                "question": [
                                    "Objectives and activities",
                                    {
                                        "kaQUfV": {
                                            "column_title": "Objective",
                                            "type": "textField",
                                        },
                                        "HpLJCu": {
                                            "column_title": "Activities that will help you achieve the objective",
                                            "type": "multilineTextField",
                                        },
                                    },
                                ],
                            },
                        ],
                    },
                ],
            },
            {
                "id": "location-of-activities",
                "name": "Location of activities",
                "themes": [
                    {
                        "id": "location-of-activities",
                        "name": "Location of activities",
                        "answers": [
                            {
                                "field_id": "iqqqTk",
                                "form_name": "location-of-activities-cyp",
                                "field_type": "yesNoField",
                                "presentation_type": "text",
                                "question": "Is the project taking place regionally?",
                            },
                            {
                                "field_id": "tApPKx",
                                "form_name": "location-of-activities-cyp",
                                "field_type": "multiInputField",
                                "presentation_type": "table",
                                "question": [
                                    "Which local authority areas will you work across?",
                                    {
                                        "kaQUSV": {
                                            "column_title": "Local authority areas",
                                            "type": "textField",
                                        },
                                    },
                                ],
                            },
                        ],
                    },
                ],
            },
            {
                "id": "working-with-fund-beneficiaries",
                "name": "Working with fund beneficiaries",
                "themes": [
                    {
                        "id": "working-with-fund-beneficiaries",
                        "name": "Working with fund beneficiaries",
                        "answers": [
                            {
                                "field_id": "XPDbsh",
                                "form_name": "working-with-fund-beneficiaries-cyp",
                                "field_type": "freeTextField",
                                "presentation_type": "free_text",
                                "question": "Tell us how you will identify and work with the intended fund beneficiaries",
                            },
                        ],
                    },
                ],
            },
        ],
    },
    {
        "id": "risk-and-deliverability",
        "name": "Risk and deliverability",
        "weighting": 0.15,
        "sub_criteria": [
            {
                "id": "risk-and-deliverability",
                "name": "Risk and deliverability",
                "themes": [
                    {
                        "id": "risk-and-deliverability",
                        "name": "Risk and deliverability",
                        "answers": [
                            {
                                "field_id": "qQLYzL",
                                "form_name": "risk-and-deliverability-cyp",
                                "field_type": "multiInputField",
                                "presentation_type": "table",
                                "question": [
                                    "Risks to the project",
                                    {
                                        "CzoasH": {
                                            "column_title": "Risk",
                                            "type": "multilineTextField",
                                        },
                                        "eADHGN": {
                                            "column_title": "Likelihood",
                                            "type": "radiosField",
                                        },
                                        "MPHvIr": {
                                            "column_title": "Impact",
                                            "type": "radiosField",
                                        },
                                        "SKQluJ": {
                                            "column_title": "Proposed mitigation",
                                            "type": "multilineTextField",
                                        },
                                    },
                                ],
                            },
                            {
                                "field_id": "KHESdE",
                                "form_name": "risk-and-deliverability-cyp",
                                "field_type": "textField",
                                "presentation_type": "text",
                                "question": "Who owns the overall risk register?",
                            },
                            {
                                "field_id": "KHESFr",
                                "form_name": "risk-and-deliverability-cyp",
                                "field_type": "freeTextField",
                                "presentation_type": "free_text",
                                "question": "Tell us about your organisation's governance structure",
                            },
                        ],
                    },
                ],
            },
        ],
    },
    {
        "id": "value-for-money",
        "name": "Value for money",
        "weighting": 0.10,
        "sub_criteria": [
            {
                "id": "value-for-money",
                "name": "Value for money",
                "themes": [
                    {
                        "id": "value-for-money",
                        "name": "Value for money",
                        "answers": [
                            {
                                "field_id": "JXKUcj",
                                "form_name": "value-for-money-cyp",
                                "field_type": "numberField",
                                "presentation_type": "currency",
                                "question": "Funding requested 27 September 2023 to 31 March 2024",
                            },
                            {
                                "field_id": "OnPeeS",
                                "form_name": "value-for-money-cyp",
                                "field_type": "numberField",
                                "presentation_type": "currency",
                                "question": "Funding requested 1 April 2024 to 31 March 2025",
                            },
                            {
                                "field_id": "qwktzL",
                                "form_name": "value-for-money-cyp",
                                "field_type": "multiInputField",
                                "presentation_type": "table",
                                "question": [
                                    "Item of expenditure",
                                    {
                                        "gLQlyJ": {
                                            "column_title": "Item of expenditure",
                                            "type": "textField",
                                        },
                                        "JizgZP": {
                                            "column_title": "Amount",
                                            "type": "numberField",
                                        },
                                        "kjuHtl": {
                                            "column_title": "Year",
                                            "type": "radiosField",
                                        },
                                    },
                                ],
                            },
                            {
                                "field_id": "qwktlZ",
                                "form_name": "value-for-money-cyp",
                                "field_type": "yesNoField",
                                "presentation_type": "text",
                                "question": "Will you use additional funding for your project?",
                            },
                            {
                                "field_id": "qqktzL",
                                "form_name": "value-for-money-cyp",
                                "field_type": "multiInputField",
                                "presentation_type": "table",
                                "question": [
                                    "Additional funding",
                                    {
                                        "gLqiyJ": {
                                            "column_title": "Funding source",
                                            "type": "textField",
                                        },
                                        "yuzbjT": {
                                            "column_title": "Amount",
                                            "type": "numberField",
                                        },
                                        "HpLJyL": {
                                            "column_title": "When is the additional funding available from?",
                                            "type": "monthYearField",
                                        },
                                        "MadvIr": {
                                            "column_title": "Which type of funding is it?",
                                            "type": "radiosField",
                                        },
                                    },
                                ],
                            },
                        ],
                    },
                ],
            },
        ],
    },
]
