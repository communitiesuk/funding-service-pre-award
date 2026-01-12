# ruff: noqa: E501

unscored_sections = [
    {
        "id": "unscored",
        "name": "Unscored",
        "sub_criteria": [
            {
                "id": "organisation_information",
                "name": "Organisation information",
                "themes": [
                    {
                        "id": "organisation_information",
                        "name": "Organisation information",
                        "answers": [
                            {
                                "field_id": "oEoIjK",
                                "form_name": "shif-apply-organisation-information",
                                "field_type": "textField",
                                "presentation_type": "text",
                                "question": """What is your organisation's name?
                                    <p>
                                        If the organisation is known by more than one name, this should be the official name
                                        registered with Companies House or the Charity Commission
                                    </p>
                                """,
                            },
                            {
                                "field_id": "WdapOj",
                                "form_name": "shif-apply-organisation-information",
                                "field_type": "textField",
                                "presentation_type": "text",
                                "question": """Who is the lead contact in your organisation?
                                    <p>
                                        This will be the main point of contact for any queries we may have about your application.
                                    </p>
                                    <p>Full name</p>

                                """,
                            },
                            {
                                "field_id": "SAcHge",
                                "form_name": "shif-apply-organisation-information",
                                "field_type": "textField",
                                "presentation_type": "text",
                                "question": "Role",
                            },
                            {
                                "field_id": "YaGHMI",
                                "form_name": "shif-apply-organisation-information",
                                "field_type": "emailAddressField",
                                "presentation_type": "text",
                                "question": "Email address",
                            },
                            {
                                "field_id": "HZkwbv",
                                "form_name": "shif-apply-organisation-information",
                                "field_type": "telephoneNumberField",
                                "presentation_type": "text",
                                "question": "Contact number",
                            },
                            {
                                "field_id": "wzawYs",
                                "form_name": "shif-apply-organisation-information",
                                "field_type": "ukAddressField",
                                "presentation_type": "text",
                                "question": "What is your organisation address?",
                            },
                            {
                                "field_id": "Hdpmjk",
                                "form_name": "shif-apply-organisation-information",
                                "field_type": "yesNoField",
                                "presentation_type": "text",
                                "question": "Does your organisation have alternative names?",
                            },
                            {
                                "field_id": "BYlNmu",
                                "form_name": "shif-apply-organisation-information",
                                "field_type": "multiInputField",
                                "presentation_type": "table",
                                "question": [
                                    "Alternative organisation name",
                                    {
                                        "UWIOHw": {
                                            "column_title": "Alternative organisation names",
                                            "type": "textField",
                                        },
                                    },
                                ],
                            },
                            {
                                "field_id": "xCuiwp",
                                "form_name": "shif-apply-organisation-information",
                                "field_type": "radiosField",
                                "presentation_type": "text",
                                "question": "What is the legal status of your organisation?",
                            },
                            {
                                "field_id": "FAxOez",
                                "form_name": "shif-apply-organisation-information",
                                "field_type": "yesNoField",
                                "presentation_type": "text",
                                "question": "Is your organisation a charity?",
                            },
                            {
                                "field_id": "jWNmMa",
                                "form_name": "shif-apply-organisation-information",
                                "field_type": "radiosField",
                                "presentation_type": "text",
                                "question": "Where is the charity registered?",
                            },
                            {
                                "field_id": "fidvDS",
                                "form_name": "shif-apply-organisation-information",
                                "field_type": "textField",
                                "presentation_type": "text",
                                "question": "What is your charity number?",
                            },
                            {
                                "field_id": "XutYBr",
                                "form_name": "shif-apply-organisation-information",
                                "field_type": "yesNoField",
                                "presentation_type": "text",
                                "question": "Do you have a company registration number?",
                            },
                            {
                                "field_id": "siMJHb",
                                "form_name": "shif-apply-organisation-information",
                                "field_type": "textField",
                                "presentation_type": "text",
                                "question": "What is your company registration number?",
                            },
                            {
                                "field_id": "RIIeoh",
                                "form_name": "shif-apply-organisation-information",
                                "field_type": "yesNoField",
                                "presentation_type": "text",
                                "question": "Is your organisation controlled by another entity?",
                            },
                            {
                                "field_id": "oDIZBr",
                                "form_name": "shif-apply-organisation-information",
                                "field_type": "textField",
                                "presentation_type": "text",
                                "question": "What is the name of the entity that controls your organisation?",
                            },
                            {
                                "field_id": "AoXseh",
                                "form_name": "shif-apply-organisation-information",
                                "field_type": "yesNoField",
                                "presentation_type": "text",
                                "question": "Are you submitting a consortium bid for funding with one or more organisations?",
                            },
                            {
                                "field_id": "dkmJFS",
                                "form_name": "shif-apply-organisation-information",
                                "field_type": "multiInputField",
                                "presentation_type": "table",
                                "question": [
                                    "Tell us the details of all the other organisations involved in the consortium bid or partnership",
                                    {
                                        "aVcweG": {
                                            "column_title": "Organisation name",
                                            "type": "textField",
                                        },
                                        "TQCUbc": {
                                            "column_title": "Alternative name (optional)",
                                            "type": "textField",
                                        },
                                        "sJkxaS": {
                                            "column_title": "Organisation address",
                                            "type": "ukAddressField",
                                        },
                                        "HLqXjr": {
                                            "column_title": "Parent organisation or holding company name (if applicable)",
                                            "type": "textField",
                                        },
                                    },
                                ],
                            },
                        ],
                    }
                ],
            },
            {
                "id": "declarations",
                "name": "Declarations",
                "themes": [
                    {
                        "id": "declarations",
                        "name": "Declarations",
                        "answers": [
                            {
                                "field_id": "Ydztii",
                                "form_name": "shif-apply-declarations",
                                "field_type": "checkboxesField",
                                "presentation_type": "text",
                                "question": """Declarations
                                <p>
                                    Confirm that you have read and agree with the following declarations
                                </p>
                                <ul>
                                    <li>
                                        My organisation will not make a profit from activities supported by grant funding
                                    </li>
                                    <li>
                                        Any awarded funding will not be used to undertake political activity nor support ideological or
                                        extremist causes ('extremism' is defined in the 2011 Prevent strategy (opens in new tab) as vocal
                                        or active opposition to fundamental British values, including democracy, the rule of law, individual
                                        liberty and mutual respect and tolerance of different faiths and beliefs)
                                    </li>
                                    <li>
                                        The information provided in this application is accurate to the best of my knowledge on the date
                                        of submission
                                    </li>
                                </ul>

                                """,
                            },
                        ],
                    },
                ],
            },
        ],
    },
]
