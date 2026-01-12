# ruff: noqa: E501

scored_sections = [
    {
        "id": "problem_statement",
        "weighting": 0.05,
        "name": "Problem statement",
        "sub_criteria": [
            {
                "id": "problem_statement",
                "name": "Problem statement",
                "themes": [
                    {
                        "id": "problem_statement",
                        "name": "Problem statement",
                        "answers": [
                            {
                                "field_id": "lTFJnY",
                                "form_name": "shif-apply-your-proposal",
                                "field_type": "freeTextField",
                                "presentation_type": "text",
                                "question": """What challenges are you trying to address?
                                 <p>This is your problem statement. Provide any supporting evidence you may have, including evidence from tenants.</p>
                                 <p>(Max 300 words)</p>""",
                            },
                        ],
                    }
                ],
            },
        ],
    },
    {
        "id": "your_proposal",
        "weighting": 0.25,
        "name": "Your proposal",
        "sub_criteria": [
            {
                "id": "your_proposal",
                "name": "Your proposal",
                "themes": [
                    {
                        "id": "your_proposal",
                        "name": "Your proposal",
                        "answers": [
                            {
                                "field_id": "RlFFTW",
                                "form_name": "shif-apply-your-proposal",
                                "field_type": "textField",
                                "presentation_type": "text",
                                "question": "What is the name of your project?",
                            },
                            {
                                "field_id": "FFNuZw",
                                "form_name": "shif-apply-your-proposal",
                                "field_type": "freeTextField",
                                "presentation_type": "text",
                                "question": """How will the proposal address the challenges specified in your problem statement?
                                    <p>Include:</p>
                                    <ul>
                                        <li>
                                            the objectives of your project and they align with the grant's objectives as set out in the prospectus
                                        </li>
                                        <li>
                                            planned activities and how they will benefit tenants
                                        </li>
                                        <li>
                                            key milestones and timescales (more detail can be set out in a separate project plan)
                                        </li>
                                    </ul>
                                    <p>
                                        For consortium bids, clearly outline each partner's role in delivering the projects.
                                    </p>
                                    <p>
                                        (Max 700 words)
                                    </p>""",
                            },
                            {
                                "field_id": "PdxtmT",
                                "form_name": "shif-apply-your-proposal",
                                "field_type": "clientSideFileUploadField",
                                "presentation_type": "s3bucketPath",
                                "question": """Upload your project plan
                                 <p>The document must be no more than 3 pages.</p>
                                 <p>PDF or Excel files only, maximum 10MB</p>""",
                                "path": "upload-your-project-plan",
                            },
                        ],
                    }
                ],
            },
        ],
    },
    {
        "id": "others_involved",
        "weighting": 0.05,
        "name": "Who is involved in implementation",
        "sub_criteria": [
            {
                "id": "others_involved",
                "name": "Who is involved in implementation",
                "themes": [
                    {
                        "id": "others_involved",
                        "name": "Who is involved in implementation",
                        "answers": [
                            {
                                "field_id": "Fxpsiw",
                                "form_name": "shif-apply-your-proposal",
                                "field_type": "freeTextField",
                                "presentation_type": "text",
                                "question": """Who will be involved in implementing the proposal?
                                <p>
                                    This can include consortium members, tenant representatives, public sector partners, voluntary
                                    and community sector organisations (VCSOs) and technology companies.
                                </p>
                                <p>(Max 300 words)</p>
                                """,
                            },
                        ],
                    }
                ],
            },
        ],
    },
    {
        "id": "co_production_with_tenants",
        "weighting": 0.2,
        "name": "Co-production with tenants",
        "sub_criteria": [
            {
                "id": "co_production_with_tenants",
                "name": "Co-production with tenants",
                "themes": [
                    {
                        "id": "co_production_with_tenants",
                        "name": "Co-production with tenants",
                        "answers": [
                            {
                                "field_id": "CjawNO",
                                "form_name": "shif-apply-co-production-with-tenants",
                                "field_type": "freeTextField",
                                "presentation_type": "text",
                                "question": """How, and to what extent, have tenants been involved in co-producing your proposal?
                                <p>Include details on how will they be involved in:</p>
                                <ul>
                                    <li>
                                        the design and delivery of the project
                                    </li>
                                    <li>
                                        monitoring the outcomes of the project
                                    </li>
                                </ul>
                                <p>
                                    Applicants will score higher if they can demonstrate projects are tenant-led, or a high level of tenant
                                    involvement at all stages of the design and delivery of the project.
                                </p>
                                <p>(Max 350 words)</p>
                                """,
                            },
                        ],
                    }
                ],
            },
        ],
    },
    {
        "id": "innovation",
        "weighting": 0.1,
        "name": "Innovation",
        "sub_criteria": [
            {
                "id": "innovation",
                "name": "Innovation",
                "themes": [
                    {
                        "id": "innovation",
                        "name": "Innovation",
                        "answers": [
                            {
                                "field_id": "WJTBzi",
                                "form_name": "shif-apply-innovation-and-scalability",
                                "field_type": "freeTextField",
                                "presentation_type": "text",
                                "question": """How is the proposed project innovative?
                                    <p>To be deemed 'innovative', the project must:</p>
                                    <ul>
                                        <li>
                                            introduce new or significantly improved approaches, technologies or partnerships to enhance
                                            tenant outcomes and improve overall resident experience
                                        </li>
                                        <li>
                                            challenge conventional practices across the sector more widely and respond
                                            creatively to tenant needs
                                        </li>
                                    </ul>
                                    <p>
                                        The grant can be used to expand or build upon an existing project, but cannot be used to fund
                                        business as usual activities.
                                    </p>
                                    <p>(Max 500 words)</p>
                                """,
                            },
                        ],
                    }
                ],
            },
        ],
    },
    {
        "id": "scalability",
        "weighting": 0.1,
        "name": "Scalability",
        "sub_criteria": [
            {
                "id": "scalability",
                "name": "Scalability",
                "themes": [
                    {
                        "id": "scalability",
                        "name": "Scalability",
                        "answers": [
                            {
                                "field_id": "czkAFo",
                                "form_name": "shif-apply-innovation-and-scalability",
                                "field_type": "freeTextField",
                                "presentation_type": "text",
                                "question": """How does this project have the potential to be scaled up or replicated on a wider scale?
                                <p>
                                    Describe how the learnings from this project could have benefits for social housing tenants
                                    more broadly across the country.
                                </p>
                                <p>(Max 300 words)</p>
                                """,
                            },
                        ],
                    }
                ],
            },
        ],
    },
    {
        "id": "costs_and_value_for_money",
        "weighting": 0.05,
        "name": "Costs and value for money",
        "sub_criteria": [
            {
                "id": "costs_and_value_for_money",
                "name": "Costs and value for money",
                "themes": [
                    {
                        "id": "costs_and_value_for_money",
                        "name": "Costs and value for money",
                        "answers": [
                            {
                                "field_id": "BwHiiN",
                                "form_name": "shif-apply-costs-and-value-for-money",
                                "field_type": "yesNoField",
                                "presentation_type": "text",
                                "question": "Are you seeking funding to cover the total cost of the project?",
                            },
                            {
                                "field_id": "UoneMB",
                                "form_name": "shif-apply-costs-and-value-for-money",
                                "field_type": "numberField",
                                "presentation_type": "text",
                                "question": """How much funding are you seeking and what is the total cost of your project?
                                    <p>
                                        This is the total amount of funding you are applying for from the Social Housing Innovation Fund.
                                        Include any non-recoverable VAT within your project total cost.
                                    </p>
                                    <p>Total funding requested</p>
                                """,
                            },
                            {
                                "field_id": "vltUZa",
                                "form_name": "shif-apply-costs-and-value-for-money",
                                "field_type": "numberField",
                                "presentation_type": "text",
                                "question": "Total cost of project",
                            },
                            {
                                "field_id": "LBPcsu",
                                "form_name": "shif-apply-costs-and-value-for-money",
                                "field_type": "freeTextField",
                                "presentation_type": "text",
                                "question": """How will you fund the outstanding costs of the project?
                                    <p>(Max 250 words)</p>
                                    """,
                            },
                            {
                                "field_id": "OdMILX",
                                "form_name": "shif-apply-costs-and-value-for-money",
                                "field_type": "numberField",
                                "presentation_type": "text",
                                "question": """How much funding are you seeking for your project?
                                    <p>
                                        This is the total amount of funding you are applying for from the Social Housing Innovation Fund.
                                    </p>
                                    <p>
                                        The indicative range of funding per project will be £60,000 to £120,000, with the latter
                                        being the maximum amount awarded. Bids under £60,000 will still be considered.
                                    </p>
                                    <p>
                                        Include any non-recoverable VAT within your project total cost.
                                    </p>
                                """,
                            },
                            {
                                "field_id": "eeNMwb",
                                "form_name": "shif-apply-costs-and-value-for-money",
                                "field_type": "yesNoField",
                                "presentation_type": "text",
                                "question": "Does this include non-recoverable VAT costs?",
                            },
                            {
                                "field_id": "bKXFmG",
                                "form_name": "shif-apply-costs-and-value-for-money",
                                "field_type": "freeTextField",
                                "presentation_type": "text",
                                "question": """Describe your project budget and assumptions
                                 <p>
                                    This should include:
                                </p>
                                <ul>
                                    <li>
                                        the key costs for your project
                                    </li>
                                    <li>
                                        your assumptions
                                    </li>
                                    <li>
                                        how you have assessed budget lines of expenditure
                                    </li>
                                </ul>
                                <p>
                                    For example, if you are setting out staffing costs, provide a breakdown of each staff member
                                    and their role. If you are setting out supply costs, set out how you have estimated these costs.
                                </p>
                                <p>(Max 300 words)</p>
                                """,
                            },
                            {
                                "field_id": "KVZvBK",
                                "form_name": "shif-apply-costs-and-value-for-money",
                                "field_type": "clientSideFileUploadField",
                                "presentation_type": "s3bucketPath",
                                "question": """Upload your project budget with a breakdown of the key costs of your project
                                    <p>The document must be no more than 3 pages.</p>
                                    <p>PDF or Excel files only, maximum 10MB</p>
                                """,
                                "path": "upload-your-project-budget-with-a-breakdown-of-the-key-costs-of-your-project",
                            },
                            {
                                "field_id": "gRddtf",
                                "form_name": "shif-apply-costs-and-value-for-money",
                                "field_type": "freeTextField",
                                "presentation_type": "text",
                                "question": """How will your project deliver value for money?
                                     <p>(Max 200 words)</p>
                                """,
                            },
                        ],
                    },
                ],
            },
        ],
    },
    {
        "id": "risk_management",
        "weighting": 0.05,
        "name": "Risk management",
        "sub_criteria": [
            {
                "id": "risk_management",
                "name": "Risk management",
                "themes": [
                    {
                        "id": "risk_management",
                        "name": "Risk management",
                        "answers": [
                            {
                                "field_id": "WkOXbJ",
                                "form_name": "shif-apply-risk-management",
                                "field_type": "freeTextField",
                                "presentation_type": "text",
                                "question": """What risks have you identified, and how will you manage and mitigate these risks?
                                    <p>(Max 200 words)</p>
                                """,
                            },
                        ],
                    }
                ],
            },
        ],
    },
    {
        "id": "outcomes_and_impact",
        "weighting": 0.1,
        "name": "Outcomes and impact",
        "sub_criteria": [
            {
                "id": "outcomes_and_impact",
                "name": "Outcomes and impact",
                "themes": [
                    {
                        "id": "outcomes_and_impact",
                        "name": "Outcomes and impact",
                        "answers": [
                            {
                                "field_id": "PHcUVY",
                                "form_name": "shif-apply-outcomes-and-measuring-impact",
                                "field_type": "freeTextField",
                                "presentation_type": "text",
                                "question": """Describe the positive impacts your project is expected to have
                                    <p>This should include:</p>
                                <ul>
                                    <li>
                                        who and how many people will benefit
                                    </li>
                                    <li>
                                        when you expect to see these benefits
                                    </li>
                                    <li>
                                        how will the project improve tenants’ experience of social housing
                                    </li>
                                </ul>
                                <p>(Max 500 words)</p>
                                """,
                            },
                        ],
                    }
                ],
            },
        ],
    },
    {
        "id": "proposed_kpis",
        "weighting": 0.05,
        "name": "Proposed KPIs",
        "sub_criteria": [
            {
                "id": "proposed_kpis",
                "name": "Proposed KPIs",
                "themes": [
                    {
                        "id": "proposed_kpis",
                        "name": "Proposed KPIs",
                        "answers": [
                            {
                                "field_id": "oRkpsw",
                                "form_name": "shif-apply-outcomes-and-measuring-impact",
                                "field_type": "freeTextField",
                                "presentation_type": "text",
                                "question": """What key performance indicators (KPIs) you will use to monitor the success of your project?
                                    <p>
                                        Describe how you will use both quantitative and qualitative data to measure success.
                                        Finalised KPIs and targets must be agreed with MHCLG if your application is successful.
                                    </p>
                                    <p>(Max 250 words)</p>
                                """,
                            },
                        ],
                    }
                ],
            },
        ],
    },
]
