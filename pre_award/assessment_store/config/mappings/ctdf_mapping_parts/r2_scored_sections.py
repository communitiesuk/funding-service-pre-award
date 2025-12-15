# ruff: noqa: E501

scored_sections = [
    {
        "id": "strategic_case",
        "weighting": 0.33,
        "name": "Strategic Case",
        "sub_criteria": [
            {
                "id": "project_scope",
                "name": "Project Scope",
                "themes": [
                    {
                        "id": "project_overview",
                        "name": "Project Overview",
                        "answers": [
                            {
                                "field_id": "projectName",
                                "form_name": "ctdf-r2-project-details",
                                "field_type": "textField",
                                "presentation_type": "text",
                                "question": "Project Name",
                            },
                            {
                                "field_id": "projectDescription",
                                "form_name": "ctdf-r2-project-details",
                                "field_type": "freeTextField",
                                "presentation_type": "text",
                                "question": "Project Description",
                            },
                            {
                                "field_id": "projectType",
                                "form_name": "ctdf-r2-project-details",
                                "field_type": "radiosField",
                                "presentation_type": "text",
                                "question": "Project Type",
                            },
                        ],
                    },
                    {
                        "id": "project_details_specifics",
                        "name": "Project Specifics",
                        "answers": [
                            {
                                "field_id": "capitalType",
                                "form_name": "ctdf-r2-project-details",
                                "field_type": "radiosField",
                                "presentation_type": "text",
                                "question": "Capital Work Type",
                            },
                            {
                                "field_id": "revenueActivities",
                                "form_name": "ctdf-r2-project-details",
                                "field_type": "checkboxesField",
                                "presentation_type": "list",
                                "question": "Revenue Activities",
                            },
                        ],
                    },
                ],
            },
            {
                "id": "community_engagement",
                "name": "Community Engagement",
                "themes": [
                    {
                        "id": "engagement_activity",
                        "name": "Engagement Activity",
                        "answers": [
                            {
                                "field_id": "communityEngagement",
                                "form_name": "ctdf-r2-supporting-evidence",
                                "field_type": "radiosField",
                                "presentation_type": "text",
                                "question": "Engagement Level",
                            },
                            {
                                "field_id": "engagementDescription",
                                "form_name": "ctdf-r2-supporting-evidence",
                                "field_type": "freeTextField",
                                "presentation_type": "text",
                                "question": "Engagement Description",
                            },
                            {
                                "field_id": "noEngagementReason",
                                "form_name": "ctdf-r2-supporting-evidence",
                                "field_type": "freeTextField",
                                "presentation_type": "text",
                                "question": "Reason for No Engagement",
                            },
                        ],
                    },
                    {
                        "id": "engagement_outcomes",
                        "name": "Engagement Outcomes",
                        "answers": [
                            {
                                "field_id": "engagementFindings",
                                "form_name": "ctdf-r2-supporting-evidence",
                                "field_type": "freeTextField",
                                "presentation_type": "text",
                                "question": "Engagement Findings",
                            },
                            {
                                "field_id": "hasLettersOfSupport",
                                "form_name": "ctdf-r2-supporting-evidence",
                                "field_type": "yesNoField",
                                "presentation_type": "text",
                                "question": "Letters of Support",
                            },
                        ],
                    },
                ],
            },
        ],
    },
    {
        "id": "financial_case",
        "weighting": 0.33,
        "name": "Financial Case",
        "sub_criteria": [
            {
                "id": "costs_and_funding",
                "name": "Costs and Funding",
                "themes": [
                    {
                        "id": "project_costs",
                        "name": "Project Costs",
                        "answers": [
                            {
                                "field_id": "costBreakdown",
                                "form_name": "ctdf-r2-project-details",
                                "field_type": "multiInputField",
                                "presentation_type": "table",
                                "question": [
                                    "Cost Breakdown",
                                    {
                                        "costItem": {
                                            "column_title": "Cost item",
                                            "type": "textField",
                                        },
                                        "costAmount": {
                                            "column_title": "Amount",
                                            "type": "numberField",
                                        },
                                    },
                                ],
                            },
                        ],
                    },
                    {
                        "id": "funding_package",
                        "name": "Funding Package",
                        "answers": [
                            {
                                "field_id": "fundingRequested",
                                "form_name": "ctdf-r2-project-details",
                                "field_type": "numberField",
                                "presentation_type": "currency",
                                "question": "Funding Requested",
                            },
                            {
                                "field_id": "hasOtherFunding",
                                "form_name": "ctdf-r2-project-details",
                                "field_type": "yesNoField",
                                "presentation_type": "text",
                                "question": "Has Other Funding",
                            },
                            {
                                "field_id": "otherFunding",
                                "form_name": "ctdf-r2-project-details",
                                "field_type": "multiInputField",
                                "presentation_type": "table",
                                "question": [
                                    "Other Funding Sources",
                                    {
                                        "funderName": {
                                            "column_title": "Funder",
                                            "type": "textField",
                                        },
                                        "funderAmount": {
                                            "column_title": "Amount",
                                            "type": "numberField",
                                        },
                                        "funderStatus": {
                                            "column_title": "Status",
                                            "type": "radiosField",
                                        },
                                    },
                                ],
                            },
                        ],
                    },
                ],
            },
            {
                "id": "outputs",
                "name": "Outputs",
                "themes": [
                    {
                        "id": "staffing",
                        "name": "Staffing",
                        "answers": [
                            {
                                "field_id": "newPosts",
                                "form_name": "ctdf-r2-project-details",
                                "field_type": "numberField",
                                "presentation_type": "text",
                                "question": "New Posts Created",
                            },
                            {
                                "field_id": "existingPosts",
                                "form_name": "ctdf-r2-project-details",
                                "field_type": "numberField",
                                "presentation_type": "text",
                                "question": "Existing Posts Supported",
                            },
                        ],
                    },
                ],
            },
        ],
    },
    {
        "id": "management_case",
        "weighting": 0.34,
        "name": "Management Case",
        "sub_criteria": [
            {
                "id": "delivery_plan",
                "name": "Delivery Plan",
                "themes": [
                    {
                        "id": "dates",
                        "name": "Key Dates",
                        "answers": [
                            {
                                "field_id": "projectStartDate",
                                "form_name": "ctdf-r2-project-details",
                                "field_type": "datePartsField",
                                "presentation_type": "text",
                                "question": "Start Date",
                            },
                            {
                                "field_id": "projectEndDate",
                                "form_name": "ctdf-r2-project-details",
                                "field_type": "datePartsField",
                                "presentation_type": "text",
                                "question": "End Date",
                            },
                        ],
                    },
                    {
                        "id": "planning_permission",
                        "name": "Planning Permission",
                        "answers": [
                            {
                                "field_id": "hasPlanning",
                                "form_name": "ctdf-r2-project-details",
                                "field_type": "yesNoField",
                                "presentation_type": "text",
                                "question": "Planning Secured",
                            },
                            {
                                "field_id": "planningStatus",
                                "form_name": "ctdf-r2-project-details",
                                "field_type": "freeTextField",
                                "presentation_type": "text",
                                "question": "Planning Status",
                            },
                        ],
                    },
                ],
            },
            {
                "id": "risks_and_capability",
                "name": "Risks and Capability",
                "themes": [
                    {
                        "id": "risk_management",
                        "name": "Risk Management",
                        "answers": [
                            {
                                "field_id": "hasRiskRegister",
                                "form_name": "ctdf-r2-supporting-evidence",
                                "field_type": "yesNoField",
                                "presentation_type": "text",
                                "question": "Risk Register Identified",
                            },
                            {
                                "field_id": "projectRisks",
                                "form_name": "ctdf-r2-supporting-evidence",
                                "field_type": "multiInputField",
                                "presentation_type": "table",
                                "question": [
                                    "Project Risks",
                                    {
                                        "riskDescription": {
                                            "column_title": "Risk",
                                            "type": "textField",
                                        },
                                        "riskLikelihood": {
                                            "column_title": "Likelihood",
                                            "type": "radiosField",
                                        },
                                        "riskMitigation": {
                                            "column_title": "Mitigation",
                                            "type": "textField",
                                        },
                                    },
                                ],
                            },
                        ],
                    },
                    {
                        "id": "project_team",
                        "name": "Project Team",
                        "answers": [
                            {
                                "field_id": "projectTeam",
                                "form_name": "ctdf-r2-organisation-information",
                                "field_type": "multiInputField",
                                "presentation_type": "table",
                                "question": [
                                    "Team Members",
                                    {
                                        "teamMemberName": {
                                            "column_title": "Name",
                                            "type": "textField",
                                        },
                                        "teamMemberRole": {
                                            "column_title": "Role",
                                            "type": "textField",
                                        },
                                        "teamMemberEmail": {
                                            "column_title": "Email",
                                            "type": "emailAddressField",
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
