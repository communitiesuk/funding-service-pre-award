# ruff: noqa: E501

unscored_sections = [
    {
        "id": "unscored",
        "name": "Unscored",
        "sub_criteria": [
            {
                "id": "about-your-organisation",
                "name": "About your organisation",
                "themes": [
                    {
                        "id": "organisation-name-and-address",
                        "name": "Organisation name and address",
                        "answers": [
                            {
                                "field_id": "JbmcJE",
                                "form_name": "about-your-organisation-cyp",
                                "field_type": "textField",
                                "presentation_type": "text",
                                "question": "Organisation name",
                            },
                            {
                                "field_id": "KUdOhN",
                                "form_name": "about-your-organisation-cyp",
                                "field_type": "yesNoField",
                                "presentation_type": "text",
                                "question": "Does your organisation use any other names?",
                            },
                            {
                                "field_id": "NcnYCn",
                                "form_name": "about-your-organisation-cyp",
                                "field_type": "textField",
                                "presentation_type": "text",
                                "question": "Alternative names of your organisation - Alternative name 1",
                            },
                            {
                                "field_id": "rtFyqT",
                                "form_name": "about-your-organisation-cyp",
                                "field_type": "textField",
                                "presentation_type": "text",
                                "question": "Alternative names of your organisation - Alternative name 2 (optional)",
                            },
                            {
                                "field_id": "DYUbGM",
                                "form_name": "about-your-organisation-cyp",
                                "field_type": "textField",
                                "presentation_type": "text",
                                "question": "Alternative names of your organisation - Alternative name 3 (optional)",
                            },
                            {
                                "field_id": "kxgOne",
                                "form_name": "about-your-organisation-cyp",
                                "field_type": "freeTextField",
                                "presentation_type": "free_text",
                                "question": "Tell us about your organisation's main activities - Activity 1",
                            },
                            {
                                "field_id": "kxgTwo",
                                "form_name": "about-your-organisation-cyp",
                                "field_type": "freeTextField",
                                "presentation_type": "free_text",
                                "question": "Tell us about your organisation's main activities - Activity 2 (optional)",
                            },
                            {
                                "field_id": "kxgThr",
                                "form_name": "about-your-organisation-cyp",
                                "field_type": "freeTextField",
                                "presentation_type": "free_text",
                                "question": "Tell us about your organisation's main activities - Activity 3 (optional)",
                            },
                            {
                                "field_id": "rmBPvK",
                                "form_name": "about-your-organisation-cyp",
                                "field_type": "ukAddressField",
                                "presentation_type": "address",
                                "question": "Registered organisation address",
                            },
                            {
                                "field_id": "smBPvK",
                                "form_name": "about-your-organisation-cyp",
                                "field_type": "ukAddressField",
                                "presentation_type": "address",
                                "question": "Alternative organisation address (optional)",
                            },
                            {
                                "field_id": "tYoOqx",
                                "form_name": "about-your-organisation-cyp",
                                "field_type": "multiInputField",
                                "presentation_type": "table",
                                "question": [
                                    "Website and social media",
                                    {
                                        "EShKlA": {
                                            "column_title": "Link",
                                            "type": "WebsiteField",
                                        },
                                    },
                                ],
                            },
                        ],
                    },
                    {
                        "id": "organisation-classification",
                        "name": "Organisation classification",
                        "answers": [
                            {
                                "field_id": "jcmcJE",
                                "form_name": "about-your-organisation-cyp",
                                "field_type": "radiosField",
                                "presentation_type": "text",
                                "question": "How is your organisation classified?",
                            },
                            {
                                "field_id": "jemcJE",
                                "form_name": "about-your-organisation-cyp",
                                "field_type": "textField",
                                "presentation_type": "text",
                                "question": "How is your organisation classified? (other)",
                            },
                            {
                                "field_id": "jencJE",
                                "form_name": "about-your-organisation-cyp",
                                "field_type": "textField",
                                "presentation_type": "text",
                                "question": "Company registration number (optional)",
                            },
                            {
                                "field_id": "jeocJE",
                                "form_name": "about-your-organisation-cyp",
                                "field_type": "textField",
                                "presentation_type": "text",
                                "question": "Charity number",
                            },
                        ],
                    },
                    {
                        "id": "partner-organisation",
                        "name": "Partner organisation",
                        "answers": [
                            {
                                "field_id": "MRdGKt",
                                "form_name": "about-your-organisation-cyp",
                                "field_type": "yesNoField",
                                "presentation_type": "text",
                                "question": "Is your application a joint bid in partnership with other organisations?",
                            },
                            {
                                "field_id": "tZoOKx",
                                "form_name": "about-your-organisation-cyp",
                                "field_type": "multiInputField",
                                "presentation_type": "table",
                                "question": [
                                    "Partner organisation details",
                                    {
                                        "GpLJDu": {
                                            "column_title": "Partner organisation name",
                                            "type": "textField",
                                        },
                                        "IXjMWp": {
                                            "column_title": "Partner organisation address",
                                            "type": "ukAddressField",
                                        },
                                        "MKbOlA": {
                                            "column_title": "Website and social media link 1",
                                            "type": "websiteField",
                                        },
                                        "OghGGr": {
                                            "column_title": "Website and social media link 2 (optional)",
                                            "type": "websiteField",
                                        },
                                        "RphKTp": {
                                            "column_title": "Website and social media link 3 (optional)",
                                            "type": "websiteField",
                                        },
                                    },
                                ],
                            },
                            {
                                "field_id": "xPcbJX",
                                "form_name": "about-your-organisation-cyp",
                                "field_type": "freeTextField",
                                "presentation_type": "free_text",
                                "question": "Tell us about how you plan to work with the partner organisations",
                            },
                            {
                                "field_id": "RUdOhN",
                                "form_name": "about-your-organisation-cyp",
                                "field_type": "yesNoField",
                                "presentation_type": "text",
                                "question": "Does an agreement currently exist between your organisation and the partnership organisations?",
                            },
                        ],
                    },
                ],
            },
            {
                "id": "applicant-information",
                "name": "Applicant information",
                "themes": [
                    {
                        "id": "applicant-information",
                        "name": "Applicant information",
                        "answers": [
                            {
                                "field_id": "rKHBnt",
                                "form_name": "applicant-information-cyp",
                                "field_type": "textField",
                                "presentation_type": "text",
                                "question": "Name of lead contact",
                            },
                            {
                                "field_id": "yWtfkb",
                                "form_name": "applicant-information-cyp",
                                "field_type": "textField",
                                "presentation_type": "text",
                                "question": "Alternative name (optional)",
                            },
                            {
                                "field_id": "kbOHaM",
                                "form_name": "applicant-information-cyp",
                                "field_type": "textField",
                                "presentation_type": "text",
                                "question": "Lead contact job title",
                            },
                            {
                                "field_id": "BKOHaM",
                                "form_name": "applicant-information-cyp",
                                "field_type": "textField",
                                "presentation_type": "text",
                                "question": "Lead contact email address",
                            },
                            {
                                "field_id": "CyANDT",
                                "form_name": "applicant-information-cyp",
                                "field_type": "textField",
                                "presentation_type": "text",
                                "question": "Lead contact telephone number",
                            },
                            {
                                "field_id": "DbFHbD",
                                "form_name": "applicant-information-cyp",
                                "field_type": "yesNoField",
                                "presentation_type": "text",
                                "question": "Is the lead contact the same person as the authorised signatory?",
                            },
                            {
                                "field_id": "pDrPDz",
                                "form_name": "applicant-information-cyp",
                                "field_type": "textField",
                                "presentation_type": "text",
                                "question": "Authorised signatory full name",
                            },
                            {
                                "field_id": "teowxM",
                                "form_name": "applicant-information-cyp",
                                "field_type": "textField",
                                "presentation_type": "text",
                                "question": "Alternative name (optional)",
                            },
                            {
                                "field_id": "tikwxM",
                                "form_name": "applicant-information-cyp",
                                "field_type": "textField",
                                "presentation_type": "text",
                                "question": "Authorised signatory job title",
                            },
                            {
                                "field_id": "ljfzCy",
                                "form_name": "applicant-information-cyp",
                                "field_type": "textField",
                                "presentation_type": "text",
                                "question": "Authorised signatory email address",
                            },
                            {
                                "field_id": "gNgJme",
                                "form_name": "applicant-information-cyp",
                                "field_type": "textField",
                                "presentation_type": "text",
                                "question": "Authorised signatory telephone number",
                            },
                        ],
                    },
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
                                "field_id": "sdeLyR",
                                "form_name": "declarations-cyp",
                                "field_type": "yesNoField",
                                "presentation_type": "text",
                                "question": "Confirm your organisation adheres to the government code of conduct",
                            },
                            {
                                "field_id": "SUTxtj",
                                "form_name": "declarations-cyp",
                                "field_type": "yesNoField",
                                "presentation_type": "text",
                                "question": "Confirm your organisation has a data handling process in place",
                            },
                            {
                                "field_id": "WWHYDI",
                                "form_name": "declarations-cyp",
                                "field_type": "yesNoField",
                                "presentation_type": "text",
                                "question": "Confirm you have a bank account set up and associated with the organisation you are applying on behalf of",
                            },
                            {
                                "field_id": "WGmcyu",
                                "form_name": "declarations-cyp",
                                "field_type": "yesNoField",
                                "presentation_type": "text",
                                "question": "Confirm that your organisation's safegaurding policies are up to date",
                            },
                            {
                                "field_id": "WGmDZu",
                                "form_name": "declarations-cyp",
                                "field_type": "yesNoField",
                                "presentation_type": "text",
                                "question": "Confirm that the information you've provided in this application is accurate to the best of your knowledge on the date of submission",
                            },
                        ],
                    },
                ],
            },
        ],
    },
]
