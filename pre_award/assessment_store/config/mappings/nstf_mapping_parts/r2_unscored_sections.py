# ruff: noqa: E501

unscored_sections = [
    {
        "id": "your_organisation",
        "name": "Your organisation",
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
                                "field_id": "opFJRm",
                                "form_name": "organisation-information-ns",
                                "field_type": "textField",
                                "presentation_type": "text",
                                "question": "Organisation name",
                            },
                            {
                                "field_id": "mhYQzL",
                                "form_name": "organisation-information-ns",
                                "field_type": "ukAddressField",
                                "presentation_type": "address",
                                "question": "Organisation address",
                            },
                            {
                                "field_id": "AVShTf",
                                "form_name": "organisation-information-ns",
                                "field_type": "textField",
                                "presentation_type": "text",
                                "question": "Which region of England do you work in?",
                            },
                            {
                                "field_id": "BwbIlM",
                                "form_name": "organisation-information-ns",
                                "field_type": "freeTextField",
                                "presentation_type": "free_text",
                                "question": "What is your organisation's main purpose?",
                            },
                            {
                                "field_id": "RxbebZ",
                                "form_name": "organisation-information-ns",
                                "field_type": "freeTextField",
                                "presentation_type": "free_text",
                                "question": "What are your organisation's charitable objects?",
                            },
                            {
                                "field_id": "YauUjZ",
                                "form_name": "organisation-information-ns",
                                "field_type": "numberField",
                                "presentation_type": "currency",
                                "question": "What is your organisation's annual turnover? "
                                "(1 April 2022 to 31 March 2023)",
                            },
                            {
                                "field_id": "zuCRBk",
                                "form_name": "organisation-information-ns",
                                "field_type": "numberField",
                                "presentation_type": "currency",
                                "question": "What is your organisation's annual turnover? "
                                "(1 April 2021 to 31 March 2022)",
                            },
                            {
                                "field_id": "NENGMj",
                                "form_name": "organisation-information-ns",
                                "field_type": "radiosField",
                                "presentation_type": "text",
                                "question": "Which membership organisations are you a member of?",
                            },
                        ],
                    }
                ],
            },
            {
                "id": "organiation_type",
                "name": "Organisation type",
                "themes": [
                    {
                        "id": "organisation-type",
                        "name": "Organisation type",
                        "answers": [
                            {
                                "field_id": "ChXWIQ",
                                "form_name": "organisation-type-ns",
                                "field_type": "checkboxesField",
                                "presentation_type": "list",
                                "question": "How is your organisation classified?",
                            },
                            {
                                "field_id": "ETJaFn",
                                "form_name": "organisation-type-ns",
                                "field_type": "textField",
                                "presentation_type": "text",
                                "question": "If None of these - How is your organisation classified?",
                            },
                            {
                                "field_id": "GnjTGi",
                                "form_name": "organisation-type-ns",
                                "field_type": "numberField",
                                "presentation_type": "text",
                                "question": "Charity number (optional)",
                            },
                            {
                                "field_id": "vtOZNq",
                                "form_name": "organisation-type-ns",
                                "field_type": "numberField",
                                "presentation_type": "text",
                                "question": "Company registration number (optional)",
                            },
                            {
                                "field_id": "ILVEOG",
                                "form_name": "organisation-type-ns",
                                "field_type": "multiInputField",
                                "presentation_type": "table",
                                "question": [
                                    "Names of trustees or committee members",
                                    {
                                        "mrCotx": {
                                            "column_title": "Full name",
                                            "type": "textField",
                                        },
                                    },
                                ],
                            },
                            {
                                "field_id": "TgBzyM",
                                "form_name": "organisation-type-ns",
                                "field_type": "radiosField",
                                "presentation_type": "text",
                                "question": "How long has your organisation been operating?",
                            },
                            {
                                "field_id": "ZMgdzY",
                                "form_name": "organisation-type-ns",
                                "field_type": "clientSideFileUploadField",
                                "presentation_type": "s3bucketPath",
                                "question": "Upload your organisation's annual accounts from the last 3 years",
                                "path": "upload-your-organisations-annual-accounts-from-the-last-3-years",
                            },
                            {
                                "field_id": "sVlFcN",
                                "form_name": "organisation-type-ns",
                                "field_type": "clientSideFileUploadField",
                                "presentation_type": "s3bucketPath",
                                "question": "Upload your organisation's annual accounts that you have available",
                                "path": "upload-your-organisations-annual-accounts-that-you-have-available",
                            },
                            {
                                "field_id": "OrWSBk",
                                "form_name": "organisation-type-ns",
                                "field_type": "clientSideFileUploadField",
                                "presentation_type": "s3bucketPath",
                                "question": "Upload a current bank statement which is less than 2 months old",
                                "path": "upload-a-current-bank-statement-which-is-less-than-2-months-old",
                            },
                            {
                                "field_id": "bgHVXX",
                                "form_name": "organisation-type-ns",
                                "field_type": "clientSideFileUploadField",
                                "presentation_type": "s3bucketPath",
                                "question": "Upload an annual budget for your organisation",
                                "path": "upload-an-annual-budget-for-your-organisation",
                            },
                        ],
                    }
                ],
            },
            {
                "id": "application_information",
                "name": "Applicant information",
                "themes": [
                    {
                        "id": "application_information",
                        "name": "Applicant information",
                        "answers": [
                            {
                                "field_id": "fUMWcd",
                                "form_name": "applicant-information-ns",
                                "field_type": "textField",
                                "presentation_type": "text",
                                "question": "Name of lead contact",
                            },
                            {
                                "field_id": "lZVkeg",
                                "form_name": "applicant-information-ns",
                                "field_type": "textField",
                                "presentation_type": "text",
                                "question": "Lead contact job title",
                            },
                            {
                                "field_id": "CDEwxp",
                                "form_name": "applicant-information-ns",
                                "field_type": "emailAddressField",
                                "presentation_type": "text",
                                "question": "Lead contact email address",
                            },
                            {
                                "field_id": "DvBqCJ",
                                "form_name": "applicant-information-ns",
                                "field_type": "telephoneNumberField",
                                "presentation_type": "text",
                                "question": "Lead contact telephone number",
                            },
                            {
                                "field_id": "ayzqnK",
                                "form_name": "applicant-information-ns",
                                "field_type": "yesNoField",
                                "presentation_type": "text",
                                "question": "Is the lead contact the same person as the authorised signatory?",
                            },
                            {
                                "field_id": "tfgPej",
                                "form_name": "applicant-information-ns",
                                "field_type": "textField",
                                "presentation_type": "text",
                                "question": "Authorised signatory full name",
                            },
                            {
                                "field_id": "RDsTKl",
                                "form_name": "applicant-information-ns",
                                "field_type": "textField",
                                "presentation_type": "text",
                                "question": "Authorised signatory job title",
                            },
                            {
                                "field_id": "OnijFx",
                                "form_name": "applicant-information-ns",
                                "field_type": "emailAddressField",
                                "presentation_type": "text",
                                "question": "Authorised signatory email address",
                            },
                            {
                                "field_id": "gJlzFS",
                                "form_name": "applicant-information-ns",
                                "field_type": "telephoneNumberField",
                                "presentation_type": "text",
                                "question": "Authorised signatory telephone number",
                            },
                        ],
                    }
                ],
            },
            {
                "id": "joint_applications",
                "name": "Joint applications",
                "themes": [
                    {
                        "id": "joint_applications",
                        "name": "Joint applications",
                        "answers": [
                            {
                                "field_id": "jsUbAI",
                                "form_name": "joint-applications-ns",
                                "field_type": "yesNoField",
                                "presentation_type": "text",
                                "question": "Is your application a joint bid in partnership with other organisations?",
                            },
                            {
                                "field_id": "oxMLrb",
                                "form_name": "joint-applications-ns",
                                "field_type": "multiInputField",
                                "presentation_type": "table",
                                "question": [
                                    "Partner organisation details",
                                    {
                                        "EFlBMr": {
                                            "column_title": "Partner organisation name",
                                            "type": "textField",
                                        },
                                        "JFEJVf": {
                                            "column_title": "Tell us about your partnership and how you plan to work together",
                                            "type": "multilineTextField",
                                        },
                                    },
                                ],
                            },
                        ],
                    }
                ],
            },
        ],
    },
    {
        "id": "declarations",
        "name": "Declarations",
        "sub_criteria": [
            {
                "id": "declarations",
                "name": "Declarations",
                "themes": [
                    {
                        "id": "declarations",
                        "name": "Declarations",
                        "answers": [
                            {
                                "field_id": "kOTdzu",
                                "form_name": "declarations-ns",
                                "field_type": "yesNoField",
                                "presentation_type": "text",
                                "question": "Confirm you have a bank account set up and associated with the organisation you are applying on behalf of",
                            },
                            {
                                "field_id": "NBcyAe",
                                "form_name": "declarations-ns",
                                "field_type": "yesNoField",
                                "presentation_type": "text",
                                "question": "Confirm that the information you've provided in this application is accurate to the best of your knowledge on the date of submission",
                            },
                            {
                                "field_id": "OKtDsH",
                                "form_name": "declarations-ns",
                                "field_type": "yesNoField",
                                "presentation_type": "text",
                                "question": "Confirm you have a safeguarding, data protection and health and safety policy",
                            },
                        ],
                    }
                ],
            }
        ],
    },
]
