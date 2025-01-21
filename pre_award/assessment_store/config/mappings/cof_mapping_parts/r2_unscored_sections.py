# ruff: noqa: E501

unscored_sections = [
    {
        "id": "unscored",
        "name": "Unscored",
        "sub_criteria": [
            {
                "id": "org_info",
                "name": "Organisation information",
                "themes": [
                    {
                        "id": "general_info",
                        "name": "General information",
                        "answers": [
                            {
                                "field_id": "WWWWxy",
                                "form_name": "organisation-information",
                                "field_type": "textField",
                                "presentation_type": "text",
                                "question": "Your unique tracker number",
                            },
                            {
                                "field_id": "YdtlQZ",
                                "form_name": "organisation-information",
                                "field_type": "textField",
                                "presentation_type": "text",
                                "question": "Organisation name",
                            },
                            {
                                "field_id": "iBCGxY",
                                "form_name": "organisation-information",
                                "field_type": "yesNoField",
                                "presentation_type": "text",
                                "question": "Does your organisation use any other names",
                            },
                            {
                                "field_id": ["PHFkCs", "QgNhXX", "XCcqae"],
                                "form_name": "organisation-information",
                                "field_type": "textField",
                                "presentation_type": "grouped_fields",
                                "question": [
                                    "Alternative names of your organisation",
                                    "Alternative names of your organisation",
                                ],
                            },
                            {
                                "field_id": ["lajFtB", "plmwJv"],
                                "form_name": "organisation-information",
                                "field_type": "radiosField",
                                "presentation_type": "grouped_fields",
                                "question": [
                                    "Type of organisation",
                                    "Type of organisation",
                                ],
                            },
                            {
                                "field_id": "GlPmCX",
                                "form_name": "organisation-information",
                                "field_type": "textField",
                                "presentation_type": "text",
                                "question": "Company registration number",
                            },
                            {
                                "field_id": ["GvPSna", "zsbmRx"],
                                "form_name": "organisation-information",
                                "field_type": "radiosField",
                                "presentation_type": "grouped_fields",
                                "question": [
                                    "Which regulatory body is your company registered with?",
                                    "Which regulatory body is your company registered with?",
                                ],
                            },
                            {
                                "field_id": "aHIGbK",
                                "form_name": "organisation-information",
                                "field_type": "textField",
                                "presentation_type": "text",
                                "question": "Charity number",
                            },
                            {
                                "field_id": "DwfHtk",
                                "form_name": "organisation-information",
                                "field_type": "yesNoField",
                                "presentation_type": "text",
                                "question": "Is your organisation a trading subsidiary of a parent company?",
                            },
                            {
                                "field_id": "MPNlZx",
                                "form_name": "organisation-information",
                                "field_type": "textField",
                                "presentation_type": "text",
                                "question": "Name of parent organisation",
                            },
                            {
                                "field_id": "MyiYMw",
                                "form_name": "organisation-information",
                                "field_type": "datePartsField",
                                "presentation_type": "text",
                                "question": "Date parent organisation was established",
                            },
                            {
                                "field_id": "ZQolYb",
                                "form_name": "organisation-information",
                                "field_type": "ukAddressField",
                                "presentation_type": "address",
                                "question": "Organisation address",
                            },
                            {
                                "field_id": "zsoLdf",
                                "form_name": "organisation-information",
                                "field_type": "yesNoField",
                                "presentation_type": "text",
                                "question": "Is your correspondence address different to the organisation address?",
                            },
                            {
                                "field_id": "VhkCbM",
                                "form_name": "organisation-information",
                                "field_type": "ukAddressField",
                                "presentation_type": "address",
                                "question": "Correspondence address",
                            },
                            {
                                "field_id": ["FhbaEy", "FcdKlB", "BzxgDA"],
                                "form_name": "organisation-information",
                                "field_type": "websiteField",
                                "presentation_type": "grouped_fields",
                                "question": [
                                    "Website and social media",
                                    "Website and social media",
                                ],
                            },
                        ],
                    },
                    {
                        "id": "activities",
                        "name": "Activities",
                        "answers": [
                            {
                                "field_id": "emVGxS",
                                "form_name": "organisation-information",
                                "field_type": "multilineTextField",
                                "presentation_type": "list",
                                "question": "What is your organisation's main purpose?",
                            },
                            {
                                "field_id": ["btTtIb", "SkocDi", "CNeeiC"],
                                "form_name": "organisation-information",
                                "field_type": "multilineTextField",
                                "presentation_type": "grouped_fields",
                                "question": [
                                    "Tell us about your organisation's main activities",
                                    "Tell us about your organisation's main activities",
                                ],
                            },
                        ],
                    },
                    {
                        "id": "partnerships",
                        "name": "Partnerships",
                        "answers": [
                            {
                                "field_id": "hnLurH",
                                "form_name": "organisation-information",
                                "field_type": "yesNoField",
                                "presentation_type": "text",
                                "question": "Is your application a joint bid in partnership with other organisations?",
                            },
                            {
                                "field_id": "APSjeB",
                                "form_name": "organisation-information",
                                "field_type": "textField",
                                "presentation_type": "text",
                                "question": "Partner organisation name",
                            },
                            {
                                "field_id": "biTJjF",
                                "form_name": "organisation-information",
                                "field_type": "ukAddressField",
                                "presentation_type": "address",
                                "question": "Partner organisation address",
                            },
                            {
                                "field_id": "IkmvEt",
                                "form_name": "organisation-information",
                                "field_type": "multilineTextField",
                                "presentation_type": "list",
                                "question": "Tell us about your partnership and how you plan to work together",
                            },
                        ],
                    },
                ],
            },
            {
                "id": "applicant_info",
                "name": "Applicant information",
                "themes": [
                    {
                        "id": "contact_information",
                        "name": "Contact information",
                        "answers": [
                            {
                                "field_id": "ZBjDTn",
                                "form_name": "applicant-information",
                                "field_type": "textField",
                                "presentation_type": "text",
                                "question": "Name of lead contact",
                            },
                            {
                                "field_id": "LZBrEj",
                                "form_name": "applicant-information",
                                "field_type": "emailAddressField",
                                "presentation_type": "text",
                                "question": "Lead contact email address",
                            },
                            {
                                "field_id": "lRfhGB",
                                "form_name": "applicant-information",
                                "field_type": "telephoneNumberField",
                                "presentation_type": "text",
                                "question": "Lead contact telephone number",
                            },
                        ],
                    },
                ],
            },
            {
                "id": "project_info",
                "name": "Project information",
                "themes": [
                    {
                        "id": "previous_funding",
                        "name": "Previous funding",
                        "answers": [
                            {
                                "field_id": "gScdbf",
                                "form_name": "project-information",
                                "field_type": "yesNoField",
                                "presentation_type": "text",
                                "question": "Have you been given funding through the Community Ownership Fund before?",
                            },
                            {
                                "field_id": "IrIYcA",
                                "form_name": "project-information",
                                "field_type": "multilineTextField",
                                "presentation_type": "list",
                                "question": "Describe your previous project",
                            },
                            {
                                "field_id": "TFdnGq",
                                "form_name": "project-information",
                                "field_type": "numberField",
                                "presentation_type": "text",
                                "question": "Amount of funding received",
                            },
                        ],
                    },
                    {
                        "id": "project_summary",
                        "name": "Project summary",
                        "answers": [
                            {
                                "field_id": "KAgrBz",
                                "form_name": "project-information",
                                "field_type": "textField",
                                "presentation_type": "text",
                                "question": "Project name",
                            },
                            {
                                "field_id": "GCjCse",
                                "form_name": "project-information",
                                "field_type": "multilineTextField",
                                "presentation_type": "list",
                                "question": "Give a brief summary of your project, including what you hope to achieve",
                            },
                        ],
                    },
                ],
            },
            {
                "id": "asset_info",
                "name": "Asset information",
                "themes": [
                    {
                        "id": "asset_ownership",
                        "name": "Asset ownership",
                        "answers": [
                            {
                                "field_id": "VWkLlk",
                                "form_name": "asset-information",
                                "field_type": "radiosField",
                                "presentation_type": "text",
                                "question": "What do you intend to do with the asset?",
                            },
                            {
                                "field_id": "IRfSZp",
                                "form_name": "asset-information",
                                "field_type": "yesNoField",
                                "presentation_type": "text",
                                "question": "Do you know who currently owns your asset?",
                            },
                            {
                                "field_id": "ymlmrX",
                                "form_name": "asset-information",
                                "field_type": "textField",
                                "presentation_type": "text",
                                "question": "Name of current asset owner",
                            },
                            {
                                "field_id": "FtDJfK",
                                "form_name": "asset-information",
                                "field_type": "textField",
                                "presentation_type": "text",
                                "question": "Describe the current ownership status",
                            },
                            {
                                "field_id": "gkulUE",
                                "form_name": "asset-information",
                                "field_type": "yesNoField",
                                "presentation_type": "text",
                                "question": "Have you already completed the purchase or lease?",
                            },
                            {
                                "field_id": "uBXptf",
                                "form_name": "asset-information",
                                "field_type": "multilineTextField",
                                "presentation_type": "list",
                                "question": "Describe the sale process, e.g. an auction, or the terms of your lease if you have rented the asset",
                            },
                            {
                                "field_id": "nvMmGE",
                                "form_name": "asset-information",
                                "field_type": "multilineTextField",
                                "presentation_type": "list",
                                "question": "Describe the expected sale process, or the proposed terms of your lease if you are renting the asset",
                            },
                            {
                                "field_id": "ghzLRv",
                                "form_name": "asset-information",
                                "field_type": "datePartsField",
                                "presentation_type": "text",
                                "question": "Expected date of sale or lease",
                            },
                            {
                                "field_id": "Wyesgy",
                                "form_name": "asset-information",
                                "field_type": "yesNoField",
                                "presentation_type": "text",
                                "question": "Is your asset currently publicly owned?",
                            },
                            {
                                "field_id": "fHvilU",
                                "form_name": "asset-information",
                                "field_type": "textField",
                                "presentation_type": "text",
                                "question": "Name of contact",
                            },
                            {
                                "field_id": "scYeIU",
                                "form_name": "asset-information",
                                "field_type": "textField",
                                "presentation_type": "text",
                                "question": "Job title of contact",
                            },
                            {
                                "field_id": "ZHPwln",
                                "form_name": "asset-information",
                                "field_type": "textField",
                                "presentation_type": "text",
                                "question": "Organisation name",
                            },
                            {
                                "field_id": "nkPfyn",
                                "form_name": "asset-information",
                                "field_type": "checkboxesField",
                                "presentation_type": "list",
                                "question": "When you buy or lease a publicly owned asset, the public authority cannot transfer statutory services or duties to the community group",
                            },
                            {
                                "field_id": "PraPAq",
                                "form_name": "asset-information",
                                "field_type": "checkboxesField",
                                "presentation_type": "list",
                                "question": "Grants from this fund cannot be used to buy the freehold or premium on the lease of a publicly owned asset. Money must only be used for renovation and refurbishment costs",
                            },
                        ],
                    },
                    {
                        "id": "asset_evidence",
                        "name": "Asset evidence",
                        "answers": [
                            {
                                "field_id": "ArVrka",
                                "form_name": "asset-information",
                                "field_type": "fileUploadField",
                                "presentation_type": "file",
                                "question": "Supporting evidence",
                            }
                        ],
                    },
                    {
                        "id": "asset_background",
                        "name": "Asset background",
                        "answers": [
                            {
                                "field_id": ["yaQoxU", "GjzaqR"],
                                "form_name": "asset-information",
                                "field_type": "textField",
                                "presentation_type": "grouped_fields",
                                "question": ["Asset type", "Asset type"],
                            },
                            {
                                "field_id": "hvzzWB",
                                "form_name": "asset-information",
                                "field_type": "yesNoField",
                                "presentation_type": "text",
                                "question": "Is this a registered Asset of Community Value?",
                            },
                            {
                                "field_id": "MLwpjP",
                                "form_name": "asset-information",
                                "field_type": "yesNoField",
                                "presentation_type": "text",
                                "question": "Will you purchase the asset within the appropriate time frame?",
                            },
                            {
                                "field_id": "VwxiGn",
                                "form_name": "asset-information",
                                "field_type": "yesNoField",
                                "presentation_type": "text",
                                "question": "Is the asset listed for disposal, or part of a Community Asset Transfer?",
                            },
                            {
                                "field_id": "bkbGIE",
                                "form_name": "asset-information",
                                "field_type": "datePartsField",
                                "presentation_type": "text",
                                "question": "When was the asset listed?",
                            },
                            {
                                "field_id": "kBCjwC",
                                "form_name": "asset-information",
                                "field_type": "websiteField",
                                "presentation_type": "text",
                                "question": "Provide a link to the listing",
                            },
                            {
                                "field_id": "vKSMwi",
                                "form_name": "asset-information",
                                "field_type": "multilineTextField",
                                "presentation_type": "list",
                                "question": "Describe the current status of the Community Asset Transfer",
                            },
                        ],
                    },
                    {
                        "id": "asset_location",
                        "name": "Asset location",
                        "answers": [
                            {
                                "field_id": "yEmHpp",
                                "form_name": "project-information",
                                "field_type": "ukAddressField",
                                "presentation_type": "address",
                                "question": "Address of the community asset",
                            },
                            {
                                "field_id": "iTeLGU",
                                "form_name": "project-information",
                                "field_type": "textField",
                                "presentation_type": "text",
                                "question": "In which constituency is your asset?",
                            },
                            {
                                "field_id": "MGRlEi",
                                "form_name": "project-information",
                                "field_type": "textField",
                                "presentation_type": "text",
                                "question": "In which local council area is your asset?",
                            },
                        ],
                    },
                ],
            },
            {
                "id": "business_plan",
                "name": "Business plan",
                "themes": [
                    {
                        "id": "business_plan",
                        "name": "Business plan",
                        "answers": [
                            {
                                "field_id": "rFXeZo",
                                "form_name": "upload-business-plan",
                                "field_type": "fileUploadField",
                                "presentation_type": "file",
                                "question": "Business plan (document upload)",
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
                                "field_id": "LlvhYl",
                                "form_name": "declarations",
                                "field_type": "yesNoField",
                                "presentation_type": "text",
                                "question": "Confirm you have considered subsidy control and state aid implications for your project, and the information you have given us is correct",
                            },
                            {
                                "field_id": "wJrJWY",
                                "form_name": "declarations",
                                "field_type": "yesNoField",
                                "presentation_type": "text",
                                "question": "Confirm you have considered people with protected characteristics throughout the planning of your project",
                            },
                            {
                                "field_id": "COiwQr",
                                "form_name": "declarations",
                                "field_type": "yesNoField",
                                "presentation_type": "text",
                                "question": "Confirm you have considered sustainability and the environment throughout the planning of your project, including compliance with the government's Net Zero ambitions",
                            },
                            {
                                "field_id": "bRPzWU",
                                "form_name": "declarations",
                                "field_type": "yesNoField",
                                "presentation_type": "text",
                                "question": "Confirm you have a bank account set up and associated with the organisation you are applying on behalf of",
                            },
                        ],
                    }
                ],
            },
            {
                "id": "subsidy_control_and_state_aid",
                "name": "Subsidy control and state aid",
                "themes": [
                    {
                        "id": "project_qualification",
                        "name": "Project qualification",
                        "answers": [
                            {
                                "field_id": "HvxXPI",
                                "form_name": "project-qualification",
                                "field_type": "yesNoField",
                                "presentation_type": "text",
                                "question": "Does your project meet the definition of a subsidy?",
                            },
                            {
                                "field_id": "RmMKzM",
                                "form_name": "project-qualification",
                                "field_type": "multilineTextField",
                                "presentation_type": "list",
                                "question": "Explain how you think a grant from this fund can be provided in compliance with the Subsidy Control Act (2022)",
                            },
                            {
                                "field_id": "UPmQrD",
                                "form_name": "project-qualification",
                                "field_type": "yesNoField",
                                "presentation_type": "text",
                                "question": "Is your project based in Northern Ireland?",
                            },
                            {
                                "field_id": "xPkdRX",
                                "form_name": "project-qualification",
                                "field_type": "multilineTextField",
                                "presentation_type": "list",
                                "question": "Explain how your project will comply with state aid rules",
                            },
                        ],
                    }
                ],
            },
        ],
    },
]
