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
                                "field_id": "GtoolQ",
                                "form_name": "nwp-shared-organisation-information",
                                "field_type": "textField",
                                "presentation_type": "text",
                                "question": "<h3>What is the name of your organisation?</h3>Give the official name registered with companies house or trading standards.",
                            },
                            {
                                "field_id": "JwFyrI",
                                "form_name": "nwp-shared-organisation-information",
                                "field_type": "textField",
                                "presentation_type": "text",
                                "question": "Give any alternative names that your organisation is known by.",
                            },
                            {
                                "field_id": "rmuxRd",
                                "form_name": "nwp-shared-organisation-information",
                                "field_type": "ukAddressField",
                                "presentation_type": "text",
                                "question": "What is your organisation's address?",
                            },
                            {
                                "field_id": "wdsvxz",
                                "form_name": "nwp-shared-organisation-information",
                                "field_type": "multilineTextField",
                                "presentation_type": "text",
                                "question": "What is your organisation's main purpose?",
                            },
                            {
                                "field_id": "obNwIa",
                                "form_name": "nwp-shared-organisation-information",
                                "field_type": "textField",
                                "presentation_type": "text",
                                "question": "What is your VAT registration number?",
                            },
                            {
                                "field_id": "zJJSsR",
                                "form_name": "nwp-shared-organisation-information",
                                "field_type": "clientSideFileUploadField",
                                "presentation_type": "s3bucketPath",
                                "question": "Upload your current insurance certificate.",
                                "path": "what-are-your-insurance-details",
                            },
                            {
                                "field_id": "JiaoiU",
                                "form_name": "nwp-shared-organisation-information",
                                "field_type": "websiteField",
                                "presentation_type": "text",
                                "question": "What is your organisation's website?",
                            },
                            {
                                "field_id": "uPoAaU",
                                "form_name": "nwp-shared-organisation-information",
                                "field_type": "multilineTextField",
                                "presentation_type": "text",
                                "question": "What are your organisation's social media accounts?",
                            },
                            {
                                "field_id": "fFNPbo",
                                "form_name": "nwp-shared-organisation-information",
                                "field_type": "multilineTextField",
                                "presentation_type": "text",
                                "question": "What professional associations is your organisation a member of?",
                            },
                            {
                                "field_id": "UstMrg",
                                "form_name": "nwp-shared-organisation-information",
                                "field_type": "multilineTextField",
                                "presentation_type": "text",
                                "question": "Provide a summary or mission statement for your organisation.",
                            },
                            {
                                "field_id": "org",
                                "form_name": "nwp-shared-organisation-information",
                                "field_type": "radiosField",
                                "presentation_type": "text",
                                "question": "What is your organisation type?",
                            },
                            {
                                "field_id": "RlaAvC",
                                "form_name": "nwp-shared-organisation-information",
                                "field_type": "yesNoField",
                                "presentation_type": "text",
                                "question": "Do you have a charity number?",
                            },
                            {
                                "field_id": "ZIIeJF",
                                "form_name": "nwp-shared-organisation-information",
                                "field_type": "textField",
                                "presentation_type": "text",
                                "question": "What is your charity number?",
                            },
                            {
                                "field_id": "dJqsly",
                                "form_name": "nwp-shared-organisation-information",
                                "field_type": "multilineTextField",
                                "presentation_type": "text",
                                "question": "What are the names of your trustees?",
                            },
                            {
                                "field_id": "WuTLHg",
                                "form_name": "nwp-shared-organisation-information",
                                "field_type": "yesNoField",
                                "presentation_type": "text",
                                "question": "Do you have a company registration number?",
                            },
                            {
                                "field_id": "yzcfRk",
                                "form_name": "nwp-shared-organisation-information",
                                "field_type": "textField",
                                "presentation_type": "text",
                                "question": "What is your company registration number?",
                            },
                            {
                                "field_id": "EXdHkT",
                                "form_name": "nwp-shared-organisation-information",
                                "field_type": "multilineTextField",
                                "presentation_type": "text",
                                "question": "What are the names of your directors?",
                            },
                            {
                                "field_id": "RInsJl",
                                "form_name": "nwp-shared-organisation-information",
                                "field_type": "yesNoField",
                                "presentation_type": "text",
                                "question": "Is there a parent or holding organisation?",
                            },
                            {
                                "field_id": "MKIpgA",
                                "form_name": "nwp-shared-organisation-information",
                                "field_type": "textField",
                                "presentation_type": "text",
                                "question": "What is the name of the parent or holding organisation?",
                            },
                            {
                                "field_id": "YmiBVh",
                                "form_name": "nwp-shared-organisation-information",
                                "field_type": "clientSideFileUploadField",
                                "presentation_type": "s3bucketPath",
                                "question": "What is the structure of your organisation?",
                                "path": "what-is-the-structure-of-your-organisation",
                            },
                        ],
                    }
                ],
            },
            {
                "id": "applicant_information",
                "name": "Applicant information",
                "themes": [
                    {
                        "id": "applicant_information",
                        "name": "Applicant information",
                        "answers": [
                            {
                                "field_id": "HqzHaG",
                                "form_name": "nwp-shared-applicant-information",
                                "field_type": "textField",
                                "presentation_type": "text",
                                "question": "<h3>Who is the accountable officer for your organisation?</h3>Full name",
                            },
                            {
                                "field_id": "Role",
                                "form_name": "nwp-shared-applicant-information",
                                "field_type": "textField",
                                "presentation_type": "text",
                                "question": "Role",
                            },
                            {
                                "field_id": "cKnBaI",
                                "form_name": "nwp-shared-applicant-information",
                                "field_type": "emailAddressField",
                                "presentation_type": "text",
                                "question": "Email address",
                            },
                            {
                                "field_id": "Telephonenumber",
                                "form_name": "nwp-shared-applicant-information",
                                "field_type": "telephoneNumberField",
                                "presentation_type": "text",
                                "question": "Telephone number",
                            },
                            {
                                "field_id": "VPYbgU",
                                "form_name": "nwp-shared-applicant-information",
                                "field_type": "textField",
                                "presentation_type": "text",
                                "question": "<h3>Who is the lead officer for your organisation?</h3>Full name",
                            },
                            {
                                "field_id": "zQeJlv",
                                "form_name": "nwp-shared-applicant-information",
                                "field_type": "textField",
                                "presentation_type": "text",
                                "question": "Role",
                            },
                            {
                                "field_id": "ZjafAo",
                                "form_name": "nwp-shared-applicant-information",
                                "field_type": "emailAddressField",
                                "presentation_type": "text",
                                "question": "Email address",
                            },
                            {
                                "field_id": "cmzQzX",
                                "form_name": "nwp-shared-applicant-information",
                                "field_type": "telephoneNumberField",
                                "presentation_type": "text",
                                "question": "Telephone number",
                            },
                            {
                                "field_id": "NuvvyU",
                                "form_name": "nwp-shared-applicant-information",
                                "field_type": "multilineTextField",
                                "presentation_type": "text",
                                "question": "A summary of the lead officer's experience and qualifications.",
                            },
                            {
                                "field_id": "rsiytx",
                                "form_name": "nwp-shared-applicant-information",
                                "field_type": "radiosField",
                                "presentation_type": "text",
                                "question": "<br>Is the primary contact the same as the accountable officer or the lead officer?",
                            },
                            {
                                "field_id": "GEyQSq",
                                "form_name": "nwp-shared-applicant-information",
                                "field_type": "textField",
                                "presentation_type": "text",
                                "question": "<h3>Who is the primary contact?</h3>Full name",
                            },
                            {
                                "field_id": "Owsgne",
                                "form_name": "nwp-shared-applicant-information",
                                "field_type": "textField",
                                "presentation_type": "text",
                                "question": "Role",
                            },
                            {
                                "field_id": "WOWWfM",
                                "form_name": "nwp-shared-applicant-information",
                                "field_type": "emailAddressField",
                                "presentation_type": "text",
                                "question": "Email address",
                            },
                            {
                                "field_id": "oExeYu",
                                "form_name": "nwp-shared-applicant-information",
                                "field_type": "telephoneNumberField",
                                "presentation_type": "text",
                                "question": "Telephone number",
                            },
                            {
                                "field_id": "gXiZBO",
                                "form_name": "nwp-shared-applicant-information",
                                "field_type": "yesNoField",
                                "presentation_type": "text",
                                "question": "<h3>Consortium information</h3>Is this application on behalf of a consortium?",
                            },
                            {
                                "field_id": "ZyAQSl",
                                "form_name": "nwp-shared-applicant-information",
                                "field_type": "multiInputField",
                                "presentation_type": "table",
                                "question": [
                                    "",
                                    {
                                        "kmYykb": {
                                            "column_title": "Consortium name",
                                            "type": "textField",
                                        },
                                        "GoeFfx": {
                                            "column_title": "Organisation's Roles",
                                            "type": "textField",
                                        },
                                        "EDVRRq": {
                                            "column_title": "Roles and responsibilities",
                                            "type": "textField",
                                        },
                                        "IUOJJs": {
                                            "column_title": "Lead organisation?",
                                            "type": "textField",
                                        },
                                    },
                                ],
                            },
                            {
                                "field_id": "lBebsG",
                                "form_name": "nwp-shared-applicant-information",
                                "field_type": "multilineTextField",
                                "presentation_type": "text",
                                "question": "How will this consortium generate efficiencies?",
                            },
                        ],
                    }
                ],
            },
            {
                "id": "stakeholders",
                "name": "Stakeholders",
                "themes": [
                    {
                        "id": "stakeholders",
                        "name": "Stakeholders",
                        "answers": [
                            {
                                "field_id": "ZAcTIF",
                                "form_name": "nwp-shared-stakeholders",
                                "field_type": "multilineTextField",
                                "presentation_type": "text",
                                "question": "Who are your main stakeholders?",
                            },
                            {
                                "field_id": "vkQCZO",
                                "form_name": "nwp-shared-stakeholders",
                                "field_type": "multilineTextField",
                                "presentation_type": "text",
                                "question": "What are you expecting stakeholders to contribute to this project?",
                            },
                            {
                                "field_id": "OUbunU",
                                "form_name": "nwp-shared-stakeholders",
                                "field_type": "multilineTextField",
                                "presentation_type": "text",
                                "question": "How will you engage with stakeholders?",
                            },
                            {
                                "field_id": "SVGlsX",
                                "form_name": "nwp-shared-stakeholders",
                                "field_type": "multilineTextField",
                                "presentation_type": "text",
                                "question": "What outcomes are you expecting?",
                            },
                        ],
                    }
                ],
            },
            {
                "id": "risks",
                "name": "Risks",
                "themes": [
                    {
                        "id": "risks",
                        "name": "Risks",
                        "answers": [
                            {
                                "field_id": "WTDdef",
                                "form_name": "nwp-shared-risks",
                                "field_type": "multiInputField",
                                "presentation_type": "table",
                                "question": [
                                    "Tell us about any risks to the proposal and how you plan to mitigate them.",
                                    {
                                        "YBPRlE": {
                                            "column_title": "Risk",
                                            "type": "textField",
                                        },
                                        "xOCujb": {
                                            "column_title": "Mitigation",
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
                "id": "declaration",
                "name": "Declaration",
                "themes": [
                    {
                        "id": "declaration",
                        "name": "Declaration",
                        "answers": [
                            {
                                "field_id": "MRbDfT",
                                "form_name": "nwp-shared-declaration",
                                "field_type": "checkboxesField",
                                "presentation_type": "text",
                                "question": "<h3>Declaration</h3>",
                            }
                        ],
                    }
                ],
            },
        ],
    },
]
