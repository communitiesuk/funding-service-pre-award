# ruff: noqa: E501

from string import Template

application_store_json_template = Template(
    """
    {
    "account_id": "cbf981cf-5238-4d3e-84e9-b9c183789a91",
    "date_submitted": "2022-10-27T08:32:13.383999",
    "forms": [
        {
            "name": "feasibility",
            "questions": [
                {
                    "fields": [
                        {
                            "answer": "Tell us about the feasibility studies you have carried out for your project",
                            "key": "ieRCkI",
                            "title": "Tell us about the feasibility studies you have carried out for your project",
                            "type": "text"
                        },
                        {
                            "answer": false,
                            "key": "aAeszH",
                            "title": "Do you need to do any further feasibility work?",
                            "type": "list"
                        }
                    ],
                    "question": "Management case",
                    "status": "COMPLETED"
                }
            ],
            "status": "COMPLETED"
        },
        {
            "name": "risk",
            "questions": [
                {
                    "fields": [
                        {
                            "answer": "sample1.doc",
                            "key": "ozgwXq",
                            "title": "Risks to your project (document upload)",
                            "type": "file"
                        }
                    ],
                    "question": "Management case",
                    "status": "COMPLETED"
                }
            ],
            "status": "COMPLETED"
        },
        {
            "name": "community-use",
            "questions": [
                {
                    "fields": [
                        {
                            "answer": [
                                "support-local-community"
                            ],
                            "key": "CDwTrG",
                            "title": "What policy aims will your project deliver against?",
                            "type": "list"
                        },
                        {
                            "answer": "Test",
                            "key": "kxgWTy",
                            "title": "Who in the community uses the asset, or has used it in the past, and who benefits from it?",
                            "type": "text"
                        },
                        {
                            "answer": "Test",
                            "key": "GNhrIs",
                            "title": "Tell us how losing the asset would affect, or has already affected, people in the community",
                            "type": "text"
                        },
                        {
                            "answer": "Test",
                            "key": "qsZLjZ",
                            "title": "Why will the asset be lost without community intervention?",
                            "type": "text"
                        }
                    ],
                    "question": "Strategic case",
                    "status": "COMPLETED"
                }
            ],
            "status": "COMPLETED"
        },
        {
            "name": "environmental-sustainability",
            "questions": [
                {
                    "fields": [
                        {
                            "answer": "Test",
                            "key": "CvVZJv",
                            "title": "Tell us how you have considered the environmental sustainability of your project",
                            "type": "text"
                        }
                    ],
                    "question": "Strategic case",
                    "status": "COMPLETED"
                }
            ],
            "status": "COMPLETED"
        },
        {
            "name": "local-support",
            "questions": [
                {
                    "fields": [
                        {
                            "answer": false,
                            "key": "KqoaJL",
                            "title": "Are you confident there is local support for your project?",
                            "type": "list"
                        }
                    ],
                    "question": "Strategic case",
                    "status": "COMPLETED"
                }
            ],
            "status": "COMPLETED"
        },
        {
            "name": "project-qualification",
            "questions": [
                {
                    "fields": [
                        {
                            "answer": false,
                            "key": "HvxXPI",
                            "title": "Does your project meet the definition of a subsidy?",
                            "type": "list"
                        }
                    ],
                    "question": "Subsidy control and state aid",
                    "status": "COMPLETED"
                }
            ],
            "status": "COMPLETED"
        },
        {
            "name": "skills-and-resources",
            "questions": [
                {
                    "fields": [
                        {
                            "answer": false,
                            "key": "CBIWnt",
                            "title": "Do you have experience of managing a community asset?",
                            "type": "list"
                        }
                    ],
                    "question": "Management case",
                    "status": "COMPLETED"
                },
                {
                    "fields": [
                        {
                            "answer": false,
                            "key": "vKnMPG",
                            "title": "Do you have any plans to recruit people to help you manage the asset?",
                            "type": "list"
                        }
                    ],
                    "question": "Management case",
                    "status": "COMPLETED"
                }
            ],
            "status": "COMPLETED"
        },
        {
            "name": "upload-business-plan",
            "questions": [
                {
                    "fields": [
                        {
                            "answer": "sample1.doc",
                            "key": "rFXeZo",
                            "title": "Upload business plan",
                            "type": "file"
                        }
                    ],
                    "question": "Management case",
                    "status": "COMPLETED"
                }
            ],
            "status": "COMPLETED"
        },
        {
            "name": "project-information",
            "questions": [
                {
                    "fields": [
                        {
                            "answer": false,
                            "key": "gScdbf",
                            "title": "Have you been given funding through the Community Ownership Fund before?",
                            "type": "list"
                        }
                    ],
                    "question": "About your project",
                    "status": "COMPLETED"
                },
                {
                    "fields": [
                        {
                            "answer": "$project_name",
                            "key": "KAgrBz",
                            "title": "Project name",
                            "type": "text"
                        },
                        {
                            "answer": "Test",
                            "key": "wudRxx",
                            "title": "Tell us how the asset is currently being used, or how it has been used before, and why it's important to the community",
                            "type": "text"
                        },
                        {
                            "answer": "Test",
                            "key": "TlGjXb",
                            "title": "Explain why the asset is at risk of being lost to the community, or why it has already been lost",
                            "type": "text"
                        },
                        {
                            "answer": "Test",
                            "key": "GCjCse",
                            "title": "Give a brief summary of your project, including what you hope to achieve",
                            "type": "text"
                        }
                    ],
                    "question": "About your project",
                    "status": "COMPLETED"
                },
                {
                    "fields": [
                        {
                            "answer": "Test Address, null, Test Town Or City, null, $location_postcode",
                            "key": "yEmHpp",
                            "title": "Address of the community asset",
                            "type": "text"
                        },
                        {
                            "answer": "Constituency",
                            "key": "iTeLGU",
                            "title": "In which constituency is your asset?",
                            "type": "text"
                        },
                        {
                            "answer": "$local_authority",
                            "key": "MGRlEi",
                            "title": "In which local council area is your asset?",
                            "type": "text"
                        }
                    ],
                    "question": "About your project",
                    "status": "COMPLETED"
                }
            ],
            "status": "COMPLETED"
        },
        {
            "name": "organisation-information",
            "questions": [
                {
                    "fields": [
                        {
                            "answer": "ANON-###-###-###",
                            "key": "WWWWxy",
                            "title": "Your unique tracker number",
                            "type": "text"
                        },
                        {
                            "answer": "Test",
                            "key": "YdtlQZ",
                            "title": "Organisation name",
                            "type": "text"
                        },
                        {
                            "answer": false,
                            "key": "iBCGxY",
                            "title": "Does your organisation use any other names?",
                            "type": "list"
                        }
                    ],
                    "question": "About your organisation",
                    "status": "COMPLETED"
                },
                {
                    "fields": [
                        {
                            "answer": "Test",
                            "key": "emVGxS",
                            "title": "What is your organisation's main purpose?",
                            "type": "text"
                        },
                        {
                            "answer": "Test",
                            "key": "btTtIb",
                            "title": "Tell us about your organisation's main activities",
                            "type": "text"
                        },
                        {
                            "answer": null,
                            "key": "SkocDi",
                            "title": "Tell us about your organisation's main activities - Activity 2 ",
                            "type": "text"
                        },
                        {
                            "answer": null,
                            "key": "CNeeiC",
                            "title": "Tell us about your organisation's main activities - Activity 3 ",
                            "type": "text"
                        },
                        {
                            "answer": false,
                            "key": "BBlCko",
                            "title": "Have you delivered projects like this before?",
                            "type": "list"
                        }
                    ],
                    "question": "About your organisation",
                    "status": "COMPLETED"
                },
                {
                    "fields": [
                        {
                            "answer": "CIO",
                            "key": "lajFtB",
                            "title": "Type of organisation",
                            "type": "list"
                        }
                    ],
                    "question": "About your organisation",
                    "status": "COMPLETED"
                },
                {
                    "fields": [
                        {
                            "answer": "Test",
                            "key": "aHIGbK",
                            "title": "Charity number ",
                            "type": "text"
                        }
                    ],
                    "question": "About your organisation",
                    "status": "COMPLETED"
                },
                {
                    "fields": [
                        {
                            "answer": false,
                            "key": "DwfHtk",
                            "title": "Is your organisation a trading subsidiary of a parent company?",
                            "type": "list"
                        }
                    ],
                    "question": "About your organisation",
                    "status": "COMPLETED"
                },
                {
                    "fields": [
                        {
                            "answer": "Test Address, null, Test Town Or City, null, $location_postcode",
                            "key": "ZQolYb",
                            "title": "Organisation address",
                            "type": "text"
                        },
                        {
                            "answer": false,
                            "key": "zsoLdf",
                            "title": "Is your correspondence address different to the organisation address?",
                            "type": "list"
                        },
                        {
                            "answer": "https://twitter.com/luhc",
                            "key": "FhbaEy",
                            "title": "Website and social media ",
                            "type": "text"
                        },
                        {
                            "answer": null,
                            "key": "FcdKlB",
                            "title": "Website and social media - Link or username 2",
                            "type": "text"
                        },
                        {
                            "answer": null,
                            "key": "BzxgDA",
                            "title": "Website and social media - Link or username 3",
                            "type": "text"
                        }
                    ],
                    "question": "About your organisation",
                    "status": "COMPLETED"
                },
                {
                    "fields": [
                        {
                            "answer": false,
                            "key": "hnLurH",
                            "title": "Is your application a joint bid in partnership with other organisations?",
                            "type": "list"
                        }
                    ],
                    "question": "About your organisation",
                    "status": "COMPLETED"
                }
            ],
            "status": "COMPLETED"
        },
        {
            "name": "applicant-information",
            "questions": [
                {
                    "fields": [
                        {
                            "answer": "Test Name",
                            "key": "ZBjDTn",
                            "title": "Name of lead contact",
                            "type": "text"
                        },
                        {
                            "answer": "testemailfundingservice@testemailfundingservice.com",
                            "key": "LZBrEj",
                            "title": "Lead contact email address",
                            "type": "text"
                        },
                        {
                            "answer": "0000000000",
                            "key": "lRfhGB",
                            "title": "Lead contact telephone number",
                            "type": "text"
                        }
                    ],
                    "question": "About your organisation",
                    "status": "COMPLETED"
                }
            ],
            "status": "COMPLETED"
        },
        {
            "name": "asset-information",
            "questions": [
                {
                    "fields": [
                        {
                            "answer": "$asset_type",
                            "key": "yaQoxU",
                            "title": "Asset type",
                            "type": "list"
                        }
                    ],
                    "question": "About your project",
                    "status": "COMPLETED"
                },
                {
                    "fields": [
                        {
                            "answer": "buy-the-asset",
                            "key": "VWkLlk",
                            "title": "What do you intend to do with the asset?",
                            "type": "list"
                        },
                        {
                            "answer": false,
                            "key": "IRfSZp",
                            "title": "Do you know who currently owns your asset?",
                            "type": "list"
                        }
                    ],
                    "question": "About your project",
                    "status": "COMPLETED"
                },
                {
                    "fields": [
                        {
                            "answer": "Current Owner",
                            "key": "FtDJfK",
                            "title": "Describe the current ownership status",
                            "type": "text"
                        }
                    ],
                    "question": "About your project",
                    "status": "COMPLETED"
                },
                {
                    "fields": [
                        {
                            "answer": false,
                            "key": "gkulUE",
                            "title": "Have you already completed the purchase or lease?",
                            "type": "list"
                        }
                    ],
                    "question": "About your project",
                    "status": "COMPLETED"
                },
                {
                    "fields": [
                        {
                            "answer": "Test",
                            "key": "nvMmGE",
                            "title": "Describe the expected sale process, or the proposed terms of your lease if you are renting the asset",
                            "type": "text"
                        },
                        {
                            "answer": "2022-12-01",
                            "key": "ghzLRv",
                            "title": "Expected date of sale or lease",
                            "type": "date"
                        }
                    ],
                    "question": "About your project",
                    "status": "COMPLETED"
                },
                {
                    "fields": [
                        {
                            "answer": false,
                            "key": "Wyesgy",
                            "title": "Is your asset currently publicly owned?",
                            "type": "list"
                        }
                    ],
                    "question": "About your project",
                    "status": "COMPLETED"
                },
                {
                    "fields": [
                        {
                            "answer": false,
                            "key": "hvzzWB",
                            "title": "Is this a registered Asset of Community Value (ACV)?",
                            "type": "list"
                        }
                    ],
                    "question": "About your project",
                    "status": "COMPLETED"
                },
                {
                    "fields": [
                        {
                            "answer": false,
                            "key": "VwxiGn",
                            "title": "Is the asset listed for disposal, or part of a Community Asset Transfer?",
                            "type": "list"
                        }
                    ],
                    "question": "About your project ",
                    "status": "COMPLETED"
                },
                {
                    "fields": [
                        {
                            "answer": [
                                "for-sale-or-listed-for-disposal"
                            ],
                            "key": "UDTxqC",
                            "title": "Why is the asset at risk of closure?",
                            "type": "list"
                        }
                    ],
                    "question": "About your project",
                    "status": "COMPLETED"
                }
            ],
            "status": "COMPLETED"
        },
        {
            "name": "community-engagement",
            "questions": [
                {
                    "fields": [
                        {
                            "answer": "Tell us how you have engaged with the community about your intention to take ownership of the asset",
                            "key": "HJBgvw",
                            "title": "Tell us how you have engaged with the community about your intention to take ownership of the asset, and explain how this has shaped your project plans",
                            "type": "text"
                        },
                        {
                            "answer": false,
                            "key": "JCACTy",
                            "title": "Have you done any fundraising in the community?",
                            "type": "list"
                        }
                    ],
                    "question": "Strategic case",
                    "status": "COMPLETED"
                },
                {
                    "fields": [
                        {
                            "answer": "Tell us how your project supports any wider local plans",
                            "key": "NZKHOp",
                            "title": "Tell us how your project supports any wider local plans",
                            "type": "text"
                        }
                    ],
                    "question": "Strategic case",
                    "status": "COMPLETED"
                }
            ],
            "status": "COMPLETED"
        },
        {
            "name": "funding-required",
            "questions": [
                {
                    "fields": [
                        {
                            "answer": "$capital_funding",
                            "key": "JzWvhj",
                            "title": "Capital funding",
                            "type": "text"
                        },
                        {
                            "answer": "$revenue_funding",
                            "key": "jLIgoi",
                            "title": "Revenue funding (optional)",
                            "type": "text"
                        }
                    ],
                    "question": "Management case ",
                    "status": "COMPLETED"
                },
                {
                    "fields": [
                        {
                            "answer": [
                                "Capital Funding : £2300"
                            ],
                            "key": "multiInputField",
                            "title": "Capital costs",
                            "type": "text"
                        }
                    ],
                    "question": "Management case ",
                    "status": "COMPLETED"
                },
                {
                    "fields": [
                        {
                            "answer": false,
                            "key": "NWTKzQ",
                            "title": "Are you applying for revenue funding from the Community Ownership Fund? (optional)",
                            "type": "list"
                        }
                    ],
                    "question": "Management case ",
                    "status": "COMPLETED"
                },
                {
                    "fields": [
                        {
                            "answer": false,
                            "key": "DIZZOC",
                            "title": "Have you secured any match funding yet?",
                            "type": "list"
                        }
                    ],
                    "question": "Management case",
                    "status": "COMPLETED"
                },
                {
                    "fields": [
                        {
                            "answer": false,
                            "key": "RvbwSX",
                            "title": "Do you have any match funding identified but not yet secured?",
                            "type": "list"
                        }
                    ],
                    "question": "Management case",
                    "status": "COMPLETED"
                },
                {
                    "fields": [
                        {
                            "answer": "2300",
                            "key": "fnIdkJ",
                            "title": "Asset value",
                            "type": "text"
                        }
                    ],
                    "question": "Management case ",
                    "status": "COMPLETED"
                }
            ],
            "status": "COMPLETED"
        },
        {
            "name": "community-benefits",
            "questions": [
                {
                    "fields": [
                        {
                            "answer": [
                                "community-pride"
                            ],
                            "key": "QjJtbs",
                            "title": "What community benefits do you expect to deliver with this project? ",
                            "type": "list"
                        },
                        {
                            "answer": "Test",
                            "key": "gDTsgG",
                            "title": "Tell us about these benefits in detail, and explain how you'll measure the benefits it'll bring for the community",
                            "type": "text"
                        },
                        {
                            "answer": "Test",
                            "key": "kYjJFy",
                            "title": "Explain how you plan to sustain, and potentially expand, these benefits over time",
                            "type": "text"
                        },
                        {
                            "answer": "Test",
                            "key": "UbjYqE",
                            "title": "Tell us how you'll make sure the whole community benefits from the asset",
                            "type": "text"
                        }
                    ],
                    "question": "Potential to deliver community benefits",
                    "status": "COMPLETED"
                }
            ],
            "status": "COMPLETED"
        },
        {
            "name": "inclusiveness-and-integration",
            "questions": [
                {
                    "fields": [
                        {
                            "answer": "Test",
                            "key": "SrtVAs",
                            "title": "Describe the planned activities or services that will take place at the asset",
                            "type": "text"
                        },
                        {
                            "answer": "Test",
                            "key": "YbfbSC",
                            "title": "Describe anything that might prevent people from using the asset or participating in its running",
                            "type": "text"
                        },
                        {
                            "answer": "Test",
                            "key": "KuhSWw",
                            "title": "Tell us how you'll make your project accessible and inclusive to everyone in the community",
                            "type": "text"
                        },
                        {
                            "answer": "Test",
                            "key": "bkJsiO",
                            "title": "Describe how the project will bring people together from all over the community",
                            "type": "text"
                        }
                    ],
                    "question": "Management case",
                    "status": "COMPLETED"
                }
            ],
            "status": "COMPLETED"
        },
        {
            "name": "project-costs",
            "questions": [
                {
                    "fields": [
                        {
                            "answer": "Test",
                            "key": "WDDkVB",
                            "title": "Summarise your cash flow for the running of the asset",
                            "type": "text"
                        },
                        {
                            "answer": false,
                            "key": "oaIntA",
                            "title": "If successful, will you use your funding in the next 12 months?",
                            "type": "list"
                        }
                    ],
                    "question": "Management case",
                    "status": "COMPLETED"
                },
                {
                    "fields": [
                        {
                            "answer": [
                                "Income Test : £2300"
                            ],
                            "key": "multiInputField",
                            "title": "Sources of income",
                            "type": "text"
                        }
                    ],
                    "question": "Management case",
                    "status": "COMPLETED"
                },
                {
                    "fields": [
                        {
                            "answer": [
                                "Running Cost Test : £2300"
                            ],
                            "key": "multiInputField-2",
                            "title": "Running costs",
                            "type": "text"
                        }
                    ],
                    "question": "Management case",
                    "status": "COMPLETED"
                }
            ],
            "status": "COMPLETED"
        },
        {
            "name": "community-representation",
            "questions": [
                {
                    "fields": [
                        {
                            "answer": "Test",
                            "key": "JnvsPq",
                            "title": "List the members of your board",
                            "type": "text"
                        },
                        {
                            "answer": "Test",
                            "key": "yMCivI",
                            "title": "Tell us about your governance and membership structures",
                            "type": "text"
                        },
                        {
                            "answer": "Test",
                            "key": "NUZOvS",
                            "title": "Explain how you'll consider the views of the community in the running of the asset",
                            "type": "text"
                        }
                    ],
                    "question": "Management case",
                    "status": "COMPLETED"
                }
            ],
            "status": "COMPLETED"
        },
        {
            "name": "value-to-the-community",
            "questions": [
                {
                    "fields": [
                        {
                            "answer": "Test",
                            "key": "oOPUXI",
                            "title": "Tell us about your local community as a whole",
                            "type": "text"
                        },
                        {
                            "answer": "Test",
                            "key": "NKOmNL",
                            "title": "Describe any specific challenges your community faces, and how the asset will address these",
                            "type": "text"
                        }
                    ],
                    "question": "Added value to the community",
                    "status": "COMPLETED"
                }
            ],
            "status": "COMPLETED"
        },
        {
            "name": "declarations",
            "questions": [
                {
                    "fields": [
                        {
                            "answer": true,
                            "key": "LlvhYl",
                            "title": "Confirm you have considered subsidy control and state aid implications for your project, and the information you have given us is correct",
                            "type": "list"
                        },
                        {
                            "answer": false,
                            "key": "wJrJWY",
                            "title": "Confirm you have considered people with protected characteristics throughout the planning of your project",
                            "type": "list"
                        },
                        {
                            "answer": true,
                            "key": "COiwQr",
                            "title": "Confirm you have considered sustainability and the environment throughout the planning of your project, including compliance with the government's Net Zero ambitions",
                            "type": "list"
                        },
                        {
                            "answer": false,
                            "key": "bRPzWU",
                            "title": "Confirm you have a bank account set up and associated with the organisation you are applying on behalf of",
                            "type": "list"
                        }
                    ],
                    "question": "Declarations",
                    "status": "COMPLETED"
                }
            ],
            "status": "COMPLETED"
        }
    ],
    "fund_id": "$fund_id",
    "id": "$app_id" ,
    "last_edited": "2022-10-27T08:32:11.843201",
    "project_name": "$project_name" ,
    "reference": "$short_ref" ,
    "round_id": "$round_id",
    "round_name": "Round 2 Window 2",
    "started_at": "2022-10-27T08:28:55.699864",
    "status": "SUBMITTED",
    "language": "en",
    "location_json_blob": {
        "error": $location_error,
        "county": "$location_county",
        "region": "$location_region",
        "country": "$location_country",
        "postcode": "$location_postcode",
        "constituency": "$location_constituency"
    }

}
"""
)

cofr3w1_application_store_json_template = Template(
    """
    {
    "id": "$app_id",
    "status": "SUBMITTED",
    "fund_id": "$fund_id",
    "language": "en",
    "round_id": "$round_id",
    "reference": "$short_ref",
    "account_id": "53433826-95b3-42b1-b56f-aee3405a1b9f",
    "round_name": "Round 3 Window 1",
    "started_at": "2023-06-05T10:52:24.629455",
    "last_edited": "2023-06-06T13:38:48.747499",
    "project_name": "$project_name",
    "date_submitted": "2023-06-06T13:38:51.467199",
    "forms": [
        {
            "name": "declarations-cof-r3-w1",
            "status": "COMPLETED",
            "questions": [
                {
                    "fields": [
                        {
                            "key": "vSQKwD",
                            "type": "list",
                            "title": "Confirm you have considered subsidy control and state aid implications for your project, and the information you have given us is correct",
                            "answer": true
                        },
                        {
                            "key": "CQoLFp",
                            "type": "list",
                            "title": "Confirm you have considered people with protected characteristics throughout the planning of your project",
                            "answer": true
                        },
                        {
                            "key": "jdPkiX",
                            "type": "list",
                            "title": "Confirm you have considered sustainability and the environment throughout the planning of your project, including compliance with the government's Net Zero ambitions",
                            "answer": true
                        },
                        {
                            "key": "qWuSCy",
                            "type": "list",
                            "title": "Confirm you have a bank account set up and associated with the organisation you are applying on behalf of",
                            "answer": true
                        },
                        {
                            "key": "tjZlml",
                            "type": "list",
                            "title": "Confirm that the information you've provided in this application is accurate to the best of your knowledge on the date of submission",
                            "answer": true
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "LkvizC",
                    "question": "Agree to the final confirmations"
                }
            ]
        },
        {
            "name": "funding-required-cof-r3-w1",
            "status": "COMPLETED",
            "questions": [
                {
                    "fields": [
                        {
                            "key": "ABROnB",
                            "type": "text",
                            "title": "Capital funding",
                            "answer": "$capital_funding"
                        },
                        {
                            "key": "cLDRvN",
                            "type": "text",
                            "title": "Revenue funding (optional)",
                            "answer": "$revenue_funding"
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "bgUGuD",
                    "question": "Total funding request from the Community Ownership Fund"
                },
                {
                    "fields": [
                        {
                            "key": "qQLyXL",
                            "type": "multiInput",
                            "title": "Capital costs",
                            "answer": [
                                {
                                    "GLQlOh": "Capital Funding",
                                    "JtwkMy": 2300
                                }
                            ]
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "bgUGuD",
                    "question": "Capital costs for your project"
                },
                {
                    "fields": [
                        {
                            "key": "DOvZvB",
                            "type": "list",
                            "title": "Have you secured any match funding yet?",
                            "answer": false
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "bgUGuD",
                    "question": "If you've secured match funding"
                },
                {
                    "fields": [
                        {
                            "key": "DmgsiG",
                            "type": "list",
                            "title": "Do you have any match funding identified but not yet secured?",
                            "answer": false
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "bgUGuD",
                    "question": "If you’ve identified further match funding"
                },
                {
                    "fields": [
                        {
                            "key": "matkNH",
                            "type": "list",
                            "title": "Are you applying for revenue funding from the Community Ownership Fund? (optional)",
                            "answer": false
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "bgUGuD",
                    "question": "Revenue funding"
                }
            ]
        },
        {
            "name": "community-representation-cof-r3-w1",
            "status": "COMPLETED",
            "questions": [
                {
                    "fields": [
                        {
                            "key": "ReomFo",
                            "type": "freeText",
                            "title": "List the members of your board",
                            "answer": "<p>Test Community Representation Form</p>"
                        },
                        {
                            "key": "fjVmOt",
                            "type": "freeText",
                            "title": "Tell us about your governance and membership structures",
                            "answer": "<p>Test Community Representation Form</p>"
                        },
                        {
                            "key": "GETNxN",
                            "type": "freeText",
                            "title": "Explain how you'll consider the views of the community in the running of the asset",
                            "answer": "<p>Test Community Representation Form</p>"
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "KbnmOO",
                    "question": "How you’ll run the asset"
                }
            ]
        },
        {
            "name": "operational-costs-cof-r3-w1",
            "status": "COMPLETED",
            "questions": [
                {
                    "fields": [
                        {
                            "key": "qXNkfr",
                            "type": "freeText",
                            "title": "Describe your cash flow for the running of the asset",
                            "answer": "<p>Summarise your cash flow for the running of the asset</p>"
                        },
                        {
                            "key": "qQSVEn",
                            "type": "list",
                            "title": "If successful, will you use your funding in the next 12 months?",
                            "answer": false
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "oSfXFZ",
                    "question": "Cashflow to run the asset"
                },
                {
                    "fields": [
                        {
                            "key": "MSNJQD",
                            "type": "multiInput",
                            "title": "Sources of income",
                            "answer": [
                                {
                                    "AJEWXD": "Income Test 2",
                                    "cHFrIp": 2300
                                }
                            ]
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "oSfXFZ",
                    "question": "Income to run the asset"
                },
                {
                    "fields": [
                        {
                            "key": "NPgwcH",
                            "type": "multiInput",
                            "title": "Running costs",
                            "answer": [
                                {
                                    "IIdfRj": "Running Cost Test",
                                    "wlGQua": 2300
                                }
                            ]
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "oSfXFZ",
                    "question": "Running costs of the asset"
                }
            ]
        },
        {
            "name": "skills-and-resources-cof-r3-w1",
            "status": "COMPLETED",
            "questions": [
                {
                    "fields": [
                        {
                            "key": "XXGyzn",
                            "type": "freeText",
                            "title": "Describe any relevant experience you have delivering similar projects or running an asset",
                            "answer": "<p>Describe any relevant experience you have delivering similar projects or running an asset</p>"
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "eLpYFr",
                    "question": "Your experience running similar assets"
                },
                {
                    "fields": [
                        {
                            "key": "Uaeyae",
                            "type": "list",
                            "title": "Do you have plans to recruit people to help you run the asset?",
                            "answer": false
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "eLpYFr",
                    "question": "Recruitment plans"
                }
            ]
        },
        {
            "name": "inclusiveness-and-integration-cof-r3-w1",
            "status": "COMPLETED",
            "questions": [
                {
                    "fields": [
                        {
                            "key": "mgIesb",
                            "type": "freeText",
                            "title": "Tell us how the asset will be accountable to local people, and involve them in its running",
                            "answer": "<p>Test Inclusiveness and Integration Form</p>"
                        },
                        {
                            "key": "lQEkep",
                            "type": "freeText",
                            "title": "Describe anything that might prevent people from using the asset or participating in its running",
                            "answer": "<p>Test Inclusiveness and Integration Form</p>"
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "eCZBSV",
                    "question": "How you’ll make the asset inclusive"
                }
            ]
        },
        {
            "name": "applicant-information-cof-r3-w1",
            "status": "COMPLETED",
            "questions": [
                {
                    "fields": [
                        {
                            "key": "SnLGJE",
                            "type": "text",
                            "title": "Name of lead contact",
                            "answer": "Joe Bloggs"
                        },
                        {
                            "key": "qRDTUc",
                            "type": "text",
                            "title": "Lead contact job title",
                            "answer": "Mr"
                        },
                        {
                            "key": "NlHSBg",
                            "type": "text",
                            "title": "Lead contact email address",
                            "answer": "testemailfundingservice@testemailfundingservice.com"
                        },
                        {
                            "key": "FhBkJQ",
                            "type": "text",
                            "title": "Lead contact telephone number",
                            "answer": "0000000000"
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "ZuHuGk",
                    "question": "Lead contact details"
                }
            ]
        },
        {
            "name": "environmental-sustainability-cof-r3-w1",
            "status": "COMPLETED",
            "questions": [
                {
                    "fields": [
                        {
                            "key": "dypuJs",
                            "type": "freeText",
                            "title": "Tell us how you have considered the environmental sustainability of your project",
                            "answer": "<p>Test Environmental Sustainability Form</p>"
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "ljcxPd",
                    "question": "How you've considered the environment"
                }
            ]
        },
        {
            "name": "feasibility-cof-r3-w1",
            "status": "COMPLETED",
            "questions": [
                {
                    "fields": [
                        {
                            "key": "iSbwDM",
                            "type": "freeText",
                            "title": "Tell us about the feasibility studies you have carried out for your project",
                            "answer": "<p>Tell us about the feasibility studies you have carried out for your project</p>"
                        },
                        {
                            "key": "jFPlEJ",
                            "type": "list",
                            "title": "Do you need to do any further feasibility work?",
                            "answer": false
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "bBGnkL",
                    "question": "Feasiblity studies you've carried out"
                }
            ]
        },
        {
            "name": "local-support-cof-r3-w1",
            "status": "COMPLETED",
            "questions": [
                {
                    "fields": [
                        {
                            "key": "tDVPnl",
                            "type": "freeText",
                            "title": "Tell us about the local support for your project",
                            "answer": "<p>Tell us about the local support for your project</p>"
                        },
                        {
                            "key": "bDWjTN",
                            "type": "text",
                            "title": "Upload supporting evidence",
                            "answer": null
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "apkBSm",
                    "question": "Your support for the project"
                }
            ]
        },
        {
            "name": "project-qualifications-cof-r3-w1",
            "status": "COMPLETED",
            "questions": [
                {
                    "fields": [
                        {
                            "key": "ZEKMQd",
                            "type": "list",
                            "title": "Does your project meet the definition of a subsidy?",
                            "answer": false
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "WsFJts",
                    "question": "If your project meets the definition"
                }
            ]
        },
        {
            "name": "risk-cof-r3-w1",
            "status": "COMPLETED",
            "questions": [
                {
                    "fields": [
                        {
                            "key": "EODncR",
                            "type": "text",
                            "title": "Risks to your project (document upload)",
                            "answer": "sample.txt"
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "HKdODf",
                    "question": "Your project risk register"
                }
            ]
        },
        {
            "name": "upload-business-plan-cof-r3-w1",
            "status": "COMPLETED",
            "questions": [
                {
                    "fields": [
                        {
                            "key": "ndpQJk",
                            "type": "text",
                            "title": "Upload business plan",
                            "answer": "sample.txt"
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "xtwqlH",
                    "question": "Your business plan"
                }
            ]
        },
        {
            "name": "project-information-cof-r3-w1",
            "status": "COMPLETED",
            "questions": [
                {
                    "fields": [
                        {
                            "key": "pWwCRM",
                            "type": "list",
                            "title": "Have you applied to the Community Ownership Fund before?",
                            "answer": false
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "qsnIGd",
                    "question": "Previous Community Ownership Fund applications"
                },
                {
                    "fields": [
                        {
                            "key": "apGjFS",
                            "type": "text",
                            "title": "Project name",
                            "answer": "$project_name"
                        },
                        {
                            "key": "bEWpAj",
                            "type": "freeText",
                            "title": "Tell us how the asset is currently being used, or how it has been used before, and why it's important to the community",
                            "answer": "<p>Test Project Information Form</p>"
                        },
                        {
                            "key": "uypCNM",
                            "type": "freeText",
                            "title": "Give a brief summary of your project, including what you hope to achieve",
                            "answer": "<p>Test Project Information Form</p>"
                        },
                        {
                            "key": "AgeRbd",
                            "type": "freeText",
                            "title": "Tell us about the planned activities and/or services that will take place in the asset",
                            "answer": "<p>Test Project Information Form</p>"
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "qsnIGd",
                    "question": "Project name and summary"
                },
                {
                    "fields": [
                        {
                            "key": "EfdliG",
                            "type": "text",
                            "title": "Address of the community asset",
                            "answer": "Test Address, null, Test Town Or City, null, $location_postcode"
                        },
                        {
                            "key": "fIEUcb",
                            "type": "text",
                            "title": " In which constituency is your asset?",
                            "answer": "Constituency"
                        },
                        {
                            "key": "SWfcTo",
                            "type": "text",
                            "title": "In which local council area is your asset?",
                            "answer": "Local Council"
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "qsnIGd",
                    "question": "Address of the asset"
                }
            ]
        },
        {
            "name": "community-benefits-cof-r3-w1",
            "status": "COMPLETED",
            "questions": [
                {
                    "fields": [
                        {
                            "key": "pqYxJO",
                            "type": "list",
                            "title": "What community benefits do you expect to deliver with this project?",
                            "answer": [
                                "community-pride"
                            ]
                        },
                        {
                            "key": "lgfiGB",
                            "type": "freeText",
                            "title": "Tell us about these benefits in detail, and how the asset's activities will help deliver them",
                            "answer": "<p>Test Community Benefits Form</p>"
                        },
                        {
                            "key": "zKKouR",
                            "type": "freeText",
                            "title": "Explain how you plan to deliver and sustain these benefits over time",
                            "answer": "<p>Test Community Benefits Form</p>"
                        },
                        {
                            "key": "ZyIQGI",
                            "type": "freeText",
                            "title": "Tell us how you'll make sure the whole community benefits from the asset",
                            "answer": "<p>Test Community Benefits Form</p>"
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "PTOBPV",
                    "question": "Benefits you'll deliver"
                }
            ]
        },
        {
            "name": "organisation-information-cof-r3-w1",
            "status": "COMPLETED",
            "questions": [
                {
                    "fields": [
                        {
                            "key": "WWWWxy",
                            "type": "text",
                            "title": "Your unique tracker number",
                            "answer": "ANON-###-###-###"
                        },
                        {
                            "key": "YdtlQZ",
                            "type": "text",
                            "title": "Organisation name",
                            "answer": "Test Change Answers"
                        },
                        {
                            "key": "iBCGxY",
                            "type": "list",
                            "title": "Does your organisation use any other names?",
                            "answer": false
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "JBqDtK",
                    "question": "Organisation names"
                },
                {
                    "fields": [
                        {
                            "key": "emVGxS",
                            "type": "freeText",
                            "title": "What is your organisation's main purpose?",
                            "answer": "<p>Test Org Form</p>"
                        },
                        {
                            "key": "btTtIb",
                            "type": "freeText",
                            "title": "Tell us about your organisation's main activities",
                            "answer": "<p>Test Org Form</p>"
                        },
                        {
                            "key": "SkocDi",
                            "type": "freeText",
                            "title": "Tell us about your organisation's main activities - Activity 2 ",
                            "answer": null
                        },
                        {
                            "key": "CNeeiC",
                            "type": "freeText",
                            "title": "Tell us about your organisation's main activities - Activity 3 ",
                            "answer": null
                        },
                        {
                            "key": "BBlCko",
                            "type": "list",
                            "title": "Have you delivered projects like this before?",
                            "answer": false
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "JBqDtK",
                    "question": "Purpose and activities"
                },
                {
                    "fields": [
                        {
                            "key": "lajFtB",
                            "type": "list",
                            "title": "Type of organisation",
                            "answer": "CIO"
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "JBqDtK",
                    "question": "How your organisation is classified"
                },
                {
                    "fields": [
                        {
                            "key": "aHIGbK",
                            "type": "text",
                            "title": "Charity number ",
                            "answer": "234388322"
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "JBqDtK",
                    "question": "Charity registration details"
                },
                {
                    "fields": [
                        {
                            "key": "DwfHtk",
                            "type": "list",
                            "title": "Is your organisation a trading subsidiary of a parent company?",
                            "answer": false
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "JBqDtK",
                    "question": "Trading subsidiaries"
                },
                {
                    "fields": [
                        {
                            "key": "ZQolYb",
                            "type": "text",
                            "title": "Organisation address",
                            "answer": "Test Address, null, Test Town Or City, null, $location_postcode"
                        },
                        {
                            "key": "zsoLdf",
                            "type": "list",
                            "title": "Is your correspondence address different to the organisation address?",
                            "answer": false
                        },
                        {
                            "key": "FhbaEy",
                            "type": "text",
                            "title": "Website and social media",
                            "answer": "https://twitter.com/luhc"
                        },
                        {
                            "key": "FcdKlB",
                            "type": "text",
                            "title": "Website and social media - Link or username 2",
                            "answer": null
                        },
                        {
                            "key": "BzxgDA",
                            "type": "text",
                            "title": "Website and social media - Link or username 3",
                            "answer": null
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "JBqDtK",
                    "question": "Organisation address"
                },
                {
                    "fields": [
                        {
                            "key": "hnLurH",
                            "type": "list",
                            "title": "Is your application a joint bid in partnership with other organisations?",
                            "answer": false
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "JBqDtK",
                    "question": "Joint applications"
                }
            ]
        },
        {
            "name": "community-engagement-cof-r3-w1",
            "status": "COMPLETED",
            "questions": [
                {
                    "fields": [
                        {
                            "key": "azCutK",
                            "type": "freeText",
                            "title": "Tell us how you have engaged with the community about your intention to take ownership of the asset",
                            "answer": "<p>Test Community Engagement Form</p>"
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "lmdhVN",
                    "question": "How you've engaged with the community"
                },
                {
                    "fields": [
                        {
                            "key": "jAhuWN",
                            "type": "freeText",
                            "title": "Describe your fundraising activities",
                            "answer": "<p>Test Community Engagement Form</p>"
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "lmdhVN",
                    "question": "Your fundraising activities"
                },
                {
                    "fields": [
                        {
                            "key": "HYsezC",
                            "type": "freeText",
                            "title": "Tell us about any partnerships you've formed, and how they'll help the project be successful",
                            "answer": "<p>Test Community Engagement Form</p>"
                        },
                        {
                            "key": "GGBgBY",
                            "type": "freeText",
                            "title": "Tell us how your project supports any wider local plans",
                            "answer": "<p>Test Community Engagement Form</p>"
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "lmdhVN",
                    "question": "Partnerships and local plans"
                }
            ]
        },
        {
            "name": "community-use-cof-r3-w1",
            "status": "COMPLETED",
            "questions": [
                {
                    "fields": [
                        {
                            "key": "zTcrYo",
                            "type": "freeText",
                            "title": "Who in the community currently uses the asset, or has used it in the past?",
                            "answer": "<p>Test Community Use Form</p>"
                        },
                        {
                            "key": "whlRYS",
                            "type": "freeText",
                            "title": "Tell us how losing the asset would affect, or has already affected, people in the community",
                            "answer": "<p>Test Community Use Form</p>"
                        },
                        {
                            "key": "NGSXHE",
                            "type": "freeText",
                            "title": "Why will the asset be lost without community intervention?",
                            "answer": "<p>Test Community Use Form</p>"
                        },
                        {
                            "key": "Ieudgn",
                            "type": "freeText",
                            "title": "Explain how the community will be better served with the asset under community ownership",
                            "answer": "<p>Test Community Use Form</p>"
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "GMkooI",
                    "question": "Who uses the asset"
                }
            ]
        },
        {
            "name": "asset-information-cof-r3-w1",
            "status": "COMPLETED",
            "questions": [
                {
                    "fields": [
                        {
                            "key": "oXGwlA",
                            "type": "list",
                            "title": "Asset type",
                            "answer": "$asset_type"
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "wxYZcT",
                    "question": "How the asset is used in the community"
                },
                {
                    "fields": [
                        {
                            "key": "LaxeJN",
                            "type": "list",
                            "title": "How do you intend to take community ownership of the asset?",
                            "answer": "buy-the-asset"
                        },
                        {
                            "key": "tTOrEp",
                            "type": "text",
                            "title": "Upload asset valuation or lease agreement",
                            "answer": "sample.txt"
                        },
                        {
                            "key": "hdmYjg",
                            "type": "list",
                            "title": "Do you know who currently owns your asset?",
                            "answer": false
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "wxYZcT",
                    "question": "The asset in community ownership"
                },
                {
                    "fields": [
                        {
                            "key": "CSsbsG",
                            "type": "text",
                            "title": "Describe the current ownership status",
                            "answer": "Current Owner"
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "wxYZcT",
                    "question": "Current ownership status"
                },
                {
                    "fields": [
                        {
                            "key": "uPvsqM",
                            "type": "list",
                            "title": "Have you already completed the purchase or lease?",
                            "answer": false
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "wxYZcT",
                    "question": "If you've already taken ownership"
                },
                {
                    "fields": [
                        {
                            "key": "XPcbJx",
                            "type": "freeText",
                            "title": "Describe the expected sale process, or the proposed terms of your lease if you are renting the asset",
                            "answer": "<p>Test Asset Information Form</p>"
                        },
                        {
                            "key": "jGjScT",
                            "type": "date",
                            "title": "Expected date of sale or lease",
                            "answer": "2022-12-01"
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "wxYZcT",
                    "question": "Expected terms of your ownership or lease"
                },
                {
                    "fields": [
                        {
                            "key": "VGXXyq",
                            "type": "list",
                            "title": "Is your asset currently publicly owned?",
                            "answer": false
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "wxYZcT",
                    "question": "Public ownership"
                },
                {
                    "fields": [
                        {
                            "key": "wjBFTf",
                            "type": "list",
                            "title": "Is this a registered Asset of Community Value (ACV)?",
                            "answer": false
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "wxYZcT",
                    "question": "Assets of community value"
                },
                {
                    "fields": [
                        {
                            "key": "HyWPwE",
                            "type": "list",
                            "title": "Is the asset listed for disposal, or part of a Community Asset Transfer?",
                            "answer": false
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "wxYZcT",
                    "question": "Assets listed for disposal"
                },
                {
                    "fields": [
                        {
                            "key": "KQlOaJ",
                            "type": "list",
                            "title": "Why is the asset at risk of closure?",
                            "answer": [
                                "for-sale-or-listed-for-disposal"
                            ]
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "wxYZcT",
                    "question": "Risk of closure"
                }
            ]
        }
    ]
}
"""
)

cofr3w2_application_store_json_template = Template(
    """
    {
    "id": "$app_id",
    "language": "en",
    "fund_id": "$fund_id",
    "last_edited": "2023-09-04T15:54:15.234643",
    "project_name": "$project_name",
    "reference": "$short_ref",
    "round_id": "$round_id",
    "round_name": "Round 3 Window 3",
    "started_at": "2023-09-04T15:48:57.567040",
    "status": "SUBMITTED",
    "account_id": "1e8884e2-b043-427f-ba09-7ec2ca409ef0",
    "date_submitted": "2023-09-04T15:54:30.373564",
    "forms": [
      {
        "name": "community-use-cof-r3-w2",
        "questions": [
          {
            "category": "GMkooI",
            "fields": [
              {
                "answer": "<p>Test Community Use Form</p>",
                "key": "zTcrYo",
                "title": "Who in the community currently uses the asset, or has used it in the past?",
                "type": "freeText"
              },
              {
                "answer": "<p>Test Community Use Form</p>",
                "key": "whlRYS",
                "title": "Tell us how losing the asset would affect, or has already affected, people in the community",
                "type": "freeText"
              },
              {
                "answer": "<p>Test Community Use Form</p>",
                "key": "NGSXHE",
                "title": "Why will the asset be lost without community intervention?",
                "type": "freeText"
              },
              {
                "answer": "<p>Test Community Use Form</p>",
                "key": "Ieudgn",
                "title": "Explain how the community will be better served with the asset under community ownership",
                "type": "freeText"
              }
            ],
            "question": "Who uses the asset",
            "status": "COMPLETED"
          }
        ],
        "status": "COMPLETED"
      },
      {
        "name": "community-engagement-cof-r3-w2",
        "questions": [
          {
            "category": "lmdhVN",
            "fields": [
              {
                "answer": "<p>Test Community Engagement Form</p>",
                "key": "azCutK",
                "title": "Tell us how you have engaged with the community about your intention to take ownership of the asset",
                "type": "freeText"
              }
            ],
            "question": "How you've engaged with the community",
            "status": "COMPLETED"
          },
          {
            "category": "lmdhVN",
            "fields": [
              {
                "answer": "<p>Test Community Engagement Form</p>",
                "key": "jAhuWN",
                "title": "Describe your fundraising activities",
                "type": "freeText"
              }
            ],
            "question": "Your fundraising activities",
            "status": "COMPLETED"
          },
          {
            "category": "lmdhVN",
            "fields": [
              {
                "answer": "<p>Test Community Engagement Form</p>",
                "key": "HYsezC",
                "title": "Tell us about any partnerships you've formed, and how they'll help the project be successful",
                "type": "freeText"
              },
              {
                "answer": "<p>Test Community Engagement Form</p>",
                "key": "GGBgBY",
                "title": "Tell us how your project supports any wider local plans",
                "type": "freeText"
              }
            ],
            "question": "Partnerships and local plans",
            "status": "COMPLETED"
          }
        ],
        "status": "COMPLETED"
      },
      {
        "name": "asset-information-cof-r3-w2",
        "questions": [
          {
            "category": "wxYZcT",
            "fields": [
              {
                "answer": "$asset_type",
                "key": "oXGwlA",
                "title": "Asset type",
                "type": "list"
              }
            ],
            "question": "How the asset is used in the community",
            "status": "COMPLETED"
          },
          {
            "category": "wxYZcT",
            "fields": [
              {
                "answer": "buy-the-asset",
                "key": "LaxeJN",
                "title": "How do you intend to take community ownership of the asset?",
                "type": "list"
              }
            ],
            "question": "The asset in community ownership",
            "status": "COMPLETED"
          },
          {
            "category": "wxYZcT",
            "fields": [
              {
                "answer": "sample.txt",
                "key": "tTOrEp",
                "title": "Please upload evidence that shows the asset valuation (if you are buying the asset) or the lease agreement (if you are leasing the asset).",
                "type": "text"
              }
            ],
            "question": "Upload asset valuation or lease agreement",
            "status": "COMPLETED"
          },
          {
            "category": "wxYZcT",
            "fields": [
              {
                "answer": true,
                "key": "wAUFqr",
                "title": "Do you know who currently owns your asset?",
                "type": "list"
              }
            ],
            "question": "Who owns the asset",
            "status": "COMPLETED"
          },
          {
            "category": "wxYZcT",
            "fields": [
              {
                "answer": "Mr. Shannon Gorczany",
                "key": "FOURVe",
                "title": "Name of current asset owner",
                "type": "text"
              }
            ],
            "question": "Who currently owns your asset",
            "status": "COMPLETED"
          },
          {
            "category": "wxYZcT",
            "fields": [
              {
                "answer": "<p>Test Asset Information Form</p>",
                "key": "XPcbJx",
                "title": "Describe the expected sale process, or the proposed terms of your lease if you are planning to rent the asset",
                "type": "freeText"
              },
              {
                "answer": "2022-12-01",
                "key": "jGjScT",
                "title": "Expected date of sale or lease",
                "type": "date"
              }
            ],
            "question": "Expected terms of your ownership or lease",
            "status": "COMPLETED"
          },
          {
            "category": "wxYZcT",
            "fields": [
              {
                "answer": false,
                "key": "VGXXyq",
                "title": "Is your asset currently publicly owned?",
                "type": "list"
              }
            ],
            "question": "Public ownership",
            "status": "COMPLETED"
          },
          {
            "fields": [
                {
                    "key": "wjBFTf",
                    "type": "list",
                    "title": "Is this a registered Asset of Community Value (ACV)?",
                    "answer": false
                }
            ],
            "status": "COMPLETED",
            "category": "wxYZcT",
            "question": "Assets of community value"
          },
          {
            "category": "wxYZcT",
            "fields": [
              {
                "answer": [
                  "Sale",
                  "Listed for disposal",
                  "Part of a Community Asset Transfer"
                ],
                "key": "qlqyUq",
                "title": "Why is the asset at risk of closure?",
                "type": "list"
              }
            ],
            "question": "Risk of closure",
            "status": "COMPLETED"
          },
          {
            "category": "wxYZcT",
            "fields": [
              {
                "answer": "2022-12-01",
                "key": "QPIPjx",
                "title": "When was the asset listed?",
                "type": "date"
              },
              {
                "answer": "https://twitter.com/luhc",
                "key": "OJWGGr",
                "title": "Provide a link to the listing",
                "type": "text"
              }
            ],
            "question": "Asset listing details",
            "status": "COMPLETED"
          },
          {
            "category": "wxYZcT",
            "fields": [
              {
                "answer": "<p>Test Asset Information Form</p>",
                "key": "WKIGQE",
                "title": "Describe the current status of the Community Asset Transfer",
                "type": "freeText"
              }
            ],
            "question": "Community asset transfer",
            "status": "COMPLETED"
          },
          {
            "category": "wxYZcT",
            "fields": [
              {
                "answer": false,
                "key": "iqnlTk",
                "title": "Is this a registered Asset of Community Value (ACV)?",
                "type": "list"
              }
            ],
            "question": "Assets of community value",
            "status": "COMPLETED"
          }
        ],
        "status": "COMPLETED"
      },
      {
        "name": "funding-required-cof-r3-w2",
        "questions": [
          {
            "category": "bgUGuD",
            "fields": [
              {
                "answer": "$capital_funding",
                "key": "ABROnB",
                "title": "Capital funding request",
                "type": "text"
              },
              {
                "answer": true,
                "key": "hJkmBS",
                "title": "If successful, will you use your funding in the next 12 months?",
                "type": "list"
              }
            ],
            "question": "Capital funding request",
            "status": "COMPLETED"
          },
          {
            "category": "bgUGuD",
            "fields": [
              {
                "answer": [
                  {
                    "GLQlOh": "Capital Funding",
                    "JtwkMy": 571
                  }
                ],
                "key": "qQLyXL",
                "title": "Capital costs",
                "type": "multiInput"
              }
            ],
            "question": "Capital costs for your project",
            "status": "COMPLETED"
          },
          {
            "category": "bgUGuD",
            "fields": [
              {
                "answer": true,
                "key": "DOvZvB",
                "title": "Have you secured any match funding yet?",
                "type": "list"
              }
            ],
            "question": "If you've secured match funding",
            "status": "COMPLETED"
          },
          {
            "category": "bgUGuD",
            "fields": [
              {
                "answer": [
                  {
                    "JKqLWU": "Secured Match Funding",
                    "LVJcDC": 571
                  }
                ],
                "key": "MopCmv",
                "title": "Secured match funding",
                "type": "multiInput"
              }
            ],
            "question": "Secured match funding",
            "status": "COMPLETED"
          },
          {
            "category": "bgUGuD",
            "fields": [
              {
                "answer": true,
                "key": "HgpNUe",
                "title": "Have you already spent the match funding you have secured?",
                "type": "list"
              }
            ],
            "question": "Have you already spent the match funding you have secured?",
            "status": "COMPLETED"
          },
          {
            "category": "bgUGuD",
            "fields": [
              {
                "answer": true,
                "key": "DmgsiG",
                "title": "Have you identified, but not yet secured, any additional match funding?",
                "type": "list"
              }
            ],
            "question": "If you’ve identified further match funding",
            "status": "COMPLETED"
          },
          {
            "category": "bgUGuD",
            "fields": [
              {
                "answer": [
                  {
                    "THOdae": 571,
                    "iMJdfs": "Unsecured Match Funding"
                  }
                ],
                "key": "vEOdBS",
                "title": "Unsecured match funding",
                "type": "multiInput"
              }
            ],
            "question": "Unsecured match funding",
            "status": "COMPLETED"
          },
          {
            "category": "bgUGuD",
            "fields": [
              {
                "answer": true,
                "key": "matkNH",
                "title": "Are you applying for revenue funding from the Community Ownership Fund? (optional)",
                "type": "list"
              }
            ],
            "question": "Revenue funding",
            "status": "COMPLETED"
          },
          {
            "category": "bgUGuD",
            "fields": [
              {
                "answer": [
                  {
                    "UyaAHw": $revenue_funding,
                    "hGsUaZ": "Revenue Costs 1"
                  },
                  {
                    "UyaAHw": $revenue_funding,
                    "hGsUaZ": "Revenue Costs 2"
                  }
                ],
                "key": "tSKhQQ",
                "title": "Revenue costs (optional)",
                "type": "multiInput"
              }
            ],
            "question": "Revenue costs (optional)",
            "status": "COMPLETED"
          },
          {
            "category": "bgUGuD",
            "fields": [
              {
                "answer": "<p>Tell us how the revenue funding you've requested will help run the asset</p>",
                "key": "XPDbsl",
                "title": "Tell us how the revenue funding you've requested will help run the asset",
                "type": "freeText"
              }
            ],
            "question": "How you'll use revenue funding",
            "status": "COMPLETED"
          }
        ],
        "status": "COMPLETED"
      },
      {
        "name": "skills-and-resources-cof-r3-w2",
        "questions": [
          {
            "category": "eLpYFr",
            "fields": [
              {
                "answer": "<p>Describe any relevant experience you have delivering similar projects or running an asset</p>",
                "key": "XXGyzn",
                "title": "Describe any relevant experience you have delivering similar projects or running an asset",
                "type": "freeText"
              }
            ],
            "question": "Your experience running similar assets",
            "status": "COMPLETED"
          },
          {
            "category": "eLpYFr",
            "fields": [
              {
                "answer": false,
                "key": "Uaeyae",
                "title": "Do you have plans to recruit people to help you run the asset?",
                "type": "list"
              }
            ],
            "question": "Recruitment plans",
            "status": "COMPLETED"
          }
        ],
        "status": "COMPLETED"
      },
      {
        "name": "organisation-information-cof-r3-w2",
        "questions": [
          {
            "category": "JBqDtK",
            "fields": [
              {
                "answer": "ANON-###-###-###",
                "key": "WWWWxy",
                "title": "Your unique tracker number",
                "type": "text"
              },
              {
                "answer": "Collier, Heaney and Bosco",
                "key": "YdtlQZ",
                "title": "Organisation name",
                "type": "text"
              },
              {
                "answer": false,
                "key": "iBCGxY",
                "title": "Does your organisation use any other names?",
                "type": "list"
              }
            ],
            "question": "Organisation names",
            "status": "COMPLETED"
          },
          {
            "category": "JBqDtK",
            "fields": [
              {
                "answer": "<p>Test Org Form</p>",
                "key": "emVGxS",
                "title": "What is your organisation's main purpose?",
                "type": "freeText"
              },
              {
                "answer": "<p>Test Org Form</p>",
                "key": "btTtIb",
                "title": "Tell us about your organisation's main activities",
                "type": "freeText"
              },
              {
                "answer": null,
                "key": "SkocDi",
                "title": "Tell us about your organisation's main activities - Activity 2 ",
                "type": "freeText"
              },
              {
                "answer": null,
                "key": "CNeeiC",
                "title": "Tell us about your organisation's main activities - Activity 3 ",
                "type": "freeText"
              },
              {
                "answer": false,
                "key": "BBlCko",
                "title": "Have you delivered projects like this before?",
                "type": "list"
              }
            ],
            "question": "Purpose and activities",
            "status": "COMPLETED"
          },
          {
            "category": "JBqDtK",
            "fields": [
              {
                "answer": "CIO",
                "key": "lajFtB",
                "title": "Type of organisation",
                "type": "list"
              }
            ],
            "question": "How your organisation is classified",
            "status": "COMPLETED"
          },
          {
            "category": "JBqDtK",
            "fields": [
              {
                "answer": "7036286351201658",
                "key": "aHIGbK",
                "title": "Charity number ",
                "type": "text"
              }
            ],
            "question": "Charity registration details",
            "status": "COMPLETED"
          },
          {
            "category": "JBqDtK",
            "fields": [
              {
                "answer": false,
                "key": "DwfHtk",
                "title": "Is your organisation a trading subsidiary of a parent company?",
                "type": "list"
              }
            ],
            "question": "Trading subsidiaries",
            "status": "COMPLETED"
          },
          {
            "category": "JBqDtK",
            "fields": [
              {
                "answer": "4 Laurine Fold, null, St. Nienow, null, $location_postcode",
                "key": "ZQolYb",
                "title": "Organisation address",
                "type": "text"
              },
              {
                "answer": false,
                "key": "zsoLdf",
                "title": "Is your correspondence address different to the organisation address?",
                "type": "list"
              },
              {
                "answer": "https://twitter.com/luhc",
                "key": "FhbaEy",
                "title": "Website and social media",
                "type": "text"
              },
              {
                "answer": null,
                "key": "FcdKlB",
                "title": "Website and social media - Link or username 2",
                "type": "text"
              },
              {
                "answer": null,
                "key": "BzxgDA",
                "title": "Website and social media - Link or username 3",
                "type": "text"
              }
            ],
            "question": "Organisation address",
            "status": "COMPLETED"
          },
          {
            "category": "JBqDtK",
            "fields": [
              {
                "answer": false,
                "key": "hnLurH",
                "title": "Is your application a joint bid in partnership with other organisations?",
                "type": "list"
              }
            ],
            "question": "Joint applications",
            "status": "COMPLETED"
          }
        ],
        "status": "COMPLETED"
      },
      {
        "name": "feasibility-cof-r3-w2",
        "questions": [
          {
            "category": "bBGnkL",
            "fields": [
              {
                "answer": "<p>Tell us about the feasibility studies you have carried out for your project</p>",
                "key": "iSbwDM",
                "title": "Tell us about the feasibility studies you have carried out for your project",
                "type": "freeText"
              },
              {
                "answer": false,
                "key": "jFPlEJ",
                "title": "Do you need to do any further feasibility work?",
                "type": "list"
              }
            ],
            "question": "Feasiblity studies you've carried out",
            "status": "COMPLETED"
          }
        ],
        "status": "COMPLETED"
      },
      {
        "name": "project-information-cof-r3-w2",
        "questions": [
          {
            "category": "qsnIGd",
            "fields": [
              {
                "answer": false,
                "key": "pWwCRM",
                "title": "Have you applied to the Community Ownership Fund before?",
                "type": "list"
              }
            ],
            "question": "Previous Community Ownership Fund applications",
            "status": "COMPLETED"
          },
          {
            "category": "qsnIGd",
            "fields": [
              {
                "answer": "$project_name",
                "key": "apGjFS",
                "title": "Project name",
                "type": "text"
              },
              {
                "answer": "<p>Test Project Information Form</p>",
                "key": "bEWpAj",
                "title": "Tell us how the asset is currently being used, or how it has been used before, and why it's important to the community",
                "type": "freeText"
              },
              {
                "answer": "<p>Test Project Information Form</p>",
                "key": "uypCNM",
                "title": "Give a brief summary of your project, including what you hope to achieve",
                "type": "freeText"
              },
              {
                "answer": "<p>Test Project Information Form</p>",
                "key": "AgeRbd",
                "title": "Tell us about the planned activities and/or services that will take place in the asset",
                "type": "freeText"
              }
            ],
            "question": "Project name and summary",
            "status": "COMPLETED"
          },
          {
            "category": "qsnIGd",
            "fields": [
              {
                "answer": "5 Haley-Powlowski End, null, Schmidt Common, null, $location_postcode",
                "key": "EfdliG",
                "title": "Address of the community asset",
                "type": "text"
              },
              {
                "answer": "Constituency",
                "key": "fIEUcb",
                "title": " In which constituency is your asset?",
                "type": "text"
              },
              {
                "answer": "Highlands and Islands",
                "key": "SWfcTo",
                "title": "In which local council area is your asset?",
                "type": "text"
              }
            ],
            "question": "Address of the asset",
            "status": "COMPLETED"
          }
        ],
        "status": "COMPLETED"
      },
      {
        "name": "declarations-cof-r3-w2",
        "questions": [
          {
            "category": "LkvizC",
            "fields": [
              {
                "answer": false,
                "key": "vSQKwD",
                "title": "Confirm you have considered subsidy control and state aid implications for your project, and the information you have given us is correct",
                "type": "list"
              },
              {
                "answer": false,
                "key": "CQoLFp",
                "title": "Confirm you have considered people with protected characteristics throughout the planning of your project",
                "type": "list"
              },
              {
                "answer": true,
                "key": "jdPkiX",
                "title": "Confirm you have considered sustainability and the environment throughout the planning of your project, including compliance with the government's Net Zero ambitions",
                "type": "list"
              },
              {
                "answer": false,
                "key": "qWuSCy",
                "title": "Confirm you have a bank account set up and associated with the organisation you are applying on behalf of",
                "type": "list"
              },
              {
                "answer": true,
                "key": "tjZlml",
                "title": "Confirm that the information you've provided in this application is accurate to the best of your knowledge on the date of submission",
                "type": "list"
              }
            ],
            "question": "Agree to the final confirmations",
            "status": "COMPLETED"
          }
        ],
        "status": "COMPLETED"
      },
      {
        "name": "applicant-information-cof-r3-w2",
        "questions": [
          {
            "category": "ZuHuGk",
            "fields": [
              {
                "answer": "Damion",
                "key": "SnLGJE",
                "title": "Name of lead contact",
                "type": "text"
              },
              {
                "answer": "National Accounts Strategist",
                "key": "qRDTUc",
                "title": "Lead contact job title",
                "type": "text"
              },
              {
                "answer": "Loraine89@yahoo.com",
                "key": "NlHSBg",
                "title": "Lead contact email address",
                "type": "text"
              },
              {
                "answer": "+44 75506381249",
                "key": "FhBkJQ",
                "title": "Lead contact telephone number",
                "type": "text"
              }
            ],
            "question": "Lead contact details",
            "status": "COMPLETED"
          }
        ],
        "status": "COMPLETED"
      },
      {
        "name": "upload-business-plan-cof-r3-w2",
        "questions": [
          {
            "category": "xtwqlH",
            "fields": [
              {
                "answer": "sample.txt",
                "key": "ndpQJk",
                "title": "Upload business plan",
                "type": "text"
              }
            ],
            "question": "Your business plan",
            "status": "COMPLETED"
          }
        ],
        "status": "COMPLETED"
      },
      {
        "name": "local-support-cof-r3-w2",
        "questions": [
          {
            "category": "apkBSm",
            "fields": [
              {
                "answer": "<p>Tell us about the local support for your project</p>",
                "key": "tDVPnl",
                "title": "Tell us about the local support for your project",
                "type": "freeText"
              },
              {
                "answer": null,
                "key": "bDWjTN",
                "title": "Upload supporting evidence (optional)",
                "type": "text"
              }
            ],
            "question": "Your support for the project",
            "status": "COMPLETED"
          }
        ],
        "status": "COMPLETED"
      },
      {
        "name": "community-representation-cof-r3-w2",
        "questions": [
          {
            "category": "KbnmOO",
            "fields": [
              {
                "answer": "<p>Test Community Representation Form</p>",
                "key": "ReomFo",
                "title": "List the members of your board",
                "type": "freeText"
              },
              {
                "answer": "<p>Test Community Representation Form</p>",
                "key": "fjVmOt",
                "title": "Tell us about your governance and membership structures",
                "type": "freeText"
              },
              {
                "answer": "<p>Test Community Representation Form</p>",
                "key": "GETNxN",
                "title": "Explain how you'll consider the views of the community in the running of the asset",
                "type": "freeText"
              }
            ],
            "question": "How you’ll run the asset",
            "status": "COMPLETED"
          }
        ],
        "status": "COMPLETED"
      },
      {
        "name": "operational-costs-cof-r3-w2",
        "questions": [
          {
            "category": "oSfXFZ",
            "fields": [
              {
                "answer": "<p>Summarise your income and operational costs for the running of the asset</p>",
                "key": "qXNkfr",
                "title": "Summarise your income and operational costs for the running of the asset",
                "type": "freeText"
              }
            ],
            "question": "Forecasted income and operational costs to run the asset",
            "status": "COMPLETED"
          }
        ],
        "status": "COMPLETED"
      },
      {
        "name": "inclusiveness-and-integration-cof-r3-w2",
        "questions": [
          {
            "category": "eCZBSV",
            "fields": [
              {
                "answer": "<p>Test Inclusiveness and Integration Form</p>",
                "key": "mgIesb",
                "title": "Tell us how the asset will be accountable to local people, and involve them in its running",
                "type": "freeText"
              },
              {
                "answer": "<p>Test Inclusiveness and Integration Form</p>",
                "key": "lQEkep",
                "title": "Describe anything that might prevent people from using the asset or participating in its running",
                "type": "freeText"
              }
            ],
            "question": "How you’ll make the asset inclusive",
            "status": "COMPLETED"
          }
        ],
        "status": "COMPLETED"
      },
      {
        "name": "environmental-sustainability-cof-r3-w2",
        "questions": [
          {
            "category": "ljcxPd",
            "fields": [
              {
                "answer": "<p>Test Environmental Sustainability Form</p>",
                "key": "dypuJs",
                "title": "Tell us how you have considered the environmental sustainability of your project",
                "type": "freeText"
              }
            ],
            "question": "How you've considered the environment",
            "status": "COMPLETED"
          }
        ],
        "status": "COMPLETED"
      },
      {
        "name": "community-benefits-cof-r3-w2",
        "questions": [
          {
            "category": "PTOBPV",
            "fields": [
              {
                "answer": [
                  "community-pride"
                ],
                "key": "pqYxJO",
                "title": "What community benefits do you expect to deliver with this project?",
                "type": "list"
              },
              {
                "answer": "<p>Test Community Benefits Form</p>",
                "key": "lgfiGB",
                "title": "Tell us about these benefits in detail, and how the asset's activities will help deliver them",
                "type": "freeText"
              },
              {
                "answer": "<p>Test Community Benefits Form</p>",
                "key": "zKKouR",
                "title": "Explain how you plan to deliver and sustain these benefits over time",
                "type": "freeText"
              },
              {
                "answer": "<p>Test Community Benefits Form</p>",
                "key": "ZyIQGI",
                "title": "Tell us how you'll make sure the whole community benefits from the asset",
                "type": "freeText"
              }
            ],
            "question": "Benefits you'll deliver",
            "status": "COMPLETED"
          }
        ],
        "status": "COMPLETED"
      },
      {
        "name": "project-qualifications-cof-r3-w2",
        "questions": [
          {
            "category": "WsFJts",
            "fields": [
              {
                "answer": false,
                "key": "ZEKMQd",
                "title": "Does your project meet the definition of a subsidy?",
                "type": "list"
              }
            ],
            "question": "If your project meets the definition",
            "status": "COMPLETED"
          }
        ],
        "status": "COMPLETED"
      },
      {
        "name": "risk-cof-r3-w2",
        "questions": [
          {
            "category": "HKdODf",
            "fields": [
              {
                "answer": "sample.txt",
                "key": "EODncR",
                "title": "Risks to your project (document upload)",
                "type": "text"
              }
            ],
            "question": "Your project risk register",
            "status": "COMPLETED"
          }
        ],
        "status": "COMPLETED"
      }
    ]
  }
"""
)


cofr3w3_application_store_json_template = Template(
    """
    {
    "id": "$app_id",
    "language": "en",
    "fund_id": "$fund_id",
    "last_edited": "2023-09-04T15:54:15.234643",
    "project_name": "$project_name",
    "reference": "$short_ref",
    "round_id": "$round_id",
    "round_name": "Round 3 Window 2",
    "started_at": "2023-09-04T15:48:57.567040",
    "status": "SUBMITTED",
    "account_id": "1e8884e2-b043-427f-ba09-7ec2ca409ef0",
    "date_submitted": "2023-09-04T15:54:30.373564",
    "forms": [
    {
      "name": "community-use-cof",
      "questions": [
        {
          "category": "GMkooI",
          "fields": [
            {
              "answer": "<p>test</p>",
              "key": "zTcrYo",
              "title": "Who in the community currently uses the asset, or has used it in the past?",
              "type": "freeText"
            },
            {
              "answer": "<p>test</p>",
              "key": "whlRYS",
              "title": "Tell us how losing the asset would affect, or has already affected, people in the community",
              "type": "freeText"
            },
            {
              "answer": "<p>test</p>",
              "key": "NGSXHE",
              "title": "Why will the asset be lost without community intervention?",
              "type": "freeText"
            },
            {
              "answer": "<p>test</p>",
              "key": "Ieudgn",
              "title": "Explain how the community will be better served with the asset under community ownership",
              "type": "freeText"
            }
          ],
          "index": 0,
          "question": "Who uses the asset",
          "status": "COMPLETED"
        },
        {
          "category": null,
          "fields": [
            {
              "answer": true,
              "key": "markAsComplete",
              "title": "Do you want to mark this section as complete?",
              "type": "boolean"
            }
          ],
          "question": "MarkAsComplete",
          "status": "COMPLETED"
        }
      ],
      "status": "COMPLETED"
    },
    {
      "name": "environmental-sustainability-cof",
      "questions": [
        {
          "category": "ljcxPd",
          "fields": [
            {
              "answer": "<p>test</p>",
              "key": "dypuJs",
              "title": "Tell us how you have considered the environmental sustainability of your project",
              "type": "freeText"
            }
          ],
          "index": 0,
          "question": "How you've considered the environment",
          "status": "COMPLETED"
        },
        {
          "category": null,
          "fields": [
            {
              "answer": true,
              "key": "markAsComplete",
              "title": "Do you want to mark this section as complete?",
              "type": "boolean"
            }
          ],
          "question": "MarkAsComplete",
          "status": "COMPLETED"
        }
      ],
      "status": "COMPLETED"
    },
    {
      "name": "applicant-information-cof",
      "questions": [
        {
          "category": "ZuHuGk",
          "fields": [
            {
              "answer": "test",
              "key": "SnLGJE",
              "title": "Name of lead contact",
              "type": "text"
            },
            {
              "answer": "test",
              "key": "qRDTUc",
              "title": "Lead contact job title",
              "type": "text"
            },
            {
              "answer": "test@test.com",
              "key": "NlHSBg",
              "title": "Lead contact email address",
              "type": "text"
            },
            {
              "answer": "1554323256554",
              "key": "FhBkJQ",
              "title": "Lead contact telephone number",
              "type": "text"
            }
          ],
          "index": 0,
          "question": "Lead contact details",
          "status": "COMPLETED"
        },
        {
          "category": null,
          "fields": [
            {
              "answer": true,
              "key": "markAsComplete",
              "title": "Do you want to mark this section as complete?",
              "type": "boolean"
            }
          ],
          "question": "MarkAsComplete",
          "status": "COMPLETED"
        }
      ],
      "status": "COMPLETED"
    },
    {
      "name": "local-support-cof",
      "questions": [
        {
          "category": "apkBSm",
          "fields": [
            {
              "answer": "<p>test</p>",
              "key": "tDVPnl",
              "title": "Tell us about the local support for your project",
              "type": "freeText"
            },
            {
              "answer": null,
              "key": "bDWjTN",
              "title": "Upload supporting evidence (optional)",
              "type": "text"
            }
          ],
          "index": 0,
          "question": "Your support for the project",
          "status": "COMPLETED"
        },
        {
          "category": null,
          "fields": [
            {
              "answer": true,
              "key": "markAsComplete",
              "title": "Do you want to mark this section as complete?",
              "type": "boolean"
            }
          ],
          "question": "MarkAsComplete",
          "status": "COMPLETED"
        }
      ],
      "status": "COMPLETED"
    },
    {
      "name": "risk-cof",
      "questions": [
        {
          "category": "HKdODf",
          "fields": [
            {
              "answer": "TestDoc.docx",
              "key": "EODncR",
              "title": "Risks to your project (document upload)",
              "type": "text"
            }
          ],
          "index": 0,
          "question": "Your project risk register",
          "status": "COMPLETED"
        },
        {
          "category": null,
          "fields": [
            {
              "answer": true,
              "key": "markAsComplete",
              "title": "Do you want to mark this section as complete?",
              "type": "boolean"
            }
          ],
          "question": "MarkAsComplete",
          "status": "COMPLETED"
        }
      ],
      "status": "COMPLETED"
    },
    {
      "name": "upload-business-plan-cof",
      "questions": [
        {
          "category": "xtwqlH",
          "fields": [
            {
              "answer": "TestDoc.docx",
              "key": "ndpQJk",
              "title": "Upload business plan",
              "type": "text"
            }
          ],
          "index": 0,
          "question": "Your business plan",
          "status": "COMPLETED"
        },
        {
          "category": null,
          "fields": [
            {
              "answer": true,
              "key": "markAsComplete",
              "title": "Do you want to mark this section as complete?",
              "type": "boolean"
            }
          ],
          "question": "MarkAsComplete",
          "status": "COMPLETED"
        }
      ],
      "status": "COMPLETED"
    },
    {
      "name": "organisation-information-cof",
      "questions": [
        {
          "category": "JBqDtK",
          "fields": [
            {
              "answer": "45634564",
              "key": "WWWWxy",
              "title": "Your unique tracker number",
              "type": "text"
            },
            {
              "answer": "Test",
              "key": "YdtlQZ",
              "title": "Organisation name",
              "type": "text"
            },
            {
              "answer": true,
              "key": "iBCGxY",
              "title": "Does your organisation use any other names?",
              "type": "list"
            }
          ],
          "index": 0,
          "question": "Organisation names",
          "status": "COMPLETED"
        },
        {
          "category": "JBqDtK",
          "fields": [
            {
              "answer": "Test",
              "key": "PHFkCs",
              "title": "Alternative names of your organisation",
              "type": "text"
            },
            {
              "answer": null,
              "key": "QgNhXX",
              "title": "Alternative names of your organisation - Alternative name 2 ",
              "type": "text"
            },
            {
              "answer": null,
              "key": "XCcqae",
              "title": "Alternative names of your organisation - Alternative name 3 ",
              "type": "text"
            }
          ],
          "index": 0,
          "question": "Alternative names of your organisation",
          "status": "COMPLETED"
        },
        {
          "category": "JBqDtK",
          "fields": [
            {
              "answer": "<p>Test</p>",
              "key": "emVGxS",
              "title": "What is your organisation's main purpose?",
              "type": "freeText"
            },
            {
              "answer": "<p>test</p>",
              "key": "btTtIb",
              "title": "Tell us about your organisation's main activities",
              "type": "freeText"
            },
            {
              "answer": "<p>test</p>",
              "key": "SkocDi",
              "title": "Tell us about your organisation's main activities - Activity 2 ",
              "type": "freeText"
            },
            {
              "answer": "<p>test</p>",
              "key": "CNeeiC",
              "title": "Tell us about your organisation's main activities - Activity 3 ",
              "type": "freeText"
            },
            {
              "answer": true,
              "key": "BBlCko",
              "title": "Have you delivered projects like this before?",
              "type": "list"
            }
          ],
          "index": 0,
          "question": "Purpose and activities",
          "status": "COMPLETED"
        },
        {
          "category": "JBqDtK",
          "fields": [
            {
              "answer": "<p>test</p>",
              "key": "wxCszQ",
              "title": "Describe your previous projects",
              "type": "freeText"
            },
            {
              "answer": "<p>test</p>",
              "key": "QJFQgi",
              "title": "Describe your previous projects - Project 2 ",
              "type": "freeText"
            },
            {
              "answer": null,
              "key": "DGNWqE",
              "title": "Describe your previous projects - Project 3 ",
              "type": "freeText"
            }
          ],
          "index": 0,
          "question": "Previous projects similar to this one",
          "status": "COMPLETED"
        },
        {
          "category": "JBqDtK",
          "fields": [
            {
              "answer": "CIO",
              "key": "lajFtB",
              "title": "Type of organisation",
              "type": "list"
            }
          ],
          "index": 0,
          "question": "How your organisation is classified",
          "status": "COMPLETED"
        },
        {
          "category": "JBqDtK",
          "fields": [
            {
              "answer": "786786",
              "key": "aHIGbK",
              "title": "Charity number ",
              "type": "text"
            }
          ],
          "index": 0,
          "question": "Charity registration details",
          "status": "COMPLETED"
        },
        {
          "category": "JBqDtK",
          "fields": [
            {
              "answer": false,
              "key": "DwfHtk",
              "title": "Is your organisation a trading subsidiary of a parent company?",
              "type": "list"
            }
          ],
          "index": 0,
          "question": "Trading subsidiaries",
          "status": "COMPLETED"
        },
        {
          "category": "JBqDtK",
          "fields": [
            {
              "answer": "test, test, test, test, ss12ss",
              "key": "ZQolYb",
              "title": "Organisation address",
              "type": "text"
            },
            {
              "answer": true,
              "key": "zsoLdf",
              "title": "Is your correspondence address different to the organisation address?",
              "type": "list"
            },
            {
              "answer": "https://www.google.com",
              "key": "FhbaEy",
              "title": "Website and social media",
              "type": "text"
            },
            {
              "answer": null,
              "key": "FcdKlB",
              "title": "Website and social media - Link or username 2",
              "type": "text"
            },
            {
              "answer": null,
              "key": "BzxgDA",
              "title": "Website and social media - Link or username 3",
              "type": "text"
            }
          ],
          "index": 0,
          "question": "Organisation address",
          "status": "COMPLETED"
        },
        {
          "category": "JBqDtK",
          "fields": [
            {
              "answer": "Test, test, test, test, ss12ss",
              "key": "VhkCbM",
              "title": "Correspondence address",
              "type": "text"
            }
          ],
          "index": 0,
          "question": "Correspondence address",
          "status": "COMPLETED"
        },
        {
          "category": "JBqDtK",
          "fields": [
            {
              "answer": false,
              "key": "hnLurH",
              "title": "Is your application a joint bid in partnership with other organisations?",
              "type": "list"
            }
          ],
          "index": 0,
          "question": "Joint applications",
          "status": "COMPLETED"
        },
        {
          "category": null,
          "fields": [
            {
              "answer": true,
              "key": "markAsComplete",
              "title": "Do you want to mark this section as complete?",
              "type": "boolean"
            }
          ],
          "question": "MarkAsComplete",
          "status": "COMPLETED"
        }
      ],
      "status": "COMPLETED"
    },
    {
      "name": "asset-information-cof",
      "questions": [
        {
          "category": "wxYZcT",
          "fields": [
            {
              "answer": "community-centre",
              "key": "oXGwlA",
              "title": "Asset type",
              "type": "list"
            }
          ],
          "index": 0,
          "question": "How the asset is used in the community",
          "status": "COMPLETED"
        },
        {
          "category": "wxYZcT",
          "fields": [
            {
              "answer": "buy-the-asset",
              "key": "LaxeJN",
              "title": "How do you intend to take community ownership of the asset?",
              "type": "list"
            }
          ],
          "index": 0,
          "question": "The asset in community ownership",
          "status": "COMPLETED"
        },
        {
          "category": "wxYZcT",
          "fields": [
            {
              "answer": "TestDoc.docx",
              "key": "tTOrEp",
              "title": "Please upload evidence that shows the asset valuation (if you are buying the asset) or the lease agreement (if you are leasing the asset).",
              "type": "text"
            }
          ],
          "index": 0,
          "question": "Upload asset valuation or lease agreement",
          "status": "COMPLETED"
        },
        {
          "category": "wxYZcT",
          "fields": [
            {
              "answer": false,
              "key": "wAUFqr",
              "title": "Do you know who currently owns your asset?",
              "type": "list"
            }
          ],
          "index": 0,
          "question": "Who owns the asset",
          "status": "COMPLETED"
        },
        {
          "category": "wxYZcT",
          "fields": [
            {
              "answer": "test",
              "key": "XiHjDO",
              "title": "Tell us what you know about the sale or lease of the asset",
              "type": "text"
            }
          ],
          "index": 0,
          "question": "Current ownership status",
          "status": "COMPLETED"
        },
        {
          "category": "wxYZcT",
          "fields": [
            {
              "answer": "<p>test</p>",
              "key": "XPcbJx",
              "title": "Describe the expected sale process, or the proposed terms of your lease if you are planning to rent the asset",
              "type": "freeText"
            },
            {
              "answer": "2020-12-11",
              "key": "jGjScT",
              "title": "Expected date of sale or lease",
              "type": "date"
            }
          ],
          "index": 0,
          "question": "Expected terms of your ownership or lease",
          "status": "COMPLETED"
        },
        {
          "category": "wxYZcT",
          "fields": [
            {
              "answer": false,
              "key": "VGXXyq",
              "title": "Is your asset currently publicly owned?",
              "type": "list"
            }
          ],
          "index": 0,
          "question": "Public ownership",
          "status": "COMPLETED"
        },
        {
          "category": "wxYZcT",
          "fields": [
            {
              "answer": [
                "Closure"
              ],
              "key": "qlqyUq",
              "title": "Why is the asset at risk of closure?",
              "type": "list"
            }
          ],
          "index": 0,
          "question": "Risk of closure",
          "status": "COMPLETED"
        },
        {
          "category": "wxYZcT",
          "fields": [
            {
              "answer": false,
              "key": "iqnlTk",
              "title": "Is this a registered Asset of Community Value (ACV)?",
              "type": "list"
            }
          ],
          "index": 0,
          "question": "Assets of community value",
          "status": "COMPLETED"
        },
        {
          "category": "wxYZcT",
          "fields": [
            {
              "answer": true,
              "key": "mZwrmI",
              "title": "Are there assets or services of a similar type available locally?",
              "type": "list"
            }
          ],
          "index": 0,
          "question": "Local service provision",
          "status": "COMPLETED"
        },
        {
          "category": "wxYZcT",
          "fields": [
            {
              "answer": true,
              "key": "BfgLCc",
              "title": "Is your asset different from what is available locally?",
              "type": "list"
            }
          ],
          "index": 0,
          "question": "Local service provision",
          "status": "COMPLETED"
        },
        {
          "category": "wxYZcT",
          "fields": [
            {
              "answer": "<p>test</p>",
              "key": "WTZoVD",
              "title": "Tell us how and why your asset or the service is different",
              "type": "freeText"
            }
          ],
          "index": 0,
          "question": "Local service provision",
          "status": "COMPLETED"
        },
        {
          "category": "wxYZcT",
          "fields": [
            {
              "answer": "<p>test</p>",
              "key": "GEJNWF",
              "title": "How accessible is the closest asset or service?",
              "type": "freeText"
            }
          ],
          "index": 0,
          "question": "Local service provision",
          "status": "COMPLETED"
        },
        {
          "category": "wxYZcT",
          "fields": [
            {
              "answer": true,
              "key": "CFFsxV",
              "title": "Does part of your project include a commercial aspect?",
              "type": "list"
            }
          ],
          "index": 0,
          "question": "Local service provision",
          "status": "COMPLETED"
        },
        {
          "category": "wxYZcT",
          "fields": [
            {
              "answer": "<p>test</p>",
              "key": "FDZQTQ",
              "title": "Tell us how the commercial aspect relates to the other services you provide",
              "type": "freeText"
            }
          ],
          "index": 0,
          "question": "Local service provision",
          "status": "COMPLETED"
        },
        {
          "category": null,
          "fields": [
            {
              "answer": true,
              "key": "markAsComplete",
              "title": "Do you want to mark this section as complete?",
              "type": "boolean"
            }
          ],
          "question": "MarkAsComplete",
          "status": "COMPLETED"
        }
      ],
      "status": "COMPLETED"
    },
    {
      "name": "project-information-cof",
      "questions": [
        {
          "category": "qsnIGd",
          "fields": [
            {
              "answer": false,
              "key": "pWwCRM",
              "title": "Have you applied to the Community Ownership Fund before?",
              "type": "list"
            }
          ],
          "index": 0,
          "question": "Previous Community Ownership Fund applications",
          "status": "COMPLETED"
        },
        {
          "category": "qsnIGd",
          "fields": [
            {
              "answer": "Test Project",
              "key": "apGjFS",
              "title": "Project name",
              "type": "text"
            },
            {
              "answer": "<p>test</p>",
              "key": "bEWpAj",
              "title": "Tell us how the asset is currently being used, or how it has been used before, and why it's important to the community",
              "type": "freeText"
            },
            {
              "answer": "<p>test</p>",
              "key": "uypCNM",
              "title": "Give a brief summary of your project, including what you hope to achieve",
              "type": "freeText"
            },
            {
              "answer": "<p>test</p>",
              "key": "AgeRbd",
              "title": "Tell us about the planned activities and/or services that will take place in the asset",
              "type": "freeText"
            }
          ],
          "index": 0,
          "question": "Project name and summary",
          "status": "COMPLETED"
        },
        {
          "category": "qsnIGd",
          "fields": [
            {
              "answer": "test, test, test, test, ss12ss",
              "key": "EfdliG",
              "title": "Address of the community asset",
              "type": "text"
            },
            {
              "answer": "test",
              "key": "fIEUcb",
              "title": " In which constituency is your asset?",
              "type": "text"
            },
            {
              "answer": "test",
              "key": "SWfcTo",
              "title": "In which local council area is your asset?",
              "type": "text"
            }
          ],
          "index": 0,
          "question": "Address of the asset",
          "status": "COMPLETED"
        },
        {
          "category": null,
          "fields": [
            {
              "answer": true,
              "key": "markAsComplete",
              "title": "Do you want to mark this section as complete?",
              "type": "boolean"
            }
          ],
          "question": "MarkAsComplete",
          "status": "COMPLETED"
        }
      ],
      "status": "COMPLETED"
    },
    {
      "name": "community-engagement-cof",
      "questions": [
        {
          "category": "lmdhVN",
          "fields": [
            {
              "answer": "<p>test</p>",
              "key": "azCutK",
              "title": "Tell us how you have engaged with the community about your intention to take ownership of the asset",
              "type": "freeText"
            }
          ],
          "index": 0,
          "question": "How you've engaged with the community",
          "status": "COMPLETED"
        },
        {
          "category": "lmdhVN",
          "fields": [
            {
              "answer": "<p>test</p>",
              "key": "jAhuWN",
              "title": "Describe your fundraising activities",
              "type": "freeText"
            }
          ],
          "index": 0,
          "question": "Your fundraising activities",
          "status": "COMPLETED"
        },
        {
          "category": "lmdhVN",
          "fields": [
            {
              "answer": "<p>test</p>",
              "key": "HYsezC",
              "title": "Tell us about any partnerships you've formed, and how they'll help the project be successful",
              "type": "freeText"
            },
            {
              "answer": "<p>test</p>",
              "key": "GGBgBY",
              "title": "Tell us how your project supports any wider local plans",
              "type": "freeText"
            }
          ],
          "index": 0,
          "question": "Partnerships and local plans",
          "status": "COMPLETED"
        },
        {
          "category": null,
          "fields": [
            {
              "answer": true,
              "key": "markAsComplete",
              "title": "Do you want to mark this section as complete?",
              "type": "boolean"
            }
          ],
          "question": "MarkAsComplete",
          "status": "COMPLETED"
        }
      ],
      "status": "COMPLETED"
    },
    {
      "name": "declarations-cof",
      "questions": [
        {
          "category": "LkvizC",
          "fields": [
            {
              "answer": true,
              "key": "vSQKwD",
              "title": "Confirm you have considered subsidy control and state aid implications for your project, and the information you have given us is correct",
              "type": "list"
            },
            {
              "answer": true,
              "key": "CQoLFp",
              "title": "Confirm you have considered people with protected characteristics throughout the planning of your project",
              "type": "list"
            },
            {
              "answer": true,
              "key": "jdPkiX",
              "title": "Confirm you have considered sustainability and the environment throughout the planning of your project, including compliance with the government's Net Zero ambitions",
              "type": "list"
            },
            {
              "answer": true,
              "key": "qWuSCy",
              "title": "Confirm you have a bank account set up and associated with the organisation you are applying on behalf of",
              "type": "list"
            },
            {
              "answer": true,
              "key": "tjZlml",
              "title": "Confirm that the information you've provided in this application is accurate to the best of your knowledge on the date of submission",
              "type": "list"
            }
          ],
          "index": 0,
          "question": "Agree to the final confirmations",
          "status": "COMPLETED"
        },
        {
          "category": null,
          "fields": [
            {
              "answer": true,
              "key": "markAsComplete",
              "title": "Do you want to mark this section as complete?",
              "type": "boolean"
            }
          ],
          "question": "MarkAsComplete",
          "status": "COMPLETED"
        }
      ],
      "status": "COMPLETED"
    },
    {
      "name": "community-benefits-cof",
      "questions": [
        {
          "category": "PTOBPV",
          "fields": [
            {
              "answer": [
                "community-pride"
              ],
              "key": "pqYxJO",
              "title": "What community benefits do you expect to deliver with this project?",
              "type": "list"
            },
            {
              "answer": "<p>test</p>",
              "key": "lgfiGB",
              "title": "Tell us about these benefits in detail, and how the asset's activities will help deliver them",
              "type": "freeText"
            },
            {
              "answer": "<p>test</p>",
              "key": "zKKouR",
              "title": "Explain how you plan to deliver and sustain these benefits over time",
              "type": "freeText"
            },
            {
              "answer": "<p>test</p>",
              "key": "ZyIQGI",
              "title": "Tell us how you'll make sure the whole community benefits from the asset",
              "type": "freeText"
            }
          ],
          "index": 0,
          "question": "Benefits you'll deliver",
          "status": "COMPLETED"
        },
        {
          "category": null,
          "fields": [
            {
              "answer": true,
              "key": "markAsComplete",
              "title": "Do you want to mark this section as complete?",
              "type": "boolean"
            }
          ],
          "question": "MarkAsComplete",
          "status": "COMPLETED"
        }
      ],
      "status": "COMPLETED"
    },
    {
      "name": "funding-required-cof",
      "questions": [
        {
          "category": "bgUGuD",
          "fields": [
            {
              "answer": "966585",
              "key": "ABROnB",
              "title": "Capital funding request",
              "type": "text"
            },
            {
              "answer": false,
              "key": "hJkmBS",
              "title": "If successful, will you use your funding in the next 12 months?",
              "type": "list"
            }
          ],
          "index": 0,
          "question": "Capital funding request",
          "status": "COMPLETED"
        },
        {
          "category": "bgUGuD",
          "fields": [
            {
              "answer": [
                {
                  "GLQlOh": "test",
                  "JtwkMy": 542,
                  "LeTLDo": 456,
                  "pHZDWT": 45654
                }
              ],
              "key": "qQLyXL",
              "title": "Capital costs",
              "type": "multiInput"
            }
          ],
          "index": 0,
          "question": "Capital costs for your project",
          "status": "COMPLETED"
        },
        {
          "category": "bgUGuD",
          "fields": [
            {
              "answer": false,
              "key": "DOvZvB",
              "title": "Have you secured any match funding yet?",
              "type": "list"
            }
          ],
          "index": 0,
          "question": "If you've secured match funding",
          "status": "COMPLETED"
        },
        {
          "category": "bgUGuD",
          "fields": [
            {
              "answer": [
                {
                  "THOdae": 41242,
                  "iMJdfs": "test"
                }
              ],
              "key": "vEOdBS",
              "title": "Unsecured match funding",
              "type": "multiInput"
            }
          ],
          "index": 0,
          "question": "Unsecured match funding",
          "status": "COMPLETED"
        },
        {
          "category": "bgUGuD",
          "fields": [
            {
              "answer": false,
              "key": "matkNH",
              "title": "Are you applying for revenue funding from the Community Ownership Fund? (optional)",
              "type": "list"
            }
          ],
          "index": 0,
          "question": "Revenue funding",
          "status": "COMPLETED"
        },
        {
          "category": null,
          "fields": [
            {
              "answer": true,
              "key": "markAsComplete",
              "title": "Do you want to mark this section as complete?",
              "type": "boolean"
            }
          ],
          "question": "MarkAsComplete",
          "status": "COMPLETED"
        }
      ],
      "status": "COMPLETED"
    },
    {
      "name": "feasibility-cof",
      "questions": [
        {
          "category": "bBGnkL",
          "fields": [
            {
              "answer": "<p>test</p>",
              "key": "iSbwDM",
              "title": "Tell us about the feasibility studies you have carried out for your project",
              "type": "freeText"
            },
            {
              "answer": false,
              "key": "jFPlEJ",
              "title": "Do you need to do any further feasibility work?",
              "type": "list"
            }
          ],
          "index": 0,
          "question": "Feasiblity studies you've carried out",
          "status": "COMPLETED"
        },
        {
          "category": null,
          "fields": [
            {
              "answer": true,
              "key": "markAsComplete",
              "title": "Do you want to mark this section as complete?",
              "type": "boolean"
            }
          ],
          "question": "MarkAsComplete",
          "status": "COMPLETED"
        }
      ],
      "status": "COMPLETED"
    },
    {
      "name": "operational-costs-cof",
      "questions": [
        {
          "category": "oSfXFZ",
          "fields": [
            {
              "answer": "<p><strong>test</strong></p>",
              "key": "qXNkfr",
              "title": "Summarise your income and operational costs for the running of the asset",
              "type": "freeText"
            }
          ],
          "index": 0,
          "question": "Forecasted income and operational costs to run the asset",
          "status": "COMPLETED"
        },
        {
          "category": null,
          "fields": [
            {
              "answer": true,
              "key": "markAsComplete",
              "title": "Do you want to mark this section as complete?",
              "type": "boolean"
            }
          ],
          "question": "MarkAsComplete",
          "status": "COMPLETED"
        }
      ],
      "status": "COMPLETED"
    },
    {
      "name": "community-representation-cof",
      "questions": [
        {
          "category": "KbnmOO",
          "fields": [
            {
              "answer": "<p>test</p>",
              "key": "ReomFo",
              "title": "List the members of your board",
              "type": "freeText"
            },
            {
              "answer": "<p>test</p>",
              "key": "fjVmOt",
              "title": "Tell us about your governance and membership structures",
              "type": "freeText"
            },
            {
              "answer": "<ol>\\r\\n<li>test</li>\\r\\n</ol>",
              "key": "GETNxN",
              "title": "Explain how you'll consider the views of the community in the running of the asset",
              "type": "freeText"
            }
          ],
          "index": 0,
          "question": "How you’ll run the asset",
          "status": "COMPLETED"
        },
        {
          "category": null,
          "fields": [
            {
              "answer": true,
              "key": "markAsComplete",
              "title": "Do you want to mark this section as complete?",
              "type": "boolean"
            }
          ],
          "question": "MarkAsComplete",
          "status": "COMPLETED"
        }
      ],
      "status": "COMPLETED"
    },
    {
      "name": "inclusiveness-and-integration-cof",
      "questions": [
        {
          "category": "eCZBSV",
          "fields": [
            {
              "answer": "<p>test</p>",
              "key": "mgIesb",
              "title": "Tell us how the asset will be accountable to local people, and involve them in its running",
              "type": "freeText"
            },
            {
              "answer": "<p>test</p>",
              "key": "lQEkep",
              "title": "Describe anything that might prevent people from using the asset or participating in its running",
              "type": "freeText"
            }
          ],
          "index": 0,
          "question": "How you’ll make the asset inclusive",
          "status": "COMPLETED"
        },
        {
          "category": null,
          "fields": [
            {
              "answer": true,
              "key": "markAsComplete",
              "title": "Do you want to mark this section as complete?",
              "type": "boolean"
            }
          ],
          "question": "MarkAsComplete",
          "status": "COMPLETED"
        }
      ],
      "status": "COMPLETED"
    },
    {
      "name": "skills-and-resources-cof",
      "questions": [
        {
          "category": "eLpYFr",
          "fields": [
            {
              "answer": "<p>test</p>",
              "key": "XXGyzn",
              "title": "Describe any relevant experience you have delivering similar projects or running an asset",
              "type": "freeText"
            }
          ],
          "index": 0,
          "question": "Your experience running similar assets",
          "status": "COMPLETED"
        },
        {
          "category": "eLpYFr",
          "fields": [
            {
              "answer": false,
              "key": "Uaeyae",
              "title": "Do you have plans to recruit people to help you run the asset?",
              "type": "list"
            }
          ],
          "index": 0,
          "question": "Recruitment plans",
          "status": "COMPLETED"
        },
        {
          "category": null,
          "fields": [
            {
              "answer": true,
              "key": "markAsComplete",
              "title": "Do you want to mark this section as complete?",
              "type": "boolean"
            }
          ],
          "question": "MarkAsComplete",
          "status": "COMPLETED"
        }
      ],
      "status": "COMPLETED"
    }
  ]
  }
"""
)

cofr3w3_application_store_json_template = Template(
    """
    {
    "id": "$app_id",
    "language": "en",
    "fund_id": "$fund_id",
    "last_edited": "2023-09-04T15:54:15.234643",
    "project_name": "$project_name",
    "reference": "$short_ref",
    "round_id": "$round_id",
    "round_name": "Round 3 Window 2",
    "started_at": "2023-09-04T15:48:57.567040",
    "status": "SUBMITTED",
    "account_id": "1e8884e2-b043-427f-ba09-7ec2ca409ef0",
    "date_submitted": "2023-09-04T15:54:30.373564",
    "forms": [
    {
      "name": "community-use-cof",
      "questions": [
        {
          "category": "GMkooI",
          "fields": [
            {
              "answer": "<p>test</p>",
              "key": "zTcrYo",
              "title": "Who in the community currently uses the asset, or has used it in the past?",
              "type": "freeText"
            },
            {
              "answer": "<p>test</p>",
              "key": "whlRYS",
              "title": "Tell us how losing the asset would affect, or has already affected, people in the community",
              "type": "freeText"
            },
            {
              "answer": "<p>test</p>",
              "key": "NGSXHE",
              "title": "Why will the asset be lost without community intervention?",
              "type": "freeText"
            },
            {
              "answer": "<p>test</p>",
              "key": "Ieudgn",
              "title": "Explain how the community will be better served with the asset under community ownership",
              "type": "freeText"
            }
          ],
          "index": 0,
          "question": "Who uses the asset",
          "status": "COMPLETED"
        },
        {
          "category": null,
          "fields": [
            {
              "answer": true,
              "key": "markAsComplete",
              "title": "Do you want to mark this section as complete?",
              "type": "boolean"
            }
          ],
          "question": "MarkAsComplete",
          "status": "COMPLETED"
        }
      ],
      "status": "COMPLETED"
    },
    {
      "name": "environmental-sustainability-cof",
      "questions": [
        {
          "category": "ljcxPd",
          "fields": [
            {
              "answer": "<p>test</p>",
              "key": "dypuJs",
              "title": "Tell us how you have considered the environmental sustainability of your project",
              "type": "freeText"
            }
          ],
          "index": 0,
          "question": "How you've considered the environment",
          "status": "COMPLETED"
        },
        {
          "category": null,
          "fields": [
            {
              "answer": true,
              "key": "markAsComplete",
              "title": "Do you want to mark this section as complete?",
              "type": "boolean"
            }
          ],
          "question": "MarkAsComplete",
          "status": "COMPLETED"
        }
      ],
      "status": "COMPLETED"
    },
    {
      "name": "applicant-information-cof",
      "questions": [
        {
          "category": "ZuHuGk",
          "fields": [
            {
              "answer": "test",
              "key": "SnLGJE",
              "title": "Name of lead contact",
              "type": "text"
            },
            {
              "answer": "test",
              "key": "qRDTUc",
              "title": "Lead contact job title",
              "type": "text"
            },
            {
              "answer": "test@test.com",
              "key": "NlHSBg",
              "title": "Lead contact email address",
              "type": "text"
            },
            {
              "answer": "1554323256554",
              "key": "FhBkJQ",
              "title": "Lead contact telephone number",
              "type": "text"
            }
          ],
          "index": 0,
          "question": "Lead contact details",
          "status": "COMPLETED"
        },
        {
          "category": null,
          "fields": [
            {
              "answer": true,
              "key": "markAsComplete",
              "title": "Do you want to mark this section as complete?",
              "type": "boolean"
            }
          ],
          "question": "MarkAsComplete",
          "status": "COMPLETED"
        }
      ],
      "status": "COMPLETED"
    },
    {
      "name": "local-support-cof",
      "questions": [
        {
          "category": "apkBSm",
          "fields": [
            {
              "answer": "<p>test</p>",
              "key": "tDVPnl",
              "title": "Tell us about the local support for your project",
              "type": "freeText"
            },
            {
              "answer": null,
              "key": "bDWjTN",
              "title": "Upload supporting evidence (optional)",
              "type": "text"
            }
          ],
          "index": 0,
          "question": "Your support for the project",
          "status": "COMPLETED"
        },
        {
          "category": null,
          "fields": [
            {
              "answer": true,
              "key": "markAsComplete",
              "title": "Do you want to mark this section as complete?",
              "type": "boolean"
            }
          ],
          "question": "MarkAsComplete",
          "status": "COMPLETED"
        }
      ],
      "status": "COMPLETED"
    },
    {
      "name": "risk-cof",
      "questions": [
        {
          "category": "HKdODf",
          "fields": [
            {
              "answer": "TestDoc.docx",
              "key": "EODncR",
              "title": "Risks to your project (document upload)",
              "type": "text"
            }
          ],
          "index": 0,
          "question": "Your project risk register",
          "status": "COMPLETED"
        },
        {
          "category": null,
          "fields": [
            {
              "answer": true,
              "key": "markAsComplete",
              "title": "Do you want to mark this section as complete?",
              "type": "boolean"
            }
          ],
          "question": "MarkAsComplete",
          "status": "COMPLETED"
        }
      ],
      "status": "COMPLETED"
    },
    {
      "name": "upload-business-plan-cof",
      "questions": [
        {
          "category": "xtwqlH",
          "fields": [
            {
              "answer": "TestDoc.docx",
              "key": "ndpQJk",
              "title": "Upload business plan",
              "type": "text"
            }
          ],
          "index": 0,
          "question": "Your business plan",
          "status": "COMPLETED"
        },
        {
          "category": null,
          "fields": [
            {
              "answer": true,
              "key": "markAsComplete",
              "title": "Do you want to mark this section as complete?",
              "type": "boolean"
            }
          ],
          "question": "MarkAsComplete",
          "status": "COMPLETED"
        }
      ],
      "status": "COMPLETED"
    },
    {
      "name": "organisation-information-cof",
      "questions": [
        {
          "category": "JBqDtK",
          "fields": [
            {
              "answer": "45634564",
              "key": "WWWWxy",
              "title": "Your unique tracker number",
              "type": "text"
            },
            {
              "answer": "Test",
              "key": "YdtlQZ",
              "title": "Organisation name",
              "type": "text"
            },
            {
              "answer": true,
              "key": "iBCGxY",
              "title": "Does your organisation use any other names?",
              "type": "list"
            }
          ],
          "index": 0,
          "question": "Organisation names",
          "status": "COMPLETED"
        },
        {
          "category": "JBqDtK",
          "fields": [
            {
              "answer": "Test",
              "key": "PHFkCs",
              "title": "Alternative names of your organisation",
              "type": "text"
            },
            {
              "answer": null,
              "key": "QgNhXX",
              "title": "Alternative names of your organisation - Alternative name 2 ",
              "type": "text"
            },
            {
              "answer": null,
              "key": "XCcqae",
              "title": "Alternative names of your organisation - Alternative name 3 ",
              "type": "text"
            }
          ],
          "index": 0,
          "question": "Alternative names of your organisation",
          "status": "COMPLETED"
        },
        {
          "category": "JBqDtK",
          "fields": [
            {
              "answer": "<p>Test</p>",
              "key": "emVGxS",
              "title": "What is your organisation's main purpose?",
              "type": "freeText"
            },
            {
              "answer": "<p>test</p>",
              "key": "btTtIb",
              "title": "Tell us about your organisation's main activities",
              "type": "freeText"
            },
            {
              "answer": "<p>test</p>",
              "key": "SkocDi",
              "title": "Tell us about your organisation's main activities - Activity 2 ",
              "type": "freeText"
            },
            {
              "answer": "<p>test</p>",
              "key": "CNeeiC",
              "title": "Tell us about your organisation's main activities - Activity 3 ",
              "type": "freeText"
            },
            {
              "answer": true,
              "key": "BBlCko",
              "title": "Have you delivered projects like this before?",
              "type": "list"
            }
          ],
          "index": 0,
          "question": "Purpose and activities",
          "status": "COMPLETED"
        },
        {
          "category": "JBqDtK",
          "fields": [
            {
              "answer": "<p>test</p>",
              "key": "wxCszQ",
              "title": "Describe your previous projects",
              "type": "freeText"
            },
            {
              "answer": "<p>test</p>",
              "key": "QJFQgi",
              "title": "Describe your previous projects - Project 2 ",
              "type": "freeText"
            },
            {
              "answer": null,
              "key": "DGNWqE",
              "title": "Describe your previous projects - Project 3 ",
              "type": "freeText"
            }
          ],
          "index": 0,
          "question": "Previous projects similar to this one",
          "status": "COMPLETED"
        },
        {
          "category": "JBqDtK",
          "fields": [
            {
              "answer": "CIO",
              "key": "lajFtB",
              "title": "Type of organisation",
              "type": "list"
            }
          ],
          "index": 0,
          "question": "How your organisation is classified",
          "status": "COMPLETED"
        },
        {
          "category": "JBqDtK",
          "fields": [
            {
              "answer": "786786",
              "key": "aHIGbK",
              "title": "Charity number ",
              "type": "text"
            }
          ],
          "index": 0,
          "question": "Charity registration details",
          "status": "COMPLETED"
        },
        {
          "category": "JBqDtK",
          "fields": [
            {
              "answer": false,
              "key": "DwfHtk",
              "title": "Is your organisation a trading subsidiary of a parent company?",
              "type": "list"
            }
          ],
          "index": 0,
          "question": "Trading subsidiaries",
          "status": "COMPLETED"
        },
        {
          "category": "JBqDtK",
          "fields": [
            {
              "answer": "test, test, test, test, ss12ss",
              "key": "ZQolYb",
              "title": "Organisation address",
              "type": "text"
            },
            {
              "answer": true,
              "key": "zsoLdf",
              "title": "Is your correspondence address different to the organisation address?",
              "type": "list"
            },
            {
              "answer": "https://www.google.com",
              "key": "FhbaEy",
              "title": "Website and social media",
              "type": "text"
            },
            {
              "answer": null,
              "key": "FcdKlB",
              "title": "Website and social media - Link or username 2",
              "type": "text"
            },
            {
              "answer": null,
              "key": "BzxgDA",
              "title": "Website and social media - Link or username 3",
              "type": "text"
            }
          ],
          "index": 0,
          "question": "Organisation address",
          "status": "COMPLETED"
        },
        {
          "category": "JBqDtK",
          "fields": [
            {
              "answer": "Test, test, test, test, ss12ss",
              "key": "VhkCbM",
              "title": "Correspondence address",
              "type": "text"
            }
          ],
          "index": 0,
          "question": "Correspondence address",
          "status": "COMPLETED"
        },
        {
          "category": "JBqDtK",
          "fields": [
            {
              "answer": false,
              "key": "hnLurH",
              "title": "Is your application a joint bid in partnership with other organisations?",
              "type": "list"
            }
          ],
          "index": 0,
          "question": "Joint applications",
          "status": "COMPLETED"
        },
        {
          "category": null,
          "fields": [
            {
              "answer": true,
              "key": "markAsComplete",
              "title": "Do you want to mark this section as complete?",
              "type": "boolean"
            }
          ],
          "question": "MarkAsComplete",
          "status": "COMPLETED"
        }
      ],
      "status": "COMPLETED"
    },
    {
      "name": "asset-information-cof",
      "questions": [
        {
          "category": "wxYZcT",
          "fields": [
            {
              "answer": "community-centre",
              "key": "oXGwlA",
              "title": "Asset type",
              "type": "list"
            }
          ],
          "index": 0,
          "question": "How the asset is used in the community",
          "status": "COMPLETED"
        },
        {
          "category": "wxYZcT",
          "fields": [
            {
              "answer": "buy-the-asset",
              "key": "LaxeJN",
              "title": "How do you intend to take community ownership of the asset?",
              "type": "list"
            }
          ],
          "index": 0,
          "question": "The asset in community ownership",
          "status": "COMPLETED"
        },
        {
          "category": "wxYZcT",
          "fields": [
            {
              "answer": "TestDoc.docx",
              "key": "tTOrEp",
              "title": "Please upload evidence that shows the asset valuation (if you are buying the asset) or the lease agreement (if you are leasing the asset).",
              "type": "text"
            }
          ],
          "index": 0,
          "question": "Upload asset valuation or lease agreement",
          "status": "COMPLETED"
        },
        {
          "category": "wxYZcT",
          "fields": [
            {
              "answer": false,
              "key": "wAUFqr",
              "title": "Do you know who currently owns your asset?",
              "type": "list"
            }
          ],
          "index": 0,
          "question": "Who owns the asset",
          "status": "COMPLETED"
        },
        {
          "category": "wxYZcT",
          "fields": [
            {
              "answer": "test",
              "key": "XiHjDO",
              "title": "Tell us what you know about the sale or lease of the asset",
              "type": "text"
            }
          ],
          "index": 0,
          "question": "Current ownership status",
          "status": "COMPLETED"
        },
        {
          "category": "wxYZcT",
          "fields": [
            {
              "answer": "<p>test</p>",
              "key": "XPcbJx",
              "title": "Describe the expected sale process, or the proposed terms of your lease if you are planning to rent the asset",
              "type": "freeText"
            },
            {
              "answer": "2020-12-11",
              "key": "jGjScT",
              "title": "Expected date of sale or lease",
              "type": "date"
            }
          ],
          "index": 0,
          "question": "Expected terms of your ownership or lease",
          "status": "COMPLETED"
        },
        {
          "category": "wxYZcT",
          "fields": [
            {
              "answer": false,
              "key": "VGXXyq",
              "title": "Is your asset currently publicly owned?",
              "type": "list"
            }
          ],
          "index": 0,
          "question": "Public ownership",
          "status": "COMPLETED"
        },
        {
          "category": "wxYZcT",
          "fields": [
            {
              "answer": [
                "Closure"
              ],
              "key": "qlqyUq",
              "title": "Why is the asset at risk of closure?",
              "type": "list"
            }
          ],
          "index": 0,
          "question": "Risk of closure",
          "status": "COMPLETED"
        },
        {
          "category": "wxYZcT",
          "fields": [
            {
              "answer": false,
              "key": "iqnlTk",
              "title": "Is this a registered Asset of Community Value (ACV)?",
              "type": "list"
            }
          ],
          "index": 0,
          "question": "Assets of community value",
          "status": "COMPLETED"
        },
        {
          "category": "wxYZcT",
          "fields": [
            {
              "answer": true,
              "key": "mZwrmI",
              "title": "Are there assets or services of a similar type available locally?",
              "type": "list"
            }
          ],
          "index": 0,
          "question": "Local service provision",
          "status": "COMPLETED"
        },
        {
          "category": "wxYZcT",
          "fields": [
            {
              "answer": true,
              "key": "BfgLCc",
              "title": "Is your asset different from what is available locally?",
              "type": "list"
            }
          ],
          "index": 0,
          "question": "Local service provision",
          "status": "COMPLETED"
        },
        {
          "category": "wxYZcT",
          "fields": [
            {
              "answer": "<p>test</p>",
              "key": "WTZoVD",
              "title": "Tell us how and why your asset or the service is different",
              "type": "freeText"
            }
          ],
          "index": 0,
          "question": "Local service provision",
          "status": "COMPLETED"
        },
        {
          "category": "wxYZcT",
          "fields": [
            {
              "answer": "<p>test</p>",
              "key": "GEJNWF",
              "title": "How accessible is the closest asset or service?",
              "type": "freeText"
            }
          ],
          "index": 0,
          "question": "Local service provision",
          "status": "COMPLETED"
        },
        {
          "category": "wxYZcT",
          "fields": [
            {
              "answer": true,
              "key": "CFFsxV",
              "title": "Does part of your project include a commercial aspect?",
              "type": "list"
            }
          ],
          "index": 0,
          "question": "Local service provision",
          "status": "COMPLETED"
        },
        {
          "category": "wxYZcT",
          "fields": [
            {
              "answer": "<p>test</p>",
              "key": "FDZQTQ",
              "title": "Tell us how the commercial aspect relates to the other services you provide",
              "type": "freeText"
            }
          ],
          "index": 0,
          "question": "Local service provision",
          "status": "COMPLETED"
        },
        {
          "category": null,
          "fields": [
            {
              "answer": true,
              "key": "markAsComplete",
              "title": "Do you want to mark this section as complete?",
              "type": "boolean"
            }
          ],
          "question": "MarkAsComplete",
          "status": "COMPLETED"
        }
      ],
      "status": "COMPLETED"
    },
    {
      "name": "project-information-cof",
      "questions": [
        {
          "category": "qsnIGd",
          "fields": [
            {
              "answer": false,
              "key": "pWwCRM",
              "title": "Have you applied to the Community Ownership Fund before?",
              "type": "list"
            }
          ],
          "index": 0,
          "question": "Previous Community Ownership Fund applications",
          "status": "COMPLETED"
        },
        {
          "category": "qsnIGd",
          "fields": [
            {
              "answer": "Test Project",
              "key": "apGjFS",
              "title": "Project name",
              "type": "text"
            },
            {
              "answer": "<p>test</p>",
              "key": "bEWpAj",
              "title": "Tell us how the asset is currently being used, or how it has been used before, and why it's important to the community",
              "type": "freeText"
            },
            {
              "answer": "<p>test</p>",
              "key": "uypCNM",
              "title": "Give a brief summary of your project, including what you hope to achieve",
              "type": "freeText"
            },
            {
              "answer": "<p>test</p>",
              "key": "AgeRbd",
              "title": "Tell us about the planned activities and/or services that will take place in the asset",
              "type": "freeText"
            }
          ],
          "index": 0,
          "question": "Project name and summary",
          "status": "COMPLETED"
        },
        {
          "category": "qsnIGd",
          "fields": [
            {
              "answer": "test, test, test, test, ss12ss",
              "key": "EfdliG",
              "title": "Address of the community asset",
              "type": "text"
            },
            {
              "answer": "test",
              "key": "fIEUcb",
              "title": " In which constituency is your asset?",
              "type": "text"
            },
            {
              "answer": "test",
              "key": "SWfcTo",
              "title": "In which local council area is your asset?",
              "type": "text"
            }
          ],
          "index": 0,
          "question": "Address of the asset",
          "status": "COMPLETED"
        },
        {
          "category": null,
          "fields": [
            {
              "answer": true,
              "key": "markAsComplete",
              "title": "Do you want to mark this section as complete?",
              "type": "boolean"
            }
          ],
          "question": "MarkAsComplete",
          "status": "COMPLETED"
        }
      ],
      "status": "COMPLETED"
    },
    {
      "name": "community-engagement-cof",
      "questions": [
        {
          "category": "lmdhVN",
          "fields": [
            {
              "answer": "<p>test</p>",
              "key": "azCutK",
              "title": "Tell us how you have engaged with the community about your intention to take ownership of the asset",
              "type": "freeText"
            }
          ],
          "index": 0,
          "question": "How you've engaged with the community",
          "status": "COMPLETED"
        },
        {
          "category": "lmdhVN",
          "fields": [
            {
              "answer": "<p>test</p>",
              "key": "jAhuWN",
              "title": "Describe your fundraising activities",
              "type": "freeText"
            }
          ],
          "index": 0,
          "question": "Your fundraising activities",
          "status": "COMPLETED"
        },
        {
          "category": "lmdhVN",
          "fields": [
            {
              "answer": "<p>test</p>",
              "key": "HYsezC",
              "title": "Tell us about any partnerships you've formed, and how they'll help the project be successful",
              "type": "freeText"
            },
            {
              "answer": "<p>test</p>",
              "key": "GGBgBY",
              "title": "Tell us how your project supports any wider local plans",
              "type": "freeText"
            }
          ],
          "index": 0,
          "question": "Partnerships and local plans",
          "status": "COMPLETED"
        },
        {
          "category": null,
          "fields": [
            {
              "answer": true,
              "key": "markAsComplete",
              "title": "Do you want to mark this section as complete?",
              "type": "boolean"
            }
          ],
          "question": "MarkAsComplete",
          "status": "COMPLETED"
        }
      ],
      "status": "COMPLETED"
    },
    {
      "name": "declarations-cof",
      "questions": [
        {
          "category": "LkvizC",
          "fields": [
            {
              "answer": true,
              "key": "vSQKwD",
              "title": "Confirm you have considered subsidy control and state aid implications for your project, and the information you have given us is correct",
              "type": "list"
            },
            {
              "answer": true,
              "key": "CQoLFp",
              "title": "Confirm you have considered people with protected characteristics throughout the planning of your project",
              "type": "list"
            },
            {
              "answer": true,
              "key": "jdPkiX",
              "title": "Confirm you have considered sustainability and the environment throughout the planning of your project, including compliance with the government's Net Zero ambitions",
              "type": "list"
            },
            {
              "answer": true,
              "key": "qWuSCy",
              "title": "Confirm you have a bank account set up and associated with the organisation you are applying on behalf of",
              "type": "list"
            },
            {
              "answer": true,
              "key": "tjZlml",
              "title": "Confirm that the information you've provided in this application is accurate to the best of your knowledge on the date of submission",
              "type": "list"
            }
          ],
          "index": 0,
          "question": "Agree to the final confirmations",
          "status": "COMPLETED"
        },
        {
          "category": null,
          "fields": [
            {
              "answer": true,
              "key": "markAsComplete",
              "title": "Do you want to mark this section as complete?",
              "type": "boolean"
            }
          ],
          "question": "MarkAsComplete",
          "status": "COMPLETED"
        }
      ],
      "status": "COMPLETED"
    },
    {
      "name": "community-benefits-cof",
      "questions": [
        {
          "category": "PTOBPV",
          "fields": [
            {
              "answer": [
                "community-pride"
              ],
              "key": "pqYxJO",
              "title": "What community benefits do you expect to deliver with this project?",
              "type": "list"
            },
            {
              "answer": "<p>test</p>",
              "key": "lgfiGB",
              "title": "Tell us about these benefits in detail, and how the asset's activities will help deliver them",
              "type": "freeText"
            },
            {
              "answer": "<p>test</p>",
              "key": "zKKouR",
              "title": "Explain how you plan to deliver and sustain these benefits over time",
              "type": "freeText"
            },
            {
              "answer": "<p>test</p>",
              "key": "ZyIQGI",
              "title": "Tell us how you'll make sure the whole community benefits from the asset",
              "type": "freeText"
            }
          ],
          "index": 0,
          "question": "Benefits you'll deliver",
          "status": "COMPLETED"
        },
        {
          "category": null,
          "fields": [
            {
              "answer": true,
              "key": "markAsComplete",
              "title": "Do you want to mark this section as complete?",
              "type": "boolean"
            }
          ],
          "question": "MarkAsComplete",
          "status": "COMPLETED"
        }
      ],
      "status": "COMPLETED"
    },
    {
      "name": "funding-required-cof",
      "questions": [
        {
          "category": "bgUGuD",
          "fields": [
            {
              "answer": "966585",
              "key": "ABROnB",
              "title": "Capital funding request",
              "type": "text"
            },
            {
              "answer": false,
              "key": "hJkmBS",
              "title": "If successful, will you use your funding in the next 12 months?",
              "type": "list"
            }
          ],
          "index": 0,
          "question": "Capital funding request",
          "status": "COMPLETED"
        },
        {
          "category": "bgUGuD",
          "fields": [
            {
              "answer": [
                {
                  "GLQlOh": "test",
                  "JtwkMy": 542,
                  "LeTLDo": 456,
                  "pHZDWT": 45654
                }
              ],
              "key": "qQLyXL",
              "title": "Capital costs",
              "type": "multiInput"
            }
          ],
          "index": 0,
          "question": "Capital costs for your project",
          "status": "COMPLETED"
        },
        {
          "category": "bgUGuD",
          "fields": [
            {
              "answer": false,
              "key": "DOvZvB",
              "title": "Have you secured any match funding yet?",
              "type": "list"
            }
          ],
          "index": 0,
          "question": "If you've secured match funding",
          "status": "COMPLETED"
        },
        {
          "category": "bgUGuD",
          "fields": [
            {
              "answer": [
                {
                  "THOdae": 41242,
                  "iMJdfs": "test"
                }
              ],
              "key": "vEOdBS",
              "title": "Unsecured match funding",
              "type": "multiInput"
            }
          ],
          "index": 0,
          "question": "Unsecured match funding",
          "status": "COMPLETED"
        },
        {
          "category": "bgUGuD",
          "fields": [
            {
              "answer": false,
              "key": "matkNH",
              "title": "Are you applying for revenue funding from the Community Ownership Fund? (optional)",
              "type": "list"
            }
          ],
          "index": 0,
          "question": "Revenue funding",
          "status": "COMPLETED"
        },
        {
          "category": null,
          "fields": [
            {
              "answer": true,
              "key": "markAsComplete",
              "title": "Do you want to mark this section as complete?",
              "type": "boolean"
            }
          ],
          "question": "MarkAsComplete",
          "status": "COMPLETED"
        }
      ],
      "status": "COMPLETED"
    },
    {
      "name": "feasibility-cof",
      "questions": [
        {
          "category": "bBGnkL",
          "fields": [
            {
              "answer": "<p>test</p>",
              "key": "iSbwDM",
              "title": "Tell us about the feasibility studies you have carried out for your project",
              "type": "freeText"
            },
            {
              "answer": false,
              "key": "jFPlEJ",
              "title": "Do you need to do any further feasibility work?",
              "type": "list"
            }
          ],
          "index": 0,
          "question": "Feasiblity studies you've carried out",
          "status": "COMPLETED"
        },
        {
          "category": null,
          "fields": [
            {
              "answer": true,
              "key": "markAsComplete",
              "title": "Do you want to mark this section as complete?",
              "type": "boolean"
            }
          ],
          "question": "MarkAsComplete",
          "status": "COMPLETED"
        }
      ],
      "status": "COMPLETED"
    },
    {
      "name": "operational-costs-cof",
      "questions": [
        {
          "category": "oSfXFZ",
          "fields": [
            {
              "answer": "<p><strong>test</strong></p>",
              "key": "qXNkfr",
              "title": "Summarise your income and operational costs for the running of the asset",
              "type": "freeText"
            }
          ],
          "index": 0,
          "question": "Forecasted income and operational costs to run the asset",
          "status": "COMPLETED"
        },
        {
          "category": null,
          "fields": [
            {
              "answer": true,
              "key": "markAsComplete",
              "title": "Do you want to mark this section as complete?",
              "type": "boolean"
            }
          ],
          "question": "MarkAsComplete",
          "status": "COMPLETED"
        }
      ],
      "status": "COMPLETED"
    },
    {
      "name": "community-representation-cof",
      "questions": [
        {
          "category": "KbnmOO",
          "fields": [
            {
              "answer": "<p>test</p>",
              "key": "ReomFo",
              "title": "List the members of your board",
              "type": "freeText"
            },
            {
              "answer": "<p>test</p>",
              "key": "fjVmOt",
              "title": "Tell us about your governance and membership structures",
              "type": "freeText"
            },
            {
              "answer": "<ol>\\r\\n<li>test</li>\\r\\n</ol>",
              "key": "GETNxN",
              "title": "Explain how you'll consider the views of the community in the running of the asset",
              "type": "freeText"
            }
          ],
          "index": 0,
          "question": "How you’ll run the asset",
          "status": "COMPLETED"
        },
        {
          "category": null,
          "fields": [
            {
              "answer": true,
              "key": "markAsComplete",
              "title": "Do you want to mark this section as complete?",
              "type": "boolean"
            }
          ],
          "question": "MarkAsComplete",
          "status": "COMPLETED"
        }
      ],
      "status": "COMPLETED"
    },
    {
      "name": "inclusiveness-and-integration-cof",
      "questions": [
        {
          "category": "eCZBSV",
          "fields": [
            {
              "answer": "<p>test</p>",
              "key": "mgIesb",
              "title": "Tell us how the asset will be accountable to local people, and involve them in its running",
              "type": "freeText"
            },
            {
              "answer": "<p>test</p>",
              "key": "lQEkep",
              "title": "Describe anything that might prevent people from using the asset or participating in its running",
              "type": "freeText"
            }
          ],
          "index": 0,
          "question": "How you’ll make the asset inclusive",
          "status": "COMPLETED"
        },
        {
          "category": null,
          "fields": [
            {
              "answer": true,
              "key": "markAsComplete",
              "title": "Do you want to mark this section as complete?",
              "type": "boolean"
            }
          ],
          "question": "MarkAsComplete",
          "status": "COMPLETED"
        }
      ],
      "status": "COMPLETED"
    },
    {
      "name": "skills-and-resources-cof",
      "questions": [
        {
          "category": "eLpYFr",
          "fields": [
            {
              "answer": "<p>test</p>",
              "key": "XXGyzn",
              "title": "Describe any relevant experience you have delivering similar projects or running an asset",
              "type": "freeText"
            }
          ],
          "index": 0,
          "question": "Your experience running similar assets",
          "status": "COMPLETED"
        },
        {
          "category": "eLpYFr",
          "fields": [
            {
              "answer": false,
              "key": "Uaeyae",
              "title": "Do you have plans to recruit people to help you run the asset?",
              "type": "list"
            }
          ],
          "index": 0,
          "question": "Recruitment plans",
          "status": "COMPLETED"
        },
        {
          "category": null,
          "fields": [
            {
              "answer": true,
              "key": "markAsComplete",
              "title": "Do you want to mark this section as complete?",
              "type": "boolean"
            }
          ],
          "question": "MarkAsComplete",
          "status": "COMPLETED"
        }
      ],
      "status": "COMPLETED"
    }
  ]
  }
"""
)
cofr4w1_application_store_json_template = Template(
    """
    {
    "id": "$app_id",
    "language": "en",
    "fund_id": "$fund_id",
    "last_edited": "2024-01-04T15:54:15.234643",
    "project_name": "$project_name",
    "reference": "$short_ref",
    "round_id": "$round_id",
    "round_name": "Round 4 Window 4",
    "started_at": "2024-01-04T15:48:57.567040",
    "status": "SUBMITTED",
    "account_id": "1e8884e2-b043-427f-ba09-7ec2ca409ef0",
    "date_submitted": "2024-01-04T15:54:30.373564",
    "forms": [
    {
      "name": "community-use-cof",
      "questions": [
        {
          "category": "GMkooI",
          "fields": [
            {
              "answer": "<p>test</p>",
              "key": "zTcrYo",
              "title": "Who in the community currently uses the asset, or has used it in the past?",
              "type": "freeText"
            },
            {
              "answer": "<p>test</p>",
              "key": "whlRYS",
              "title": "Tell us how losing the asset would affect, or has already affected, people in the community",
              "type": "freeText"
            },
            {
              "answer": "<p>test</p>",
              "key": "NGSXHE",
              "title": "Why will the asset be lost without community intervention?",
              "type": "freeText"
            },
            {
              "answer": "<p>test</p>",
              "key": "Ieudgn",
              "title": "Explain how the community will be better served with the asset under community ownership",
              "type": "freeText"
            }
          ],
          "index": 0,
          "question": "Who uses the asset",
          "status": "COMPLETED"
        },
        {
          "category": null,
          "fields": [
            {
              "answer": true,
              "key": "markAsComplete",
              "title": "Do you want to mark this section as complete?",
              "type": "boolean"
            }
          ],
          "question": "MarkAsComplete",
          "status": "COMPLETED"
        }
      ],
      "status": "COMPLETED"
    },
    {
      "name": "environmental-sustainability-cof",
      "questions": [
        {
          "category": "ljcxPd",
          "fields": [
            {
              "answer": "<p>test</p>",
              "key": "dypuJs",
              "title": "Tell us how you have considered the environmental sustainability of your project",
              "type": "freeText"
            }
          ],
          "index": 0,
          "question": "How you've considered the environment",
          "status": "COMPLETED"
        },
        {
          "category": null,
          "fields": [
            {
              "answer": true,
              "key": "markAsComplete",
              "title": "Do you want to mark this section as complete?",
              "type": "boolean"
            }
          ],
          "question": "MarkAsComplete",
          "status": "COMPLETED"
        }
      ],
      "status": "COMPLETED"
    },
    {
      "name": "applicant-information-cof",
      "questions": [
        {
          "category": "ZuHuGk",
          "fields": [
            {
              "answer": "test",
              "key": "SnLGJE",
              "title": "Name of lead contact",
              "type": "text"
            },
            {
              "answer": "test",
              "key": "qRDTUc",
              "title": "Lead contact job title",
              "type": "text"
            },
            {
              "answer": "test@test.com",
              "key": "NlHSBg",
              "title": "Lead contact email address",
              "type": "text"
            },
            {
              "answer": "1554323256554",
              "key": "FhBkJQ",
              "title": "Lead contact telephone number",
              "type": "text"
            }
          ],
          "index": 0,
          "question": "Lead contact details",
          "status": "COMPLETED"
        },
        {
          "category": null,
          "fields": [
            {
              "answer": true,
              "key": "markAsComplete",
              "title": "Do you want to mark this section as complete?",
              "type": "boolean"
            }
          ],
          "question": "MarkAsComplete",
          "status": "COMPLETED"
        }
      ],
      "status": "COMPLETED"
    },
    {
      "name": "local-support-cof",
      "questions": [
        {
          "category": "apkBSm",
          "fields": [
            {
              "answer": "<p>test</p>",
              "key": "tDVPnl",
              "title": "Tell us about the local support for your project",
              "type": "freeText"
            },
            {
              "answer": null,
              "key": "bDWjTN",
              "title": "Upload supporting evidence (optional)",
              "type": "text"
            }
          ],
          "index": 0,
          "question": "Your support for the project",
          "status": "COMPLETED"
        },
        {
          "category": null,
          "fields": [
            {
              "answer": true,
              "key": "markAsComplete",
              "title": "Do you want to mark this section as complete?",
              "type": "boolean"
            }
          ],
          "question": "MarkAsComplete",
          "status": "COMPLETED"
        }
      ],
      "status": "COMPLETED"
    },
    {
      "name": "risk-cof",
      "questions": [
        {
          "category": "HKdODf",
          "fields": [
            {
              "answer": "TestDoc.docx",
              "key": "EODncR",
              "title": "Risks to your project (document upload)",
              "type": "text"
            }
          ],
          "index": 0,
          "question": "Your project risk register",
          "status": "COMPLETED"
        },
        {
          "category": null,
          "fields": [
            {
              "answer": true,
              "key": "markAsComplete",
              "title": "Do you want to mark this section as complete?",
              "type": "boolean"
            }
          ],
          "question": "MarkAsComplete",
          "status": "COMPLETED"
        }
      ],
      "status": "COMPLETED"
    },
    {
      "name": "upload-business-plan-cof",
      "questions": [
        {
          "category": "xtwqlH",
          "fields": [
            {
              "answer": "TestDoc.docx",
              "key": "ndpQJk",
              "title": "Upload business plan",
              "type": "text"
            }
          ],
          "index": 0,
          "question": "Your business plan",
          "status": "COMPLETED"
        },
        {
          "category": null,
          "fields": [
            {
              "answer": true,
              "key": "markAsComplete",
              "title": "Do you want to mark this section as complete?",
              "type": "boolean"
            }
          ],
          "question": "MarkAsComplete",
          "status": "COMPLETED"
        }
      ],
      "status": "COMPLETED"
    },
    {
      "name": "organisation-information-cof",
      "questions": [
        {
          "category": "JBqDtK",
          "fields": [
            {
              "answer": "45634564",
              "key": "WWWWxy",
              "title": "Your unique tracker number",
              "type": "text"
            },
            {
              "answer": "Test",
              "key": "YdtlQZ",
              "title": "Organisation name",
              "type": "text"
            },
            {
              "answer": true,
              "key": "iBCGxY",
              "title": "Does your organisation use any other names?",
              "type": "list"
            }
          ],
          "index": 0,
          "question": "Organisation names",
          "status": "COMPLETED"
        },
        {
          "category": "JBqDtK",
          "fields": [
            {
              "answer": "Test",
              "key": "PHFkCs",
              "title": "Alternative names of your organisation",
              "type": "text"
            },
            {
              "answer": null,
              "key": "QgNhXX",
              "title": "Alternative names of your organisation - Alternative name 2 ",
              "type": "text"
            },
            {
              "answer": null,
              "key": "XCcqae",
              "title": "Alternative names of your organisation - Alternative name 3 ",
              "type": "text"
            }
          ],
          "index": 0,
          "question": "Alternative names of your organisation",
          "status": "COMPLETED"
        },
        {
          "category": "JBqDtK",
          "fields": [
            {
              "answer": "<p>Test</p>",
              "key": "emVGxS",
              "title": "What is your organisation's main purpose?",
              "type": "freeText"
            },
            {
              "answer": "<p>test</p>",
              "key": "btTtIb",
              "title": "Tell us about your organisation's main activities",
              "type": "freeText"
            },
            {
              "answer": "<p>test</p>",
              "key": "SkocDi",
              "title": "Tell us about your organisation's main activities - Activity 2 ",
              "type": "freeText"
            },
            {
              "answer": "<p>test</p>",
              "key": "CNeeiC",
              "title": "Tell us about your organisation's main activities - Activity 3 ",
              "type": "freeText"
            },
            {
              "answer": true,
              "key": "BBlCko",
              "title": "Have you delivered projects like this before?",
              "type": "list"
            }
          ],
          "index": 0,
          "question": "Purpose and activities",
          "status": "COMPLETED"
        },
        {
          "category": "JBqDtK",
          "fields": [
            {
              "answer": "<p>test</p>",
              "key": "wxCszQ",
              "title": "Describe your previous projects",
              "type": "freeText"
            },
            {
              "answer": "<p>test</p>",
              "key": "QJFQgi",
              "title": "Describe your previous projects - Project 2 ",
              "type": "freeText"
            },
            {
              "answer": null,
              "key": "DGNWqE",
              "title": "Describe your previous projects - Project 3 ",
              "type": "freeText"
            }
          ],
          "index": 0,
          "question": "Previous projects similar to this one",
          "status": "COMPLETED"
        },
        {
          "category": "JBqDtK",
          "fields": [
            {
              "answer": "CIO",
              "key": "lajFtB",
              "title": "Type of organisation",
              "type": "list"
            }
          ],
          "index": 0,
          "question": "How your organisation is classified",
          "status": "COMPLETED"
        },
        {
          "category": "JBqDtK",
          "fields": [
            {
              "answer": "786786",
              "key": "aHIGbK",
              "title": "Charity number ",
              "type": "text"
            }
          ],
          "index": 0,
          "question": "Charity registration details",
          "status": "COMPLETED"
        },
        {
          "category": "JBqDtK",
          "fields": [
            {
              "answer": false,
              "key": "DwfHtk",
              "title": "Is your organisation a trading subsidiary of a parent company?",
              "type": "list"
            }
          ],
          "index": 0,
          "question": "Trading subsidiaries",
          "status": "COMPLETED"
        },
        {
          "category": "JBqDtK",
          "fields": [
            {
              "answer": "test, test, test, test, ss12ss",
              "key": "ZQolYb",
              "title": "Organisation address",
              "type": "text"
            },
            {
              "answer": true,
              "key": "zsoLdf",
              "title": "Is your correspondence address different to the organisation address?",
              "type": "list"
            },
            {
              "answer": "https://www.google.com",
              "key": "FhbaEy",
              "title": "Website and social media",
              "type": "text"
            },
            {
              "answer": null,
              "key": "FcdKlB",
              "title": "Website and social media - Link or username 2",
              "type": "text"
            },
            {
              "answer": null,
              "key": "BzxgDA",
              "title": "Website and social media - Link or username 3",
              "type": "text"
            }
          ],
          "index": 0,
          "question": "Organisation address",
          "status": "COMPLETED"
        },
        {
          "category": "JBqDtK",
          "fields": [
            {
              "answer": "Test, test, test, test, ss12ss",
              "key": "VhkCbM",
              "title": "Correspondence address",
              "type": "text"
            }
          ],
          "index": 0,
          "question": "Correspondence address",
          "status": "COMPLETED"
        },
        {
          "category": "JBqDtK",
          "fields": [
            {
              "answer": false,
              "key": "hnLurH",
              "title": "Is your application a joint bid in partnership with other organisations?",
              "type": "list"
            }
          ],
          "index": 0,
          "question": "Joint applications",
          "status": "COMPLETED"
        },
        {
          "category": null,
          "fields": [
            {
              "answer": true,
              "key": "markAsComplete",
              "title": "Do you want to mark this section as complete?",
              "type": "boolean"
            }
          ],
          "question": "MarkAsComplete",
          "status": "COMPLETED"
        }
      ],
      "status": "COMPLETED"
    },
    {
      "name": "asset-information-cof",
      "questions": [
        {
          "category": "wxYZcT",
          "fields": [
            {
              "answer": "community-centre",
              "key": "oXGwlA",
              "title": "Asset type",
              "type": "list"
            }
          ],
          "index": 0,
          "question": "How the asset is used in the community",
          "status": "COMPLETED"
        },
        {
          "category": "wxYZcT",
          "fields": [
            {
              "answer": "buy-the-asset",
              "key": "LaxeJN",
              "title": "How do you intend to take community ownership of the asset?",
              "type": "list"
            }
          ],
          "index": 0,
          "question": "The asset in community ownership",
          "status": "COMPLETED"
        },
        {
          "category": "wxYZcT",
          "fields": [
            {
              "answer": "TestDoc.docx",
              "key": "tTOrEp",
              "title": "Please upload evidence that shows the asset valuation (if you are buying the asset) or the lease agreement (if you are leasing the asset).",
              "type": "text"
            }
          ],
          "index": 0,
          "question": "Upload asset valuation or lease agreement",
          "status": "COMPLETED"
        },
        {
          "category": "wxYZcT",
          "fields": [
            {
              "answer": false,
              "key": "wAUFqr",
              "title": "Do you know who currently owns your asset?",
              "type": "list"
            }
          ],
          "index": 0,
          "question": "Who owns the asset",
          "status": "COMPLETED"
        },
        {
          "category": "wxYZcT",
          "fields": [
            {
              "answer": "test",
              "key": "XiHjDO",
              "title": "Tell us what you know about the sale or lease of the asset",
              "type": "text"
            }
          ],
          "index": 0,
          "question": "Current ownership status",
          "status": "COMPLETED"
        },
        {
          "category": "wxYZcT",
          "fields": [
            {
              "answer": "<p>test</p>",
              "key": "XPcbJx",
              "title": "Describe the expected sale process, or the proposed terms of your lease if you are planning to rent the asset",
              "type": "freeText"
            },
            {
              "answer": "2020-12-11",
              "key": "jGjScT",
              "title": "Expected date of sale or lease",
              "type": "date"
            }
          ],
          "index": 0,
          "question": "Expected terms of your ownership or lease",
          "status": "COMPLETED"
        },
        {
          "category": "wxYZcT",
          "fields": [
            {
              "answer": false,
              "key": "VGXXyq",
              "title": "Is your asset currently publicly owned?",
              "type": "list"
            }
          ],
          "index": 0,
          "question": "Public ownership",
          "status": "COMPLETED"
        },
        {
          "category": "wxYZcT",
          "fields": [
            {
              "answer": [
                "Closure"
              ],
              "key": "qlqyUq",
              "title": "Why is the asset at risk of closure?",
              "type": "list"
            }
          ],
          "index": 0,
          "question": "Risk of closure",
          "status": "COMPLETED"
        },
        {
          "category": "wxYZcT",
          "fields": [
            {
              "answer": false,
              "key": "iqnlTk",
              "title": "Is this a registered Asset of Community Value (ACV)?",
              "type": "list"
            }
          ],
          "index": 0,
          "question": "Assets of community value",
          "status": "COMPLETED"
        },
        {
          "category": "wxYZcT",
          "fields": [
            {
              "answer": true,
              "key": "mZwrmI",
              "title": "Are there assets or services of a similar type available locally?",
              "type": "list"
            }
          ],
          "index": 0,
          "question": "Local service provision",
          "status": "COMPLETED"
        },
        {
          "category": "wxYZcT",
          "fields": [
            {
              "answer": true,
              "key": "BfgLCc",
              "title": "Is your asset different from what is available locally?",
              "type": "list"
            }
          ],
          "index": 0,
          "question": "Local service provision",
          "status": "COMPLETED"
        },
        {
          "category": "wxYZcT",
          "fields": [
            {
              "answer": "<p>test</p>",
              "key": "WTZoVD",
              "title": "Tell us how and why your asset or the service is different",
              "type": "freeText"
            }
          ],
          "index": 0,
          "question": "Local service provision",
          "status": "COMPLETED"
        },
        {
          "category": "wxYZcT",
          "fields": [
            {
              "answer": "<p>test</p>",
              "key": "GEJNWF",
              "title": "How accessible is the closest asset or service?",
              "type": "freeText"
            }
          ],
          "index": 0,
          "question": "Local service provision",
          "status": "COMPLETED"
        },
        {
          "category": "wxYZcT",
          "fields": [
            {
              "answer": true,
              "key": "CFFsxV",
              "title": "Does part of your project include a commercial aspect?",
              "type": "list"
            }
          ],
          "index": 0,
          "question": "Local service provision",
          "status": "COMPLETED"
        },
        {
          "category": "wxYZcT",
          "fields": [
            {
              "answer": "<p>test</p>",
              "key": "FDZQTQ",
              "title": "Tell us how the commercial aspect relates to the other services you provide",
              "type": "freeText"
            }
          ],
          "index": 0,
          "question": "Local service provision",
          "status": "COMPLETED"
        },
        {
          "category": null,
          "fields": [
            {
              "answer": true,
              "key": "markAsComplete",
              "title": "Do you want to mark this section as complete?",
              "type": "boolean"
            }
          ],
          "question": "MarkAsComplete",
          "status": "COMPLETED"
        }
      ],
      "status": "COMPLETED"
    },
    {
      "name": "project-information-cof",
      "questions": [
        {
          "category": "qsnIGd",
          "fields": [
            {
              "answer": false,
              "key": "pWwCRM",
              "title": "Have you applied to the Community Ownership Fund before?",
              "type": "list"
            }
          ],
          "index": 0,
          "question": "Previous Community Ownership Fund applications",
          "status": "COMPLETED"
        },
        {
          "category": "qsnIGd",
          "fields": [
            {
              "answer": "Test Project",
              "key": "apGjFS",
              "title": "Project name",
              "type": "text"
            },
            {
              "answer": "<p>test</p>",
              "key": "bEWpAj",
              "title": "Tell us how the asset is currently being used, or how it has been used before, and why it's important to the community",
              "type": "freeText"
            },
            {
              "answer": "<p>test</p>",
              "key": "uypCNM",
              "title": "Give a brief summary of your project, including what you hope to achieve",
              "type": "freeText"
            },
            {
              "answer": "<p>test</p>",
              "key": "AgeRbd",
              "title": "Tell us about the planned activities and/or services that will take place in the asset",
              "type": "freeText"
            }
          ],
          "index": 0,
          "question": "Project name and summary",
          "status": "COMPLETED"
        },
        {
          "category": "qsnIGd",
          "fields": [
            {
              "answer": "test, test, test, test, ss12ss",
              "key": "EfdliG",
              "title": "Address of the community asset",
              "type": "text"
            },
            {
              "answer": "test",
              "key": "fIEUcb",
              "title": " In which constituency is your asset?",
              "type": "text"
            },
            {
              "answer": "test",
              "key": "SWfcTo",
              "title": "In which local council area is your asset?",
              "type": "text"
            }
          ],
          "index": 0,
          "question": "Address of the asset",
          "status": "COMPLETED"
        },
        {
          "category": null,
          "fields": [
            {
              "answer": true,
              "key": "markAsComplete",
              "title": "Do you want to mark this section as complete?",
              "type": "boolean"
            }
          ],
          "question": "MarkAsComplete",
          "status": "COMPLETED"
        }
      ],
      "status": "COMPLETED"
    },
    {
      "name": "community-engagement-cof",
      "questions": [
        {
          "category": "lmdhVN",
          "fields": [
            {
              "answer": "<p>test</p>",
              "key": "azCutK",
              "title": "Tell us how you have engaged with the community about your intention to take ownership of the asset",
              "type": "freeText"
            }
          ],
          "index": 0,
          "question": "How you've engaged with the community",
          "status": "COMPLETED"
        },
        {
          "category": "lmdhVN",
          "fields": [
            {
              "answer": "<p>test</p>",
              "key": "jAhuWN",
              "title": "Describe your fundraising activities",
              "type": "freeText"
            }
          ],
          "index": 0,
          "question": "Your fundraising activities",
          "status": "COMPLETED"
        },
        {
          "category": "lmdhVN",
          "fields": [
            {
              "answer": "<p>test</p>",
              "key": "HYsezC",
              "title": "Tell us about any partnerships you've formed, and how they'll help the project be successful",
              "type": "freeText"
            },
            {
              "answer": "<p>test</p>",
              "key": "GGBgBY",
              "title": "Tell us how your project supports any wider local plans",
              "type": "freeText"
            }
          ],
          "index": 0,
          "question": "Partnerships and local plans",
          "status": "COMPLETED"
        },
        {
          "category": null,
          "fields": [
            {
              "answer": true,
              "key": "markAsComplete",
              "title": "Do you want to mark this section as complete?",
              "type": "boolean"
            }
          ],
          "question": "MarkAsComplete",
          "status": "COMPLETED"
        }
      ],
      "status": "COMPLETED"
    },
    {
      "name": "declarations-cof",
      "questions": [
        {
          "category": "LkvizC",
          "fields": [
            {
              "answer": true,
              "key": "vSQKwD",
              "title": "Confirm you have considered subsidy control and state aid implications for your project, and the information you have given us is correct",
              "type": "list"
            },
            {
              "answer": true,
              "key": "CQoLFp",
              "title": "Confirm you have considered people with protected characteristics throughout the planning of your project",
              "type": "list"
            },
            {
              "answer": true,
              "key": "jdPkiX",
              "title": "Confirm you have considered sustainability and the environment throughout the planning of your project, including compliance with the government's Net Zero ambitions",
              "type": "list"
            },
            {
              "answer": true,
              "key": "qWuSCy",
              "title": "Confirm you have a bank account set up and associated with the organisation you are applying on behalf of",
              "type": "list"
            },
            {
              "answer": true,
              "key": "tjZlml",
              "title": "Confirm that the information you've provided in this application is accurate to the best of your knowledge on the date of submission",
              "type": "list"
            }
          ],
          "index": 0,
          "question": "Agree to the final confirmations",
          "status": "COMPLETED"
        },
        {
          "category": null,
          "fields": [
            {
              "answer": true,
              "key": "markAsComplete",
              "title": "Do you want to mark this section as complete?",
              "type": "boolean"
            }
          ],
          "question": "MarkAsComplete",
          "status": "COMPLETED"
        }
      ],
      "status": "COMPLETED"
    },
    {
      "name": "community-benefits-cof",
      "questions": [
        {
          "category": "PTOBPV",
          "fields": [
            {
              "answer": [
                "community-pride"
              ],
              "key": "pqYxJO",
              "title": "What community benefits do you expect to deliver with this project?",
              "type": "list"
            },
            {
              "answer": "<p>test</p>",
              "key": "lgfiGB",
              "title": "Tell us about these benefits in detail, and how the asset's activities will help deliver them",
              "type": "freeText"
            },
            {
              "answer": "<p>test</p>",
              "key": "zKKouR",
              "title": "Explain how you plan to deliver and sustain these benefits over time",
              "type": "freeText"
            },
            {
              "answer": "<p>test</p>",
              "key": "ZyIQGI",
              "title": "Tell us how you'll make sure the whole community benefits from the asset",
              "type": "freeText"
            }
          ],
          "index": 0,
          "question": "Benefits you'll deliver",
          "status": "COMPLETED"
        },
        {
          "category": null,
          "fields": [
            {
              "answer": true,
              "key": "markAsComplete",
              "title": "Do you want to mark this section as complete?",
              "type": "boolean"
            }
          ],
          "question": "MarkAsComplete",
          "status": "COMPLETED"
        }
      ],
      "status": "COMPLETED"
    },
    {
      "name": "funding-required-cof",
      "questions": [
        {
          "category": "bgUGuD",
          "fields": [
            {
              "answer": "966585",
              "key": "ABROnB",
              "title": "Capital funding request",
              "type": "text"
            },
            {
              "answer": false,
              "key": "hJkmBS",
              "title": "If successful, will you use your funding in the next 12 months?",
              "type": "list"
            }
          ],
          "index": 0,
          "question": "Capital funding request",
          "status": "COMPLETED"
        },
        {
          "category": "bgUGuD",
          "fields": [
            {
              "answer": [
                {
                  "GLQlOh": "test",
                  "JtwkMy": 542,
                  "LeTLDo": 456,
                  "pHZDWT": 45654
                }
              ],
              "key": "qQLyXL",
              "title": "Capital costs",
              "type": "multiInput"
            }
          ],
          "index": 0,
          "question": "Capital costs for your project",
          "status": "COMPLETED"
        },
        {
          "category": "bgUGuD",
          "fields": [
            {
              "answer": false,
              "key": "DOvZvB",
              "title": "Have you secured any match funding yet?",
              "type": "list"
            }
          ],
          "index": 0,
          "question": "If you've secured match funding",
          "status": "COMPLETED"
        },
        {
          "category": "bgUGuD",
          "fields": [
            {
              "answer": [
                {
                  "THOdae": 41242,
                  "iMJdfs": "test"
                }
              ],
              "key": "vEOdBS",
              "title": "Unsecured match funding",
              "type": "multiInput"
            }
          ],
          "index": 0,
          "question": "Unsecured match funding",
          "status": "COMPLETED"
        },
        {
          "category": "bgUGuD",
          "fields": [
            {
              "answer": false,
              "key": "matkNH",
              "title": "Are you applying for revenue funding from the Community Ownership Fund? (optional)",
              "type": "list"
            }
          ],
          "index": 0,
          "question": "Revenue funding",
          "status": "COMPLETED"
        },
        {
          "category": null,
          "fields": [
            {
              "answer": true,
              "key": "markAsComplete",
              "title": "Do you want to mark this section as complete?",
              "type": "boolean"
            }
          ],
          "question": "MarkAsComplete",
          "status": "COMPLETED"
        }
      ],
      "status": "COMPLETED"
    },
    {
      "name": "feasibility-cof",
      "questions": [
        {
          "category": "bBGnkL",
          "fields": [
            {
              "answer": "<p>test</p>",
              "key": "iSbwDM",
              "title": "Tell us about the feasibility studies you have carried out for your project",
              "type": "freeText"
            },
            {
              "answer": false,
              "key": "jFPlEJ",
              "title": "Do you need to do any further feasibility work?",
              "type": "list"
            }
          ],
          "index": 0,
          "question": "Feasiblity studies you've carried out",
          "status": "COMPLETED"
        },
        {
          "category": null,
          "fields": [
            {
              "answer": true,
              "key": "markAsComplete",
              "title": "Do you want to mark this section as complete?",
              "type": "boolean"
            }
          ],
          "question": "MarkAsComplete",
          "status": "COMPLETED"
        }
      ],
      "status": "COMPLETED"
    },
    {
      "name": "operational-costs-cof",
      "questions": [
        {
          "category": "oSfXFZ",
          "fields": [
            {
              "answer": "<p><strong>test</strong></p>",
              "key": "qXNkfr",
              "title": "Summarise your income and operational costs for the running of the asset",
              "type": "freeText"
            }
          ],
          "index": 0,
          "question": "Forecasted income and operational costs to run the asset",
          "status": "COMPLETED"
        },
        {
          "category": null,
          "fields": [
            {
              "answer": true,
              "key": "markAsComplete",
              "title": "Do you want to mark this section as complete?",
              "type": "boolean"
            }
          ],
          "question": "MarkAsComplete",
          "status": "COMPLETED"
        }
      ],
      "status": "COMPLETED"
    },
    {
      "name": "community-representation-cof",
      "questions": [
        {
          "category": "KbnmOO",
          "fields": [
            {
              "answer": "<p>test</p>",
              "key": "ReomFo",
              "title": "List the members of your board",
              "type": "freeText"
            },
            {
              "answer": "<p>test</p>",
              "key": "fjVmOt",
              "title": "Tell us about your governance and membership structures",
              "type": "freeText"
            },
            {
              "answer": "<ol>\\r\\n<li>test</li>\\r\\n</ol>",
              "key": "GETNxN",
              "title": "Explain how you'll consider the views of the community in the running of the asset",
              "type": "freeText"
            }
          ],
          "index": 0,
          "question": "How you’ll run the asset",
          "status": "COMPLETED"
        },
        {
          "category": null,
          "fields": [
            {
              "answer": true,
              "key": "markAsComplete",
              "title": "Do you want to mark this section as complete?",
              "type": "boolean"
            }
          ],
          "question": "MarkAsComplete",
          "status": "COMPLETED"
        }
      ],
      "status": "COMPLETED"
    },
    {
      "name": "inclusiveness-and-integration-cof",
      "questions": [
        {
          "category": "eCZBSV",
          "fields": [
            {
              "answer": "<p>test</p>",
              "key": "mgIesb",
              "title": "Tell us how the asset will be accountable to local people, and involve them in its running",
              "type": "freeText"
            },
            {
              "answer": "<p>test</p>",
              "key": "lQEkep",
              "title": "Describe anything that might prevent people from using the asset or participating in its running",
              "type": "freeText"
            }
          ],
          "index": 0,
          "question": "How you’ll make the asset inclusive",
          "status": "COMPLETED"
        },
        {
          "category": null,
          "fields": [
            {
              "answer": true,
              "key": "markAsComplete",
              "title": "Do you want to mark this section as complete?",
              "type": "boolean"
            }
          ],
          "question": "MarkAsComplete",
          "status": "COMPLETED"
        }
      ],
      "status": "COMPLETED"
    },
    {
      "name": "skills-and-resources-cof",
      "questions": [
        {
          "category": "eLpYFr",
          "fields": [
            {
              "answer": "<p>test</p>",
              "key": "XXGyzn",
              "title": "Describe any relevant experience you have delivering similar projects or running an asset",
              "type": "freeText"
            }
          ],
          "index": 0,
          "question": "Your experience running similar assets",
          "status": "COMPLETED"
        },
        {
          "category": "eLpYFr",
          "fields": [
            {
              "answer": false,
              "key": "Uaeyae",
              "title": "Do you have plans to recruit people to help you run the asset?",
              "type": "list"
            }
          ],
          "index": 0,
          "question": "Recruitment plans",
          "status": "COMPLETED"
        },
        {
          "category": null,
          "fields": [
            {
              "answer": true,
              "key": "markAsComplete",
              "title": "Do you want to mark this section as complete?",
              "type": "boolean"
            }
          ],
          "question": "MarkAsComplete",
          "status": "COMPLETED"
        }
      ],
      "status": "COMPLETED"
    }
  ]
  }
"""
)

cofr4w2_application_store_json_template = Template(
    """
    {
    "id": "$app_id",
    "language": "en",
    "fund_id": "$fund_id",
    "last_edited": "2024-01-04T15:54:15.234643",
    "project_name": "$project_name",
    "reference": "$short_ref",
    "round_id": "$round_id",
    "round_name": "Round 4 Window 4",
    "started_at": "2024-01-04T15:48:57.567040",
    "status": "SUBMITTED",
    "account_id": "1e8884e2-b043-427f-ba09-7ec2ca409ef0",
    "date_submitted": "2024-01-04T15:54:30.373564",
    "forms": [
    {
      "name": "community-use-cof",
      "questions": [
        {
          "category": "GMkooI",
          "fields": [
            {
              "answer": "<p>test</p>",
              "key": "zTcrYo",
              "title": "Who in the community currently uses the asset, or has used it in the past?",
              "type": "freeText"
            },
            {
              "answer": "<p>test</p>",
              "key": "whlRYS",
              "title": "Tell us how losing the asset would affect, or has already affected, people in the community",
              "type": "freeText"
            },
            {
              "answer": "<p>test</p>",
              "key": "NGSXHE",
              "title": "Why will the asset be lost without community intervention?",
              "type": "freeText"
            },
            {
              "answer": "<p>test</p>",
              "key": "Ieudgn",
              "title": "Explain how the community will be better served with the asset under community ownership",
              "type": "freeText"
            }
          ],
          "index": 0,
          "question": "Who uses the asset",
          "status": "COMPLETED"
        },
        {
          "category": null,
          "fields": [
            {
              "answer": true,
              "key": "markAsComplete",
              "title": "Do you want to mark this section as complete?",
              "type": "boolean"
            }
          ],
          "question": "MarkAsComplete",
          "status": "COMPLETED"
        }
      ],
      "status": "COMPLETED"
    },
    {
      "name": "environmental-sustainability-cof",
      "questions": [
        {
          "category": "ljcxPd",
          "fields": [
            {
              "answer": "<p>test</p>",
              "key": "dypuJs",
              "title": "Tell us how you have considered the environmental sustainability of your project",
              "type": "freeText"
            }
          ],
          "index": 0,
          "question": "How you've considered the environment",
          "status": "COMPLETED"
        },
        {
          "category": null,
          "fields": [
            {
              "answer": true,
              "key": "markAsComplete",
              "title": "Do you want to mark this section as complete?",
              "type": "boolean"
            }
          ],
          "question": "MarkAsComplete",
          "status": "COMPLETED"
        }
      ],
      "status": "COMPLETED"
    },
    {
      "name": "applicant-information-cof",
      "questions": [
        {
          "category": "ZuHuGk",
          "fields": [
            {
              "answer": "test",
              "key": "SnLGJE",
              "title": "Name of lead contact",
              "type": "text"
            },
            {
              "answer": "test",
              "key": "qRDTUc",
              "title": "Lead contact job title",
              "type": "text"
            },
            {
              "answer": "test@test.com",
              "key": "NlHSBg",
              "title": "Lead contact email address",
              "type": "text"
            },
            {
              "answer": "1554323256554",
              "key": "FhBkJQ",
              "title": "Lead contact telephone number",
              "type": "text"
            }
          ],
          "index": 0,
          "question": "Lead contact details",
          "status": "COMPLETED"
        },
        {
          "category": null,
          "fields": [
            {
              "answer": true,
              "key": "markAsComplete",
              "title": "Do you want to mark this section as complete?",
              "type": "boolean"
            }
          ],
          "question": "MarkAsComplete",
          "status": "COMPLETED"
        }
      ],
      "status": "COMPLETED"
    },
    {
      "name": "local-support-cof",
      "questions": [
        {
          "category": "apkBSm",
          "fields": [
            {
              "answer": "<p>test</p>",
              "key": "tDVPnl",
              "title": "Tell us about the local support for your project",
              "type": "freeText"
            },
            {
              "answer": null,
              "key": "bDWjTN",
              "title": "Upload supporting evidence (optional)",
              "type": "text"
            }
          ],
          "index": 0,
          "question": "Your support for the project",
          "status": "COMPLETED"
        },
        {
          "category": null,
          "fields": [
            {
              "answer": true,
              "key": "markAsComplete",
              "title": "Do you want to mark this section as complete?",
              "type": "boolean"
            }
          ],
          "question": "MarkAsComplete",
          "status": "COMPLETED"
        }
      ],
      "status": "COMPLETED"
    },
    {
      "name": "risk-cof",
      "questions": [
        {
          "category": "HKdODf",
          "fields": [
            {
              "answer": "TestDoc.docx",
              "key": "EODncR",
              "title": "Risks to your project (document upload)",
              "type": "text"
            }
          ],
          "index": 0,
          "question": "Your project risk register",
          "status": "COMPLETED"
        },
        {
          "category": null,
          "fields": [
            {
              "answer": true,
              "key": "markAsComplete",
              "title": "Do you want to mark this section as complete?",
              "type": "boolean"
            }
          ],
          "question": "MarkAsComplete",
          "status": "COMPLETED"
        }
      ],
      "status": "COMPLETED"
    },
    {
      "name": "upload-business-plan-cof",
      "questions": [
        {
          "category": "xtwqlH",
          "fields": [
            {
              "answer": "TestDoc.docx",
              "key": "ndpQJk",
              "title": "Upload business plan",
              "type": "text"
            }
          ],
          "index": 0,
          "question": "Your business plan",
          "status": "COMPLETED"
        },
        {
          "category": null,
          "fields": [
            {
              "answer": true,
              "key": "markAsComplete",
              "title": "Do you want to mark this section as complete?",
              "type": "boolean"
            }
          ],
          "question": "MarkAsComplete",
          "status": "COMPLETED"
        }
      ],
      "status": "COMPLETED"
    },
    {
      "name": "organisation-information-cof",
      "questions": [
        {
          "category": "JBqDtK",
          "fields": [
            {
              "answer": "45634564",
              "key": "WWWWxy",
              "title": "Your unique tracker number",
              "type": "text"
            },
            {
              "answer": "Test",
              "key": "YdtlQZ",
              "title": "Organisation name",
              "type": "text"
            },
            {
              "answer": true,
              "key": "iBCGxY",
              "title": "Does your organisation use any other names?",
              "type": "list"
            }
          ],
          "index": 0,
          "question": "Organisation names",
          "status": "COMPLETED"
        },
        {
          "category": "JBqDtK",
          "fields": [
            {
              "answer": "Test",
              "key": "PHFkCs",
              "title": "Alternative names of your organisation",
              "type": "text"
            },
            {
              "answer": null,
              "key": "QgNhXX",
              "title": "Alternative names of your organisation - Alternative name 2 ",
              "type": "text"
            },
            {
              "answer": null,
              "key": "XCcqae",
              "title": "Alternative names of your organisation - Alternative name 3 ",
              "type": "text"
            }
          ],
          "index": 0,
          "question": "Alternative names of your organisation",
          "status": "COMPLETED"
        },
        {
          "category": "JBqDtK",
          "fields": [
            {
              "answer": "<p>Test</p>",
              "key": "emVGxS",
              "title": "What is your organisation's main purpose?",
              "type": "freeText"
            },
            {
              "answer": "<p>test</p>",
              "key": "btTtIb",
              "title": "Tell us about your organisation's main activities",
              "type": "freeText"
            },
            {
              "answer": "<p>test</p>",
              "key": "SkocDi",
              "title": "Tell us about your organisation's main activities - Activity 2 ",
              "type": "freeText"
            },
            {
              "answer": "<p>test</p>",
              "key": "CNeeiC",
              "title": "Tell us about your organisation's main activities - Activity 3 ",
              "type": "freeText"
            },
            {
              "answer": true,
              "key": "BBlCko",
              "title": "Have you delivered projects like this before?",
              "type": "list"
            }
          ],
          "index": 0,
          "question": "Purpose and activities",
          "status": "COMPLETED"
        },
        {
          "category": "JBqDtK",
          "fields": [
            {
              "answer": "<p>test</p>",
              "key": "wxCszQ",
              "title": "Describe your previous projects",
              "type": "freeText"
            },
            {
              "answer": "<p>test</p>",
              "key": "QJFQgi",
              "title": "Describe your previous projects - Project 2 ",
              "type": "freeText"
            },
            {
              "answer": null,
              "key": "DGNWqE",
              "title": "Describe your previous projects - Project 3 ",
              "type": "freeText"
            }
          ],
          "index": 0,
          "question": "Previous projects similar to this one",
          "status": "COMPLETED"
        },
        {
          "category": "JBqDtK",
          "fields": [
            {
              "answer": "CIO",
              "key": "lajFtB",
              "title": "Type of organisation",
              "type": "list"
            }
          ],
          "index": 0,
          "question": "How your organisation is classified",
          "status": "COMPLETED"
        },
        {
          "category": "JBqDtK",
          "fields": [
            {
              "answer": "786786",
              "key": "aHIGbK",
              "title": "Charity number ",
              "type": "text"
            }
          ],
          "index": 0,
          "question": "Charity registration details",
          "status": "COMPLETED"
        },
        {
          "category": "JBqDtK",
          "fields": [
            {
              "answer": false,
              "key": "DwfHtk",
              "title": "Is your organisation a trading subsidiary of a parent company?",
              "type": "list"
            }
          ],
          "index": 0,
          "question": "Trading subsidiaries",
          "status": "COMPLETED"
        },
        {
          "category": "JBqDtK",
          "fields": [
            {
              "answer": "test, test, test, test, ss12ss",
              "key": "ZQolYb",
              "title": "Organisation address",
              "type": "text"
            },
            {
              "answer": true,
              "key": "zsoLdf",
              "title": "Is your correspondence address different to the organisation address?",
              "type": "list"
            },
            {
              "answer": "https://www.google.com",
              "key": "FhbaEy",
              "title": "Website and social media",
              "type": "text"
            },
            {
              "answer": null,
              "key": "FcdKlB",
              "title": "Website and social media - Link or username 2",
              "type": "text"
            },
            {
              "answer": null,
              "key": "BzxgDA",
              "title": "Website and social media - Link or username 3",
              "type": "text"
            }
          ],
          "index": 0,
          "question": "Organisation address",
          "status": "COMPLETED"
        },
        {
          "category": "JBqDtK",
          "fields": [
            {
              "answer": "Test, test, test, test, ss12ss",
              "key": "VhkCbM",
              "title": "Correspondence address",
              "type": "text"
            }
          ],
          "index": 0,
          "question": "Correspondence address",
          "status": "COMPLETED"
        },
        {
          "category": "JBqDtK",
          "fields": [
            {
              "answer": false,
              "key": "hnLurH",
              "title": "Is your application a joint bid in partnership with other organisations?",
              "type": "list"
            }
          ],
          "index": 0,
          "question": "Joint applications",
          "status": "COMPLETED"
        },
        {
          "category": null,
          "fields": [
            {
              "answer": true,
              "key": "markAsComplete",
              "title": "Do you want to mark this section as complete?",
              "type": "boolean"
            }
          ],
          "question": "MarkAsComplete",
          "status": "COMPLETED"
        }
      ],
      "status": "COMPLETED"
    },
    {
      "name": "asset-information-cof",
      "questions": [
        {
          "category": "wxYZcT",
          "fields": [
            {
              "answer": "community-centre",
              "key": "oXGwlA",
              "title": "Asset type",
              "type": "list"
            }
          ],
          "index": 0,
          "question": "How the asset is used in the community",
          "status": "COMPLETED"
        },
        {
          "category": "wxYZcT",
          "fields": [
            {
              "answer": "buy-the-asset",
              "key": "LaxeJN",
              "title": "How do you intend to take community ownership of the asset?",
              "type": "list"
            }
          ],
          "index": 0,
          "question": "The asset in community ownership",
          "status": "COMPLETED"
        },
        {
          "category": "wxYZcT",
          "fields": [
            {
              "answer": "TestDoc.docx",
              "key": "tTOrEp",
              "title": "Please upload evidence that shows the asset valuation (if you are buying the asset) or the lease agreement (if you are leasing the asset).",
              "type": "text"
            }
          ],
          "index": 0,
          "question": "Upload asset valuation or lease agreement",
          "status": "COMPLETED"
        },
        {
          "category": "wxYZcT",
          "fields": [
            {
              "answer": false,
              "key": "wAUFqr",
              "title": "Do you know who currently owns your asset?",
              "type": "list"
            }
          ],
          "index": 0,
          "question": "Who owns the asset",
          "status": "COMPLETED"
        },
        {
          "category": "wxYZcT",
          "fields": [
            {
              "answer": "test",
              "key": "XiHjDO",
              "title": "Tell us what you know about the sale or lease of the asset",
              "type": "text"
            }
          ],
          "index": 0,
          "question": "Current ownership status",
          "status": "COMPLETED"
        },
        {
          "category": "wxYZcT",
          "fields": [
            {
              "answer": "<p>test</p>",
              "key": "XPcbJx",
              "title": "Describe the expected sale process, or the proposed terms of your lease if you are planning to rent the asset",
              "type": "freeText"
            },
            {
              "answer": "2020-12-11",
              "key": "jGjScT",
              "title": "Expected date of sale or lease",
              "type": "date"
            }
          ],
          "index": 0,
          "question": "Expected terms of your ownership or lease",
          "status": "COMPLETED"
        },
        {
          "category": "wxYZcT",
          "fields": [
            {
              "answer": false,
              "key": "VGXXyq",
              "title": "Is your asset currently publicly owned?",
              "type": "list"
            }
          ],
          "index": 0,
          "question": "Public ownership",
          "status": "COMPLETED"
        },
        {
          "category": "wxYZcT",
          "fields": [
            {
              "answer": [
                "Closure"
              ],
              "key": "qlqyUq",
              "title": "Why is the asset at risk of closure?",
              "type": "list"
            }
          ],
          "index": 0,
          "question": "Risk of closure",
          "status": "COMPLETED"
        },
        {
          "category": "wxYZcT",
          "fields": [
            {
              "answer": false,
              "key": "iqnlTk",
              "title": "Is this a registered Asset of Community Value (ACV)?",
              "type": "list"
            }
          ],
          "index": 0,
          "question": "Assets of community value",
          "status": "COMPLETED"
        },
        {
          "category": "wxYZcT",
          "fields": [
            {
              "answer": true,
              "key": "mZwrmI",
              "title": "Are there assets or services of a similar type available locally?",
              "type": "list"
            }
          ],
          "index": 0,
          "question": "Local service provision",
          "status": "COMPLETED"
        },
        {
          "category": "wxYZcT",
          "fields": [
            {
              "answer": true,
              "key": "BfgLCc",
              "title": "Is your asset different from what is available locally?",
              "type": "list"
            }
          ],
          "index": 0,
          "question": "Local service provision",
          "status": "COMPLETED"
        },
        {
          "category": "wxYZcT",
          "fields": [
            {
              "answer": "<p>test</p>",
              "key": "WTZoVD",
              "title": "Tell us how and why your asset or the service is different",
              "type": "freeText"
            }
          ],
          "index": 0,
          "question": "Local service provision",
          "status": "COMPLETED"
        },
        {
          "category": "wxYZcT",
          "fields": [
            {
              "answer": "<p>test</p>",
              "key": "GEJNWF",
              "title": "How accessible is the closest asset or service?",
              "type": "freeText"
            }
          ],
          "index": 0,
          "question": "Local service provision",
          "status": "COMPLETED"
        },
        {
          "category": "wxYZcT",
          "fields": [
            {
              "answer": true,
              "key": "CFFsxV",
              "title": "Does part of your project include a commercial aspect?",
              "type": "list"
            }
          ],
          "index": 0,
          "question": "Local service provision",
          "status": "COMPLETED"
        },
        {
          "category": "wxYZcT",
          "fields": [
            {
              "answer": "<p>test</p>",
              "key": "FDZQTQ",
              "title": "Tell us how the commercial aspect relates to the other services you provide",
              "type": "freeText"
            }
          ],
          "index": 0,
          "question": "Local service provision",
          "status": "COMPLETED"
        },
        {
          "category": null,
          "fields": [
            {
              "answer": true,
              "key": "markAsComplete",
              "title": "Do you want to mark this section as complete?",
              "type": "boolean"
            }
          ],
          "question": "MarkAsComplete",
          "status": "COMPLETED"
        }
      ],
      "status": "COMPLETED"
    },
    {
      "name": "project-information-cof",
      "questions": [
        {
          "category": "qsnIGd",
          "fields": [
            {
              "answer": false,
              "key": "pWwCRM",
              "title": "Have you applied to the Community Ownership Fund before?",
              "type": "list"
            }
          ],
          "index": 0,
          "question": "Previous Community Ownership Fund applications",
          "status": "COMPLETED"
        },
        {
          "category": "qsnIGd",
          "fields": [
            {
              "answer": "Test Project",
              "key": "apGjFS",
              "title": "Project name",
              "type": "text"
            },
            {
              "answer": "<p>test</p>",
              "key": "bEWpAj",
              "title": "Tell us how the asset is currently being used, or how it has been used before, and why it's important to the community",
              "type": "freeText"
            },
            {
              "answer": "<p>test</p>",
              "key": "uypCNM",
              "title": "Give a brief summary of your project, including what you hope to achieve",
              "type": "freeText"
            },
            {
              "answer": "<p>test</p>",
              "key": "AgeRbd",
              "title": "Tell us about the planned activities and/or services that will take place in the asset",
              "type": "freeText"
            }
          ],
          "index": 0,
          "question": "Project name and summary",
          "status": "COMPLETED"
        },
        {
          "category": "qsnIGd",
          "fields": [
            {
              "answer": "test, test, test, test, ss12ss",
              "key": "EfdliG",
              "title": "Address of the community asset",
              "type": "text"
            },
            {
              "answer": "test",
              "key": "fIEUcb",
              "title": " In which constituency is your asset?",
              "type": "text"
            },
            {
              "answer": "test",
              "key": "SWfcTo",
              "title": "In which local council area is your asset?",
              "type": "text"
            }
          ],
          "index": 0,
          "question": "Address of the asset",
          "status": "COMPLETED"
        },
        {
          "category": null,
          "fields": [
            {
              "answer": true,
              "key": "markAsComplete",
              "title": "Do you want to mark this section as complete?",
              "type": "boolean"
            }
          ],
          "question": "MarkAsComplete",
          "status": "COMPLETED"
        }
      ],
      "status": "COMPLETED"
    },
    {
      "name": "community-engagement-cof",
      "questions": [
        {
          "category": "lmdhVN",
          "fields": [
            {
              "answer": "<p>test</p>",
              "key": "azCutK",
              "title": "Tell us how you have engaged with the community about your intention to take ownership of the asset",
              "type": "freeText"
            }
          ],
          "index": 0,
          "question": "How you've engaged with the community",
          "status": "COMPLETED"
        },
        {
          "category": "lmdhVN",
          "fields": [
            {
              "answer": "<p>test</p>",
              "key": "jAhuWN",
              "title": "Describe your fundraising activities",
              "type": "freeText"
            }
          ],
          "index": 0,
          "question": "Your fundraising activities",
          "status": "COMPLETED"
        },
        {
          "category": "lmdhVN",
          "fields": [
            {
              "answer": "<p>test</p>",
              "key": "HYsezC",
              "title": "Tell us about any partnerships you've formed, and how they'll help the project be successful",
              "type": "freeText"
            },
            {
              "answer": "<p>test</p>",
              "key": "GGBgBY",
              "title": "Tell us how your project supports any wider local plans",
              "type": "freeText"
            }
          ],
          "index": 0,
          "question": "Partnerships and local plans",
          "status": "COMPLETED"
        },
        {
          "category": null,
          "fields": [
            {
              "answer": true,
              "key": "markAsComplete",
              "title": "Do you want to mark this section as complete?",
              "type": "boolean"
            }
          ],
          "question": "MarkAsComplete",
          "status": "COMPLETED"
        }
      ],
      "status": "COMPLETED"
    },
    {
      "name": "declarations-cof",
      "questions": [
        {
          "category": "LkvizC",
          "fields": [
            {
              "answer": true,
              "key": "vSQKwD",
              "title": "Confirm you have considered subsidy control and state aid implications for your project, and the information you have given us is correct",
              "type": "list"
            },
            {
              "answer": true,
              "key": "CQoLFp",
              "title": "Confirm you have considered people with protected characteristics throughout the planning of your project",
              "type": "list"
            },
            {
              "answer": true,
              "key": "jdPkiX",
              "title": "Confirm you have considered sustainability and the environment throughout the planning of your project, including compliance with the government's Net Zero ambitions",
              "type": "list"
            },
            {
              "answer": true,
              "key": "qWuSCy",
              "title": "Confirm you have a bank account set up and associated with the organisation you are applying on behalf of",
              "type": "list"
            },
            {
              "answer": true,
              "key": "tjZlml",
              "title": "Confirm that the information you've provided in this application is accurate to the best of your knowledge on the date of submission",
              "type": "list"
            }
          ],
          "index": 0,
          "question": "Agree to the final confirmations",
          "status": "COMPLETED"
        },
        {
          "category": null,
          "fields": [
            {
              "answer": true,
              "key": "markAsComplete",
              "title": "Do you want to mark this section as complete?",
              "type": "boolean"
            }
          ],
          "question": "MarkAsComplete",
          "status": "COMPLETED"
        }
      ],
      "status": "COMPLETED"
    },
    {
      "name": "community-benefits-cof",
      "questions": [
        {
          "category": "PTOBPV",
          "fields": [
            {
              "answer": [
                "community-pride"
              ],
              "key": "pqYxJO",
              "title": "What community benefits do you expect to deliver with this project?",
              "type": "list"
            },
            {
              "answer": "<p>test</p>",
              "key": "lgfiGB",
              "title": "Tell us about these benefits in detail, and how the asset's activities will help deliver them",
              "type": "freeText"
            },
            {
              "answer": "<p>test</p>",
              "key": "zKKouR",
              "title": "Explain how you plan to deliver and sustain these benefits over time",
              "type": "freeText"
            },
            {
              "answer": "<p>test</p>",
              "key": "ZyIQGI",
              "title": "Tell us how you'll make sure the whole community benefits from the asset",
              "type": "freeText"
            }
          ],
          "index": 0,
          "question": "Benefits you'll deliver",
          "status": "COMPLETED"
        },
        {
          "category": null,
          "fields": [
            {
              "answer": true,
              "key": "markAsComplete",
              "title": "Do you want to mark this section as complete?",
              "type": "boolean"
            }
          ],
          "question": "MarkAsComplete",
          "status": "COMPLETED"
        }
      ],
      "status": "COMPLETED"
    },
    {
      "name": "funding-required-cof",
      "questions": [
        {
          "category": "bgUGuD",
          "fields": [
            {
              "answer": "966585",
              "key": "ABROnB",
              "title": "Capital funding request",
              "type": "text"
            },
            {
              "answer": false,
              "key": "hJkmBS",
              "title": "If successful, will you use your funding in the next 12 months?",
              "type": "list"
            }
          ],
          "index": 0,
          "question": "Capital funding request",
          "status": "COMPLETED"
        },
        {
          "category": "bgUGuD",
          "fields": [
            {
              "answer": [
                {
                  "GLQlOh": "test",
                  "JtwkMy": 542,
                  "LeTLDo": 456,
                  "pHZDWT": 45654
                }
              ],
              "key": "qQLyXL",
              "title": "Capital costs",
              "type": "multiInput"
            }
          ],
          "index": 0,
          "question": "Capital costs for your project",
          "status": "COMPLETED"
        },
        {
          "category": "bgUGuD",
          "fields": [
            {
              "answer": false,
              "key": "DOvZvB",
              "title": "Have you secured any match funding yet?",
              "type": "list"
            }
          ],
          "index": 0,
          "question": "If you've secured match funding",
          "status": "COMPLETED"
        },
        {
          "category": "bgUGuD",
          "fields": [
            {
              "answer": [
                {
                  "THOdae": 41242,
                  "iMJdfs": "test"
                }
              ],
              "key": "vEOdBS",
              "title": "Unsecured match funding",
              "type": "multiInput"
            }
          ],
          "index": 0,
          "question": "Unsecured match funding",
          "status": "COMPLETED"
        },
        {
          "category": "bgUGuD",
          "fields": [
            {
              "answer": false,
              "key": "matkNH",
              "title": "Are you applying for revenue funding from the Community Ownership Fund? (optional)",
              "type": "list"
            }
          ],
          "index": 0,
          "question": "Revenue funding",
          "status": "COMPLETED"
        },
        {
          "category": null,
          "fields": [
            {
              "answer": true,
              "key": "markAsComplete",
              "title": "Do you want to mark this section as complete?",
              "type": "boolean"
            }
          ],
          "question": "MarkAsComplete",
          "status": "COMPLETED"
        }
      ],
      "status": "COMPLETED"
    },
    {
      "name": "feasibility-cof",
      "questions": [
        {
          "category": "bBGnkL",
          "fields": [
            {
              "answer": "<p>test</p>",
              "key": "iSbwDM",
              "title": "Tell us about the feasibility studies you have carried out for your project",
              "type": "freeText"
            },
            {
              "answer": false,
              "key": "jFPlEJ",
              "title": "Do you need to do any further feasibility work?",
              "type": "list"
            }
          ],
          "index": 0,
          "question": "Feasiblity studies you've carried out",
          "status": "COMPLETED"
        },
        {
          "category": null,
          "fields": [
            {
              "answer": true,
              "key": "markAsComplete",
              "title": "Do you want to mark this section as complete?",
              "type": "boolean"
            }
          ],
          "question": "MarkAsComplete",
          "status": "COMPLETED"
        }
      ],
      "status": "COMPLETED"
    },
    {
      "name": "operational-costs-cof",
      "questions": [
        {
          "category": "oSfXFZ",
          "fields": [
            {
              "answer": "<p><strong>test</strong></p>",
              "key": "qXNkfr",
              "title": "Summarise your income and operational costs for the running of the asset",
              "type": "freeText"
            }
          ],
          "index": 0,
          "question": "Forecasted income and operational costs to run the asset",
          "status": "COMPLETED"
        },
        {
          "category": null,
          "fields": [
            {
              "answer": true,
              "key": "markAsComplete",
              "title": "Do you want to mark this section as complete?",
              "type": "boolean"
            }
          ],
          "question": "MarkAsComplete",
          "status": "COMPLETED"
        }
      ],
      "status": "COMPLETED"
    },
    {
      "name": "community-representation-cof",
      "questions": [
        {
          "category": "KbnmOO",
          "fields": [
            {
              "answer": "<p>test</p>",
              "key": "ReomFo",
              "title": "List the members of your board",
              "type": "freeText"
            },
            {
              "answer": "<p>test</p>",
              "key": "fjVmOt",
              "title": "Tell us about your governance and membership structures",
              "type": "freeText"
            },
            {
              "answer": "<ol>\\r\\n<li>test</li>\\r\\n</ol>",
              "key": "GETNxN",
              "title": "Explain how you'll consider the views of the community in the running of the asset",
              "type": "freeText"
            }
          ],
          "index": 0,
          "question": "How you’ll run the asset",
          "status": "COMPLETED"
        },
        {
          "category": null,
          "fields": [
            {
              "answer": true,
              "key": "markAsComplete",
              "title": "Do you want to mark this section as complete?",
              "type": "boolean"
            }
          ],
          "question": "MarkAsComplete",
          "status": "COMPLETED"
        }
      ],
      "status": "COMPLETED"
    },
    {
      "name": "inclusiveness-and-integration-cof",
      "questions": [
        {
          "category": "eCZBSV",
          "fields": [
            {
              "answer": "<p>test</p>",
              "key": "mgIesb",
              "title": "Tell us how the asset will be accountable to local people, and involve them in its running",
              "type": "freeText"
            },
            {
              "answer": "<p>test</p>",
              "key": "lQEkep",
              "title": "Describe anything that might prevent people from using the asset or participating in its running",
              "type": "freeText"
            }
          ],
          "index": 0,
          "question": "How you’ll make the asset inclusive",
          "status": "COMPLETED"
        },
        {
          "category": null,
          "fields": [
            {
              "answer": true,
              "key": "markAsComplete",
              "title": "Do you want to mark this section as complete?",
              "type": "boolean"
            }
          ],
          "question": "MarkAsComplete",
          "status": "COMPLETED"
        }
      ],
      "status": "COMPLETED"
    },
    {
      "name": "skills-and-resources-cof",
      "questions": [
        {
          "category": "eLpYFr",
          "fields": [
            {
              "answer": "<p>test</p>",
              "key": "XXGyzn",
              "title": "Describe any relevant experience you have delivering similar projects or running an asset",
              "type": "freeText"
            }
          ],
          "index": 0,
          "question": "Your experience running similar assets",
          "status": "COMPLETED"
        },
        {
          "category": "eLpYFr",
          "fields": [
            {
              "answer": false,
              "key": "Uaeyae",
              "title": "Do you have plans to recruit people to help you run the asset?",
              "type": "list"
            }
          ],
          "index": 0,
          "question": "Recruitment plans",
          "status": "COMPLETED"
        },
        {
          "category": null,
          "fields": [
            {
              "answer": true,
              "key": "markAsComplete",
              "title": "Do you want to mark this section as complete?",
              "type": "boolean"
            }
          ],
          "question": "MarkAsComplete",
          "status": "COMPLETED"
        }
      ],
      "status": "COMPLETED"
    }
  ]
  }
"""
)

cof25r1_application_store_json_template = Template(
    """
    {
    "id": "$app_id",
    "language": "en",
    "fund_id": "$fund_id",
    "last_edited": "2024-10-28T14:02:51.824519",
    "project_name": "$project_name",
    "reference": "$short_ref",
    "round_id": "$round_id",
    "round_name": "Round 1",
    "started_at": "2024-10-28T13:58:21.742143",
    "status": "SUBMITTED",
    "account_id": "3e5de99b-121d-4ebd-adaa-a81a40c9f808",
    "date_submitted": "2024-10-28T14:08:57.519775",
    "forms": [
        {
        "name": "applicant-information-cof-25",
        "questions": [
            {
            "category": "ZuHuGk",
            "fields": [
                {
                "answer": "Sonia",
                "key": "SnLGJE",
                "title": "Name of lead contact",
                "type": "text"
                },
                {
                "answer": "Senior Web Representative",
                "key": "qRDTUc",
                "title": "Lead contact job title",
                "type": "text"
                },
                {
                "answer": "Hosea_Gleichner90@gmail.com",
                "key": "NlHSBg",
                "title": "Lead contact email address",
                "type": "text"
                },
                {
                "answer": "+44 77100756732",
                "key": "FhBkJQ",
                "title": "Lead contact telephone number",
                "type": "text"
                }
            ],
            "question": "Lead contact details",
            "status": "COMPLETED"
            },
            {
            "category": null,
            "fields": [
                {
                "answer": true,
                "key": "markAsComplete",
                "title": "Do you want to mark this section as complete?",
                "type": "boolean"
                }
            ],
            "question": "MarkAsComplete",
            "status": "COMPLETED"
            }
        ],
        "status": "COMPLETED"
        },
        {
        "name": "community-use-cof-25",
        "questions": [
            {
            "category": "GMkooI",
            "fields": [
                {
                "answer": "<p>Test Community use/significance Form</p>",
                "key": "zTcrYo",
                "title": "Who in the community currently uses the asset, or has used it in the past?",
                "type": "freeText"
                },
                {
                "answer": "<p>Test Community use/significance Form</p>",
                "key": "whlRYS",
                "title": "Tell us how losing the asset would affect, or has already affected, people in the community",
                "type": "freeText"
                },
                {
                "answer": "<p>Test Community use/significance Form</p>",
                "key": "NGSXHE",
                "title": "Why will the asset be lost without community intervention?",
                "type": "freeText"
                },
                {
                "answer": "<p>Test Community use/significance Form</p>",
                "key": "Ieudgn",
                "title": "Explain how the community will be better served with the asset under community ownership",
                "type": "freeText"
                }
            ],
            "question": "Who uses the asset",
            "status": "COMPLETED"
            },
            {
            "category": null,
            "fields": [
                {
                "answer": true,
                "key": "markAsComplete",
                "title": "Do you want to mark this section as complete?",
                "type": "boolean"
                }
            ],
            "question": "MarkAsComplete",
            "status": "COMPLETED"
            }
        ],
        "status": "COMPLETED"
        },
        {
        "name": "local-support-cof-25",
        "questions": [
            {
            "category": "apkBSm",
            "fields": [
                {
                "answer": "<p>Tell us about the local support for your project</p>",
                "key": "tDVPnl",
                "title": "Tell us about the local support for your project",
                "type": "freeText"
                },
                {
                "answer": null,
                "key": "bDWjTN",
                "title": "Upload supporting evidence (optional)",
                "type": "text"
                }
            ],
            "question": "Your support for the project",
            "status": "COMPLETED"
            },
            {
            "category": null,
            "fields": [
                {
                "answer": true,
                "key": "markAsComplete",
                "title": "Do you want to mark this section as complete?",
                "type": "boolean"
                }
            ],
            "question": "MarkAsComplete",
            "status": "COMPLETED"
            }
        ],
        "status": "COMPLETED"
        },
        {
        "name": "environmental-sustainability-cof-25",
        "questions": [
            {
            "category": "ljcxPd",
            "fields": [
                {
                "answer": "<p>Test Environmental Sustainability Form</p>",
                "key": "dypuJs",
                "title": "Tell us how you have considered the environmental sustainability of your project",
                "type": "freeText"
                }
            ],
            "question": "How you've considered the environment",
            "status": "COMPLETED"
            },
            {
            "category": null,
            "fields": [
                {
                "answer": true,
                "key": "markAsComplete",
                "title": "Do you want to mark this section as complete?",
                "type": "boolean"
                }
            ],
            "question": "MarkAsComplete",
            "status": "COMPLETED"
            }
        ],
        "status": "COMPLETED"
        },
        {
        "name": "risk-cof-25",
        "questions": [
            {
            "category": "HKdODf",
            "fields": [
                {
                "answer": "sample.txt",
                "key": "EODncR",
                "title": "Risks to your project (document upload)",
                "type": "text"
                }
            ],
            "question": "Your project risk register",
            "status": "COMPLETED"
            },
            {
            "category": null,
            "fields": [
                {
                "answer": true,
                "key": "markAsComplete",
                "title": "Do you want to mark this section as complete?",
                "type": "boolean"
                }
            ],
            "question": "MarkAsComplete",
            "status": "COMPLETED"
            }
        ],
        "status": "COMPLETED"
        },
        {
        "name": "upload-business-plan-cof-25",
        "questions": [
            {
            "category": "xtwqlH",
            "fields": [
                {
                "answer": "sample.txt",
                "key": "ndpQJk",
                "title": "Upload business plan",
                "type": "text"
                }
            ],
            "question": "Your business plan",
            "status": "COMPLETED"
            },
            {
            "category": null,
            "fields": [
                {
                "answer": true,
                "key": "markAsComplete",
                "title": "Do you want to mark this section as complete?",
                "type": "boolean"
                }
            ],
            "question": "MarkAsComplete",
            "status": "COMPLETED"
            }
        ],
        "status": "COMPLETED"
        },
        {
        "name": "organisation-information-cof-25",
        "questions": [
            {
            "category": "JBqDtK",
            "fields": [
                {
                "answer": "ANON-###-###-###",
                "key": "WWWWxy",
                "title": "Your expression of interest (EOI) application reference",
                "type": "text"
                },
                {
                "answer": "Moore - Medhurst",
                "key": "YdtlQZ",
                "title": "Organisation name",
                "type": "text"
                },
                {
                "answer": true,
                "key": "iBCGxY",
                "title": "Does your organisation use any other names?",
                "type": "list"
                }
            ],
            "question": "Organisation names",
            "status": "COMPLETED"
            },
            {
            "category": "JBqDtK",
            "fields": [
                {
                "answer": "Moore - Medhurst",
                "key": "PHFkCs",
                "title": "Alternative names of your organisation",
                "type": "text"
                },
                {
                "answer": null,
                "key": "QgNhXX",
                "title": "Alternative names of your organisation - Alternative name 2 ",
                "type": "text"
                },
                {
                "answer": null,
                "key": "XCcqae",
                "title": "Alternative names of your organisation - Alternative name 3 ",
                "type": "text"
                }
            ],
            "question": "Alternative names of your organisation",
            "status": "COMPLETED"
            },
            {
            "category": "JBqDtK",
            "fields": [
                {
                "answer": "<p>Test Org Form</p>",
                "key": "emVGxS",
                "title": "What is your organisation's main purpose?",
                "type": "freeText"
                },
                {
                "answer": "<p>Test Org Form</p>",
                "key": "btTtIb",
                "title": "Tell us about your organisation's main activities",
                "type": "freeText"
                },
                {
                "answer": null,
                "key": "SkocDi",
                "title": "Tell us about your organisation's main activities - Activity 2 ",
                "type": "freeText"
                },
                {
                "answer": null,
                "key": "CNeeiC",
                "title": "Tell us about your organisation's main activities - Activity 3 ",
                "type": "freeText"
                },
                {
                "answer": true,
                "key": "BBlCko",
                "title": "Have you delivered projects like this before?",
                "type": "list"
                }
            ],
            "question": "Purpose and activities",
            "status": "COMPLETED"
            },
            {
            "category": "JBqDtK",
            "fields": [
                {
                "answer": "<p>Test Org Form</p>",
                "key": "wxCszQ",
                "title": "Describe your previous projects",
                "type": "freeText"
                },
                {
                "answer": null,
                "key": "QJFQgi",
                "title": "Describe your previous projects - Project 2 ",
                "type": "freeText"
                },
                {
                "answer": null,
                "key": "DGNWqE",
                "title": "Describe your previous projects - Project 3 ",
                "type": "freeText"
                }
            ],
            "question": "Previous projects similar to this one",
            "status": "COMPLETED"
            },
            {
            "category": "JBqDtK",
            "fields": [
                {
                "answer": "Trust port",
                "key": "lajFtB",
                "title": "Type of organisation",
                "type": "list"
                }
            ],
            "question": "How your organisation is classified",
            "status": "COMPLETED"
            },
            {
            "category": "JBqDtK",
            "fields": [
                {
                "answer": "7579008310984176",
                "key": "GlPmCX",
                "title": "Company registration number",
                "type": "text"
                }
            ],
            "question": "Company registration details",
            "status": "COMPLETED"
            },
            {
            "category": "JBqDtK",
            "fields": [
                {
                "answer": "Companies House",
                "key": "GvPSna",
                "title": "Which regulatory body is your company registered with?",
                "type": "list"
                }
            ],
            "question": "Registration details",
            "status": "COMPLETED"
            },
            {
            "category": "JBqDtK",
            "fields": [
                {
                "answer": true,
                "key": "DwfHtk",
                "title": "Is your organisation a trading subsidiary of a parent company?",
                "type": "list"
                }
            ],
            "question": "Trading subsidiaries",
            "status": "COMPLETED"
            },
            {
            "category": "JBqDtK",
            "fields": [
                {
                "answer": "Moore - Medhurst",
                "key": "MPNlZx",
                "title": "Name of parent organisation",
                "type": "text"
                },
                {
                "answer": "2024-01-01",
                "key": "MyiYMw",
                "title": "Date parent organisation was established",
                "type": "date"
                }
            ],
            "question": "Parent organisation details",
            "status": "COMPLETED"
            },
            {
            "category": "JBqDtK",
            "fields": [
                {
                "answer": "80 Vicarage Road, Birchett Road, East Gradywick, Hampshire, GU11 1LY",
                "key": "ZQolYb",
                "title": "Organisation address",
                "type": "text"
                },
                {
                "answer": false,
                "key": "zsoLdf",
                "title": "Is your correspondence address different to the organisation address?",
                "type": "list"
                },
                {
                "answer": "https://twitter.com/luhc",
                "key": "FhbaEy",
                "title": "Website and social media",
                "type": "text"
                },
                {
                "answer": null,
                "key": "FcdKlB",
                "title": "Website and social media - Link or username 2",
                "type": "text"
                },
                {
                "answer": null,
                "key": "BzxgDA",
                "title": "Website and social media - Link or username 3",
                "type": "text"
                }
            ],
            "question": "Organisation address",
            "status": "COMPLETED"
            },
            {
            "category": "JBqDtK",
            "fields": [
                {
                "answer": true,
                "key": "hnLurH",
                "title": "Is your application a joint bid in partnership with other organisations?",
                "type": "list"
                }
            ],
            "question": "Joint applications",
            "status": "COMPLETED"
            },
            {
            "category": "JBqDtK",
            "fields": [
                {
                "answer": "Moore - Medhurst",
                "key": "APSjeB",
                "title": "Partner organisation name",
                "type": "text"
                },
                {
                "answer": "80 Vicarage Road, Birchett Road, East Gradywick, Hampshire, GU11 1LY",
                "key": "biTJjF",
                "title": "Partner organisation address",
                "type": "text"
                },
                {
                "answer": "<p>Test Org Form</p>",
                "key": "IkmvEt",
                "title": "Tell us about your partnership and how you plan to work together",
                "type": "freeText"
                }
            ],
            "question": "Partner organisation details",
            "status": "COMPLETED"
            },
            {
            "category": null,
            "fields": [
                {
                "answer": true,
                "key": "markAsComplete",
                "title": "Do you want to mark this section as complete?",
                "type": "boolean"
                }
            ],
            "question": "MarkAsComplete",
            "status": "COMPLETED"
            }
        ],
        "status": "COMPLETED"
        },
        {
        "name": "project-information-cof-25",
        "questions": [
            {
            "category": "qsnIGd",
            "fields": [
                {
                "answer": true,
                "key": "pWwCRM",
                "title": "Have you applied to the Community Ownership Fund 2025 before?",
                "type": "list"
                }
            ],
            "question": "Previous Community Ownership Fund 2025 applications",
            "status": "COMPLETED"
            },
            {
            "category": "qsnIGd",
            "fields": [
                {
                "answer": true,
                "key": "paawsj",
                "title": "Was your application successful?",
                "type": "list"
                }
            ],
            "question": "Successful Community Ownership Fund 2025 applications",
            "status": "COMPLETED"
            },
            {
            "category": "qsnIGd",
            "fields": [
                {
                "answer": "<p>Test Project Information Form</p>",
                "key": "ACppgI",
                "title": "Describe the project for which you were given funding",
                "type": "freeText"
                },
                {
                "answer": "995",
                "key": "yuvajR",
                "title": "Amount of funding received",
                "type": "text"
                }
            ],
            "question": "Projects previously funded by the Community Ownership Fund 2025",
            "status": "COMPLETED"
            },
            {
            "category": "qsnIGd",
            "fields": [
                {
                "answer": "Community Ownership Fund E2E Journey Barton, Blick and Kessler Project ",
                "key": "apGjFS",
                "title": "Project name",
                "type": "text"
                },
                {
                "answer": "<p>Test Project Information Form</p>",
                "key": "bEWpAj",
                "title": "Tell us how the asset is currently being used, or how it has been used before, and why it's important to the community",
                "type": "freeText"
                },
                {
                "answer": "<p>Test Project Information Form</p>",
                "key": "uypCNM",
                "title": "Give a brief summary of your project, including what you hope to achieve",
                "type": "freeText"
                },
                {
                "answer": "<p>Test Project Information Form</p>",
                "key": "AgeRbd",
                "title": "Tell us about the planned activities and/or services that will take place in the asset",
                "type": "freeText"
                }
            ],
            "question": "Project name and summary",
            "status": "COMPLETED"
            },
            {
            "category": "qsnIGd",
            "fields": [
                {
                "answer": "64 Cambridge Street, Birchett Road, Connelly-upon-Fisher, Hampshire, GU11 1LY",
                "key": "EfdliG",
                "title": "Address of the community asset",
                "type": "text"
                },
                {
                "answer": "Aldershot",
                "key": "fIEUcb",
                "title": " In which constituency is your asset?",
                "type": "text"
                },
                {
                "answer": "Rushmoor",
                "key": "SWfcTo",
                "title": "In which local council area is your asset?",
                "type": "text"
                }
            ],
            "question": "Address of the asset",
            "status": "COMPLETED"
            },
            {
            "category": null,
            "fields": [
                {
                "answer": true,
                "key": "markAsComplete",
                "title": "Do you want to mark this section as complete?",
                "type": "boolean"
                }
            ],
            "question": "MarkAsComplete",
            "status": "COMPLETED"
            }
        ],
        "status": "COMPLETED"
        },
        {
        "name": "declarations-cof-25",
        "questions": [
            {
            "category": "LkvizC",
            "fields": [
                {
                "answer": false,
                "key": "vSQKwD",
                "title": "Confirm you have considered subsidy control and state aid implications for your project, and the information you have given us is correct",
                "type": "list"
                },
                {
                "answer": false,
                "key": "CQoLFp",
                "title": "Confirm you have considered people with protected characteristics throughout the planning of your project",
                "type": "list"
                },
                {
                "answer": true,
                "key": "jdPkiX",
                "title": "Confirm you have considered sustainability and the environment throughout the planning of your project, including compliance with the government's Net Zero ambitions",
                "type": "list"
                },
                {
                "answer": false,
                "key": "qWuSCy",
                "title": "Confirm you have a bank account set up and associated with the organisation you are applying on behalf of",
                "type": "list"
                },
                {
                "answer": true,
                "key": "tjZlml",
                "title": "Confirm that the information you've provided in this application is accurate to the best of your knowledge on the date of submission",
                "type": "list"
                }
            ],
            "question": "Agree to the final confirmations",
            "status": "COMPLETED"
            },
            {
            "category": null,
            "fields": [
                {
                "answer": true,
                "key": "markAsComplete",
                "title": "Do you want to mark this section as complete?",
                "type": "boolean"
                }
            ],
            "question": "MarkAsComplete",
            "status": "COMPLETED"
            }
        ],
        "status": "COMPLETED"
        },
        {
        "name": "community-benefits-cof-25",
        "questions": [
            {
            "category": "PTOBPV",
            "fields": [
                {
                "answer": [
                    "community-pride"
                ],
                "key": "pqYxJO",
                "title": "What community benefits do you expect to deliver with this project?",
                "type": "list"
                },
                {
                "answer": "<p>Test Community Benefits Form</p>",
                "key": "lgfiGB",
                "title": "Tell us about these benefits in detail, and how the asset's activities will help deliver them",
                "type": "freeText"
                },
                {
                "answer": "<p>Test Community Benefits Form</p>",
                "key": "zKKouR",
                "title": "Explain how you plan to deliver and sustain these benefits over time",
                "type": "freeText"
                },
                {
                "answer": "<p>Test Community Benefits Form</p>",
                "key": "ZyIQGI",
                "title": "Tell us how you'll make sure the whole community benefits from the asset",
                "type": "freeText"
                }
            ],
            "question": "Benefits you'll deliver",
            "status": "COMPLETED"
            },
            {
            "category": null,
            "fields": [
                {
                "answer": true,
                "key": "markAsComplete",
                "title": "Do you want to mark this section as complete?",
                "type": "boolean"
                }
            ],
            "question": "MarkAsComplete",
            "status": "COMPLETED"
            }
        ],
        "status": "COMPLETED"
        },
        {
        "name": "community-engagement-cof-25",
        "questions": [
            {
            "category": "lmdhVN",
            "fields": [
                {
                "answer": "<p>Test Community Engagement Form</p>",
                "key": "azCutK",
                "title": "Tell us how you have engaged with the community about your intention to take ownership of the asset",
                "type": "freeText"
                }
            ],
            "question": "How you've engaged with the community",
            "status": "COMPLETED"
            },
            {
            "category": "lmdhVN",
            "fields": [
                {
                "answer": "<p>Test Community Engagement Form</p>",
                "key": "jAhuWN",
                "title": "Describe your fundraising activities",
                "type": "freeText"
                }
            ],
            "question": "Your fundraising activities",
            "status": "COMPLETED"
            },
            {
            "category": "lmdhVN",
            "fields": [
                {
                "answer": "<p>Test Community Engagement Form</p>",
                "key": "HYsezC",
                "title": "Tell us about any partnerships you've formed, and how they'll help the project be successful",
                "type": "freeText"
                },
                {
                "answer": "<p>Test Community Engagement Form</p>",
                "key": "GGBgBY",
                "title": "Tell us how your project supports any wider local plans",
                "type": "freeText"
                }
            ],
            "question": "Partnerships and local plans",
            "status": "COMPLETED"
            },
            {
            "category": null,
            "fields": [
                {
                "answer": true,
                "key": "markAsComplete",
                "title": "Do you want to mark this section as complete?",
                "type": "boolean"
                }
            ],
            "question": "MarkAsComplete",
            "status": "COMPLETED"
            }
        ],
        "status": "COMPLETED"
        },
        {
        "name": "asset-information-cof-25",
        "questions": [
            {
            "category": "wxYZcT",
            "fields": [
                {
                "answer": "cinema",
                "key": "oXGwlA",
                "title": "Asset type",
                "type": "list"
                }
            ],
            "question": "How the asset is used in the community",
            "status": "COMPLETED"
            },
            {
            "category": "wxYZcT",
            "fields": [
                {
                "answer": "buy-the-asset",
                "key": "LaxeJN",
                "title": "How do you intend to take community ownership of the asset?",
                "type": "list"
                }
            ],
            "question": "The asset in community ownership",
            "status": "COMPLETED"
            },
            {
            "category": "wxYZcT",
            "fields": [
                {
                "answer": "sample.txt",
                "key": "tTOrEp",
                "title": "Please upload evidence that shows the asset valuation (if you are buying the asset) or the lease agreement (if you are leasing the asset).",
                "type": "text"
                }
            ],
            "question": "Upload asset valuation or lease agreement",
            "status": "COMPLETED"
            },
            {
            "category": "wxYZcT",
            "fields": [
                {
                "answer": true,
                "key": "wAUFqr",
                "title": "Do you know who currently owns your asset?",
                "type": "list"
                }
            ],
            "question": "Who owns the asset",
            "status": "COMPLETED"
            },
            {
            "category": "wxYZcT",
            "fields": [
                {
                "answer": "Mrs. Erin Schinner",
                "key": "FOURVe",
                "title": "Name of current asset owner",
                "type": "text"
                }
            ],
            "question": "Who currently owns your asset",
            "status": "COMPLETED"
            },
            {
            "category": "wxYZcT",
            "fields": [
                {
                "answer": "<p>Test Asset Information Form</p>",
                "key": "XPcbJx",
                "title": "Describe the expected sale process, or the proposed terms of your lease if you are planning to rent the asset",
                "type": "freeText"
                },
                {
                "answer": "2022-12-01",
                "key": "jGjScT",
                "title": "Expected date of sale or lease",
                "type": "date"
                }
            ],
            "question": "Expected terms of your ownership or lease",
            "status": "COMPLETED"
            },
            {
            "category": "wxYZcT",
            "fields": [
                {
                "answer": true,
                "key": "VGXXyq",
                "title": "Is your asset currently publicly owned?",
                "type": "list"
                }
            ],
            "question": "Public ownership",
            "status": "COMPLETED"
            },
            {
            "category": "wxYZcT",
            "fields": [
                {
                "answer": "Mrs. Erin Schinner",
                "key": "rNYmXq",
                "title": "Tell us about the person you have spoken to at the relevant public body about the asset",
                "type": "text"
                },
                {
                "answer": "Customer Configuration Developer",
                "key": "SiOmZn",
                "title": "Job title of contact",
                "type": "text"
                },
                {
                "answer": "Nolan LLC",
                "key": "XXVXuj",
                "title": "Organisation name",
                "type": "text"
                },
                {
                "answer": [
                    "confirm"
                ],
                "key": "MIqglh",
                "title": "When you buy or lease a publicly owned asset, the public authority cannot transfer statutory services or duties to the community group.",
                "type": "list"
                },
                {
                "answer": [
                    "confirm"
                ],
                "key": "JdEmqn",
                "title": "Grants from this fund cannot be used to buy the freehold or premium on the lease of a publicly owned asset. Money must only be used for renovation and refurbishment costs",
                "type": "list"
                },
                {
                "answer": "sample.txt",
                "key": "RFTloT",
                "title": "Upload evidence to confirm the above information and that the asset is at risk",
                "type": "text"
                }
            ],
            "question": "Public ownership details and declarations",
            "status": "COMPLETED"
            },
            {
            "category": "wxYZcT",
            "fields": [
                {
                "answer": [
                    "Sale",
                    "Listed for disposal"
                ],
                "key": "qlqyUq",
                "title": "Why is the asset at risk of closure?",
                "type": "list"
                }
            ],
            "question": "Risk of closure",
            "status": "COMPLETED"
            },
            {
            "category": "wxYZcT",
            "fields": [
                {
                "answer": "2022-12-01",
                "key": "QPIPjx",
                "title": "When was the asset listed?",
                "type": "date"
                },
                {
                "answer": "https://twitter.com/luhc",
                "key": "OJWGGr",
                "title": "Provide a link to the listing",
                "type": "text"
                }
            ],
            "question": "Asset listing details",
            "status": "COMPLETED"
            },
            {
            "category": "wxYZcT",
            "fields": [
                {
                "answer": false,
                "key": "iqnlTk",
                "title": "Is this a registered Asset of Community Value (ACV)?",
                "type": "list"
                }
            ],
            "question": "Assets of community value",
            "status": "COMPLETED"
            },
            {
            "category": "wxYZcT",
            "fields": [
                {
                "answer": true,
                "key": "mZwrmI",
                "title": "Are there assets or services of a similar type available locally?",
                "type": "list"
                }
            ],
            "question": "Local service provision",
            "status": "COMPLETED"
            },
            {
            "category": "wxYZcT",
            "fields": [
                {
                "answer": true,
                "key": "BfgLCc",
                "title": "Is your asset different from what is available locally?",
                "type": "list"
                }
            ],
            "question": "Local service provision",
            "status": "COMPLETED"
            },
            {
            "category": "wxYZcT",
            "fields": [
                {
                "answer": "<p>Test Asset Information Form</p>",
                "key": "WTZoVD",
                "title": "Tell us how and why your asset or the service is different",
                "type": "freeText"
                }
            ],
            "question": "Local service provision",
            "status": "COMPLETED"
            },
            {
            "category": "wxYZcT",
            "fields": [
                {
                "answer": "<p>Test Asset Information Form</p>",
                "key": "GEJNWF",
                "title": "How accessible is the closest asset or service?",
                "type": "freeText"
                }
            ],
            "question": "Local service provision",
            "status": "COMPLETED"
            },
            {
            "category": "wxYZcT",
            "fields": [
                {
                "answer": true,
                "key": "CFFsxV",
                "title": "Does part of your project include a commercial aspect?",
                "type": "list"
                }
            ],
            "question": "Local service provision",
            "status": "COMPLETED"
            },
            {
            "category": "wxYZcT",
            "fields": [
                {
                "answer": "<p>Test Asset Information Form</p>",
                "key": "FDZQTQ",
                "title": "Tell us how the commercial aspect relates to the other services you provide",
                "type": "freeText"
                }
            ],
            "question": "Local service provision",
            "status": "COMPLETED"
            },
            {
            "category": null,
            "fields": [
                {
                "answer": true,
                "key": "markAsComplete",
                "title": "Do you want to mark this section as complete?",
                "type": "boolean"
                }
            ],
            "question": "MarkAsComplete",
            "status": "COMPLETED"
            }
        ],
        "status": "COMPLETED"
        },
        {
        "name": "feasibility-cof-25",
        "questions": [
            {
            "category": "bBGnkL",
            "fields": [
                {
                "answer": "<p>Tell us about the feasibility studies you have carried out for your project</p>",
                "key": "iSbwDM",
                "title": "Tell us about the feasibility studies you have carried out for your project",
                "type": "freeText"
                },
                {
                "answer": true,
                "key": "jFPlEJ",
                "title": "Do you need to do any further feasibility work?",
                "type": "list"
                }
            ],
            "question": "Feasiblity studies you've carried out",
            "status": "COMPLETED"
            },
            {
            "category": "bBGnkL",
            "fields": [
                {
                "answer": "<p>Describe the feasibility work you still need to complete</p>",
                "key": "WWdVTC",
                "title": "Describe the feasibility work you still need to complete",
                "type": "freeText"
                }
            ],
            "question": "Further feasibility work",
            "status": "COMPLETED"
            },
            {
            "category": null,
            "fields": [
                {
                "answer": true,
                "key": "markAsComplete",
                "title": "Do you want to mark this section as complete?",
                "type": "boolean"
                }
            ],
            "question": "MarkAsComplete",
            "status": "COMPLETED"
            }
        ],
        "status": "COMPLETED"
        },
        {
        "name": "operational-costs-cof-25",
        "questions": [
            {
            "category": "oSfXFZ",
            "fields": [
                {
                "answer": "<p>Summarise your income and operational costs for the running of the asset</p>",
                "key": "qXNkfr",
                "title": "Summarise your income and operational costs for the running of the asset",
                "type": "freeText"
                }
            ],
            "question": "Forecasted income and operational costs to run the asset",
            "status": "COMPLETED"
            },
            {
            "category": null,
            "fields": [
                {
                "answer": true,
                "key": "markAsComplete",
                "title": "Do you want to mark this section as complete?",
                "type": "boolean"
                }
            ],
            "question": "MarkAsComplete",
            "status": "COMPLETED"
            }
        ],
        "status": "COMPLETED"
        },
        {
        "name": "skills-and-resources-cof-25",
        "questions": [
            {
            "category": "eLpYFr",
            "fields": [
                {
                "answer": "<p>Test Skills And Resources Form</p>",
                "key": "XXGyzn",
                "title": "Describe any relevant experience you have delivering similar projects or running an asset",
                "type": "freeText"
                }
            ],
            "question": "Your experience running similar assets",
            "status": "COMPLETED"
            },
            {
            "category": "eLpYFr",
            "fields": [
                {
                "answer": true,
                "key": "Uaeyae",
                "title": "Do you have plans to recruit people to help you run the asset?",
                "type": "list"
                }
            ],
            "question": "Recruitment plans",
            "status": "COMPLETED"
            },
            {
            "category": "eLpYFr",
            "fields": [
                {
                "answer": "<p>Test Skills And Resources Form</p>",
                "key": "yHXVSA",
                "title": "Tells us about the roles you'll recruit",
                "type": "freeText"
                }
            ],
            "question": "Roles you’ll recruit to help you run the asset",
            "status": "COMPLETED"
            },
            {
            "category": null,
            "fields": [
                {
                "answer": true,
                "key": "markAsComplete",
                "title": "Do you want to mark this section as complete?",
                "type": "boolean"
                }
            ],
            "question": "MarkAsComplete",
            "status": "COMPLETED"
            }
        ],
        "status": "COMPLETED"
        },
        {
        "name": "inclusiveness-and-integration-cof-25",
        "questions": [
            {
            "category": "eCZBSV",
            "fields": [
                {
                "answer": "<p>Test Inclusiveness and Integration Form</p>",
                "key": "mgIesb",
                "title": "Tell us how the asset will be accountable to local people, and involve them in its running",
                "type": "freeText"
                },
                {
                "answer": "<p>Test Inclusiveness and Integration Form</p>",
                "key": "lQEkep",
                "title": "Describe anything that might prevent people from using the asset or participating in its running",
                "type": "freeText"
                }
            ],
            "question": "How you’ll make the asset inclusive",
            "status": "COMPLETED"
            },
            {
            "category": null,
            "fields": [
                {
                "answer": true,
                "key": "markAsComplete",
                "title": "Do you want to mark this section as complete?",
                "type": "boolean"
                }
            ],
            "question": "MarkAsComplete",
            "status": "COMPLETED"
            }
        ],
        "status": "COMPLETED"
        },
        {
        "name": "funding-required-cof-25",
        "questions": [
            {
            "category": "bgUGuD",
            "fields": [
                {
                "answer": "497",
                "key": "ABROnB",
                "title": "Capital funding request",
                "type": "text"
                },
                {
                "answer": true,
                "key": "hJkmBS",
                "title": "If successful, will you use your funding in the next 12 months?",
                "type": "list"
                }
            ],
            "question": "Capital funding request",
            "status": "COMPLETED"
            },
            {
            "category": "bgUGuD",
            "fields": [
                {
                "answer": [
                    {
                    "GLQlOh": "Capital Funding",
                    "JtwkMy": 497,
                    "LeTLDo": 497,
                    "pHZDWT": 497
                    }
                ],
                "key": "qQLyXL",
                "title": "Capital costs",
                "type": "multiInput"
                }
            ],
            "question": "Capital costs for your project",
            "status": "COMPLETED"
            },
            {
            "category": "bgUGuD",
            "fields": [
                {
                "answer": true,
                "key": "DOvZvB",
                "title": "Have you secured any match funding yet?",
                "type": "list"
                }
            ],
            "question": "If you've secured match funding",
            "status": "COMPLETED"
            },
            {
            "category": "bgUGuD",
            "fields": [
                {
                "answer": [
                    {
                    "JKqLWU": "Secured Match Funding",
                    "LVJcDC": 497
                    }
                ],
                "key": "MopCmv",
                "title": "Secured match funding",
                "type": "multiInput"
                }
            ],
            "question": "Secured match funding",
            "status": "COMPLETED"
            },
            {
            "category": "bgUGuD",
            "fields": [
                {
                "answer": true,
                "key": "HgpNUe",
                "title": "Have you already spent the match funding you have secured?",
                "type": "list"
                }
            ],
            "question": "Have you already spent the match funding you have secured?",
            "status": "COMPLETED"
            },
            {
            "category": "bgUGuD",
            "fields": [
                {
                "answer": true,
                "key": "DmgsiG",
                "title": "Have you identified, but not yet secured, any additional match funding?",
                "type": "list"
                }
            ],
            "question": "If you’ve identified further match funding",
            "status": "COMPLETED"
            },
            {
            "category": "bgUGuD",
            "fields": [
                {
                "answer": [
                    {
                    "THOdae": 497,
                    "iMJdfs": "Unsecured Match Funding"
                    }
                ],
                "key": "vEOdBS",
                "title": "Unsecured match funding",
                "type": "multiInput"
                }
            ],
            "question": "Unsecured match funding",
            "status": "COMPLETED"
            },
            {
            "category": "bgUGuD",
            "fields": [
                {
                "answer": true,
                "key": "matkNH",
                "title": "Are you applying for revenue funding from the Community Ownership Fund 2025? (optional)",
                "type": "list"
                }
            ],
            "question": "Revenue funding",
            "status": "COMPLETED"
            },
            {
            "category": "bgUGuD",
            "fields": [
                {
                "answer": [
                    {
                    "UyaAHw": 497,
                    "hGsUaZ": "Revenue Costs"
                    }
                ],
                "key": "tSKhQQ",
                "title": "Revenue costs (optional)",
                "type": "multiInput"
                }
            ],
            "question": "Revenue costs (optional)",
            "status": "COMPLETED"
            },
            {
            "category": "bgUGuD",
            "fields": [
                {
                "answer": "<p>Tell us how the revenue funding you've requested will help run the asset</p>",
                "key": "XPDbsl",
                "title": "Tell us how the revenue funding you've requested will help run the asset",
                "type": "freeText"
                }
            ],
            "question": "How you'll use revenue funding",
            "status": "COMPLETED"
            },
            {
            "category": null,
            "fields": [
                {
                "answer": true,
                "key": "markAsComplete",
                "title": "Do you want to mark this section as complete?",
                "type": "boolean"
                }
            ],
            "question": "MarkAsComplete",
            "status": "COMPLETED"
            }
        ],
        "status": "COMPLETED"
        },
        {
        "name": "community-representation-cof-25",
        "questions": [
            {
            "category": "KbnmOO",
            "fields": [
                {
                "answer": "<p>Test Community Representation Form</p>",
                "key": "ReomFo",
                "title": "List the members of your board",
                "type": "freeText"
                },
                {
                "answer": "<p>Test Community Representation Form</p>",
                "key": "fjVmOt",
                "title": "Tell us about your governance and membership structures",
                "type": "freeText"
                },
                {
                "answer": "<p>Test Community Representation Form</p>",
                "key": "GETNxN",
                "title": "Explain how you'll consider the views of the community in the running of the asset",
                "type": "freeText"
                }
            ],
            "question": "How you’ll run the asset",
            "status": "COMPLETED"
            },
            {
            "category": null,
            "fields": [
                {
                "answer": true,
                "key": "markAsComplete",
                "title": "Do you want to mark this section as complete?",
                "type": "boolean"
                }
            ],
            "question": "MarkAsComplete",
            "status": "COMPLETED"
            }
        ],
        "status": "COMPLETED"
        }
    ]
    }
    """
)

nstfr2_application_store_json_template = Template(
    """
    {
    "id": "$app_id",
    "status": "SUBMITTED",
    "fund_id": "$fund_id",
    "language": "en",
    "round_id": "$round_id",
    "reference": "$short_ref",
    "account_id": "dd143674-958b-4cb0-8f73-f4ddfddc4578",
    "round_name": "Round 2",
    "started_at": "2023-06-12T13:16:58.555188",
    "last_edited": "2023-06-12T13:19:34.332308",
    "project_name": "$project_name",
    "date_submitted": "2023-06-12T13:19:38.752573",
    "forms": [
        {
            "name": "proposed-services-ns",
            "status": "COMPLETED",
            "questions": [
                {
                    "fields": [
                        {
                            "key": "lOliDH",
                            "type": "freeText",
                            "title": "Tell us how your proposal will transform your existing services",
                            "answer": "<p>Test Proposed Services NS Form</p>"
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "gIqXgO",
                    "question": "Tell us how your proposal will transform your existing services"
                },
                {
                    "fields": [
                        {
                            "key": "dWxxdq",
                            "type": "list",
                            "title": "Do you plan to use this funding to make any changes to the existing night shelter or emergency accommodation?",
                            "answer": true
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "gIqXgO",
                    "question": "Do you plan to use this funding to make any changes to the existing night shelter or emergency accommodation?"
                },
                {
                    "fields": [
                        {
                            "key": "UEndmh",
                            "type": "text",
                            "title": "How many single rooms will you provide with the funding?",
                            "answer": "123"
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "gIqXgO",
                    "question": "How many single rooms will you provide with the funding?"
                },
                {
                    "fields": [
                        {
                            "key": "jzzBDS",
                            "type": "list",
                            "title": "Do you plan to use this funding to make any changes to the existing day provision?",
                            "answer": true
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "gIqXgO",
                    "question": "Do you plan to use this funding to make any changes to the existing day provision?"
                },
                {
                    "fields": [
                        {
                            "key": "bGCkPI",
                            "type": "list",
                            "title": "Which additional day provision will your proposal provide?",
                            "answer": [
                                "other"
                            ]
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "gIqXgO",
                    "question": "Which additional day provision will your proposal provide?"
                },
                {
                    "fields": [
                        {
                            "key": "brLcqY",
                            "type": "freeText",
                            "title": "Which other additional day provision will your proposal provide?",
                            "answer": "<p>Test Proposed Services NS Form</p>"
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "gIqXgO",
                    "question": "Which other additional day provision will your proposal provide?"
                },
                {
                    "fields": [
                        {
                            "key": "bCQWFN",
                            "type": "list",
                            "title": "Will you provide any other additional services?",
                            "answer": true
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "gIqXgO",
                    "question": "Will you provide any other additional services?"
                },
                {
                    "fields": [
                        {
                            "key": "kPvpzG",
                            "type": "freeText",
                            "title": "Which other services will you use the funding to provide?",
                            "answer": "<p>Test Proposed Services NS Form</p>"
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "gIqXgO",
                    "question": "Which other services will you use the funding to provide?"
                },
                {
                    "fields": [
                        {
                            "key": "xYNpHc",
                            "type": "list",
                            "title": "Will your proposal provide additional specialist support?",
                            "answer": true
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "gIqXgO",
                    "question": "Will your proposal provide additional specialist support?"
                },
                {
                    "fields": [
                        {
                            "key": "RKPpEV",
                            "type": "list",
                            "title": "Who will your proposal provide targeted specialist support to?",
                            "answer": [
                                "disabled-people",
                                "other"
                            ]
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "gIqXgO",
                    "question": "Who will your proposal provide targeted specialist support to?"
                },
                {
                    "fields": [
                        {
                            "key": "HTGgzg",
                            "type": "freeText",
                            "title": "Who will your proposal provide specialist support to?",
                            "answer": "<p>Test Proposed Services NS Form</p>"
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "gIqXgO",
                    "question": "Who will your proposal provide specialist support to?"
                }
            ]
        },
        {
            "name": "outputs-and-outcomes-ns",
            "status": "COMPLETED",
            "questions": [
                {
                    "fields": [
                        {
                            "key": "cYEiGS",
                            "type": "text",
                            "title": "How many people will the proposal support with the funding in 2023 to 2024?",
                            "answer": "5"
                        },
                        {
                            "key": "ZZisap",
                            "type": "text",
                            "title": "How many people will the proposal support with the funding in 2024 to 2025?",
                            "answer": "10"
                        },
                        {
                            "key": "ZJCVjE",
                            "type": "text",
                            "title": "How many people with restricted eligibility will the proposal support in 2023 to 2024?",
                            "answer": "15"
                        },
                        {
                            "key": "dboegN",
                            "type": "text",
                            "title": "How many people with restricted eligibility will the proposal support in 2024 to 2025?",
                            "answer": "20"
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "VeHFTz",
                    "question": "Who your proposal will support"
                }
            ]
        },
        {
            "name": "declarations-ns",
            "status": "COMPLETED",
            "questions": [
                {
                    "fields": [
                        {
                            "key": "kOTdzu",
                            "type": "list",
                            "title": "Confirm you have a bank account set up and associated with the organisation you are applying on behalf of",
                            "answer": false
                        },
                        {
                            "key": "NBcyAe",
                            "type": "list",
                            "title": "Confirm that the information you've provided in this application is accurate to the best of your knowledge on the date of submission",
                            "answer": true
                        },
                        {
                            "key": "OKtDsH",
                            "type": "list",
                            "title": "Confirm you have a safeguarding, data protection and health and safety policy",
                            "answer": false
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "gkTvmJ",
                    "question": "Agree to the final confirmations"
                }
            ]
        },
        {
            "name": "working-in-partnership-ns",
            "status": "COMPLETED",
            "questions": [
                {
                    "fields": [
                        {
                            "key": "qMRHPz",
                            "type": "freeText",
                            "title": "Describe your important local partners and how they will support your proposal",
                            "answer": "<p>Test Working In Partnership NS Form</p>"
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "TsNdVD",
                    "question": "Describe your important local partners and how they will support your proposal"
                }
            ]
        },
        {
            "name": "match-funding-ns",
            "status": "COMPLETED",
            "questions": [
                {
                    "fields": [
                        {
                            "key": "nxpXlE",
                            "type": "list",
                            "title": "Will you use match funding for this proposal?",
                            "answer": true
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "qXObyw",
                    "question": "Will you use match funding for this proposal?"
                },
                {
                    "fields": [
                        {
                            "key": "uuyBff",
                            "type": "multiInput",
                            "title": "Match funding",
                            "answer": [
                                {
                                    "AfAKxk": "Test Match Funding NS Form",
                                    "CrcLtW": 1234,
                                    "ndySbC": "1 April 2023 to 31 March 2024",
                                    "pATWyM": "Capital",
                                    "sIFBGc": true
                                }
                            ]
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "qXObyw",
                    "question": "Match funding"
                }
            ]
        },
        {
            "name": "name-your-application-ns",
            "status": "COMPLETED",
            "questions": [
                {
                    "fields": [
                        {
                            "key": "YVsPtE",
                            "type": "text",
                            "title": "Application name",
                            "answer": "$project_name"
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "pCEnjo",
                    "question": "Name your application"
                }
            ]
        },
        {
            "name": "objectives-and-activities-ns",
            "status": "COMPLETED",
            "questions": [
                {
                    "fields": [
                        {
                            "key": "pWFwci",
                            "type": "freeText",
                            "title": "Give a brief summary of your project, including what you hope to achieve",
                            "answer": "<p>Test Objectives and Activities NS Form</p>"
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "VCtwUB",
                    "question": "Give a brief summary of your project, including what you hope to achieve"
                },
                {
                    "fields": [
                        {
                            "key": "kRxOHF",
                            "type": "multiInput",
                            "title": "Proposal milestones",
                            "answer": [
                                {
                                    "FbWEBY": "Test Objectives and Activities NS Form",
                                    "RXrpzV": "Test Objectives and Activities NS Form"
                                }
                            ]
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "VCtwUB",
                    "question": "Objectives and activities"
                }
            ]
        },
        {
            "name": "project-milestones-ns",
            "status": "COMPLETED",
            "questions": [
                {
                    "fields": [
                        {
                            "key": "sXlkAm",
                            "type": "multiInput",
                            "title": "Milestones",
                            "answer": [
                                {
                                    "PrulfI": {
                                        "PrulfI__year": 2023,
                                        "PrulfI__month": 6
                                    },
                                    "fFIuPP": "Test Project Milestones NS Form"
                                }
                            ]
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "KdUbsr",
                    "question": "Proposal milestones"
                }
            ]
        },
        {
            "name": "risk-and-deliverability-ns",
            "status": "COMPLETED",
            "questions": [
                {
                    "fields": [
                        {
                            "key": "xDpgOK",
                            "type": "multiInput",
                            "title": "Risk",
                            "answer": [
                                {
                                    "GVoNOE": "high",
                                    "SRHsAx": "Test Risk And Deliverability NS Form",
                                    "dmKRCF": "Test Risk And Deliverability NS Form"
                                }
                            ]
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "JOYYbl",
                    "question": "Risks to the proposal"
                }
            ]
        },
        {
            "name": "applicant-information-ns",
            "status": "COMPLETED",
            "questions": [
                {
                    "fields": [
                        {
                            "key": "fUMWcd",
                            "type": "text",
                            "title": "Name of lead contact",
                            "answer": "Test Applicant Information Form"
                        },
                        {
                            "key": "lZVkeg",
                            "type": "text",
                            "title": "Lead contact job title",
                            "answer": "Test Applicant Information Form"
                        },
                        {
                            "key": "CDEwxp",
                            "type": "text",
                            "title": "Lead contact email address",
                            "answer": "test@test.com"
                        },
                        {
                            "key": "DvBqCJ",
                            "type": "text",
                            "title": "Lead contact telephone number",
                            "answer": "0000000000"
                        },
                        {
                            "key": "ayzqnK",
                            "type": "list",
                            "title": "Is the lead contact the same person as the authorised signatory?",
                            "answer": true
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "ZbxIUV",
                    "question": "Lead contact details"
                }
            ]
        },
        {
            "name": "staff-and-volunteers-ns",
            "status": "COMPLETED",
            "questions": [
                {
                    "fields": [
                        {
                            "key": "bcJWbJ",
                            "type": "text",
                            "title": "How many staff members are currently employed in your organisation?",
                            "answer": "44"
                        },
                        {
                            "key": "pwPYdF",
                            "type": "text",
                            "title": "How many volunteers are actively involved in your organisation?",
                            "answer": "39"
                        },
                        {
                            "key": "VXKVmM",
                            "type": "text",
                            "title": "What percentage of your employed staff work part-time?",
                            "answer": "10%"
                        },
                        {
                            "key": "wOUNbF",
                            "type": "text",
                            "title": "For part-time employees, what is their average full-time equivalency (FTE)?",
                            "answer": "0.6"
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "ibsaRz",
                    "question": "Employed staff and volunteers at your organisation"
                }
            ]
        },
        {
            "name": "local-need-and-support-ns",
            "status": "COMPLETED",
            "questions": [
                {
                    "fields": [
                        {
                            "key": "nMfGTS",
                            "type": "freeText",
                            "title": "Tell us why your proposal is needed in your area",
                            "answer": "<p>Test Local Need And Support NS Form</p>"
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "vzkeMY",
                    "question": "Tell us why your proposal is needed in your area"
                },
                {
                    "fields": [
                        {
                            "key": "nURkuc",
                            "type": "text",
                            "title": "What is the name of the local authority where your proposal will be based?",
                            "answer": "$local_authority"
                        },
                        {
                            "key": "lFTgWk",
                            "type": "list",
                            "title": "Do you have the local authority's support and endorsement for your proposal?",
                            "answer": false
                        },
                        {
                            "key": "mIGfuL",
                            "type": "text",
                            "title": "Upload letter of endorsement from your local authority (optional)",
                            "answer": null
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "vzkeMY",
                    "question": "Local authority support"
                }
            ]
        },
        {
            "name": "joint-applications-ns",
            "status": "COMPLETED",
            "questions": [
                {
                    "fields": [
                        {
                            "key": "jsUbAI",
                            "type": "list",
                            "title": "Is your application a joint bid in partnership with other organisations?",
                            "answer": true
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "uFLqwl",
                    "question": "Is your application a joint bid in partnership with other organisations?"
                },
                {
                    "fields": [
                        {
                            "key": "oxMLrb",
                            "type": "multiInput",
                            "title": "Your partner organisations",
                            "answer": [
                                {
                                    "EFlBMr": "Test Joint Applications NS Form",
                                    "JFEJVf": "Test Joint Applications NS Form"
                                }
                            ]
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "uFLqwl",
                    "question": "Partner organisation details"
                }
            ]
        },
        {
            "name": "proposal-sustainability-ns",
            "status": "COMPLETED",
            "questions": [
                {
                    "fields": [
                        {
                            "key": "PEMJEy",
                            "type": "freeText",
                            "title": "How will this funding support the longer-term sustainability of your proposal beyond the funding period?",
                            "answer": "<p>Test Proposal Sustainability NS Form</p>"
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "LZWArS",
                    "question": "How will this funding support the longer-term sustainability of your proposal beyond the funding period?"
                }
            ]
        },
        {
            "name": "funding-required-ns",
            "status": "COMPLETED",
            "questions": [
                {
                    "fields": [
                        {
                            "key": "NxVqXd",
                            "type": "list",
                            "title": "What funding are you applying for?",
                            "answer": "$funding_type"
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "LABTna",
                    "question": "What funding are you applying for?"
                },
                {
                    "fields": [
                        {
                            "key": "GRWtfV",
                            "type": "text",
                            "title": "Both revenue and capital",
                            "answer": "$revenue_funding"
                        },
                        {
                            "key": "zvPzXN",
                            "type": "text",
                            "title": "Revenue for 1 April 2024 to 31 March 2025",
                            "answer": "$revenue_funding"
                        },
                        {
                            "key": "QUCvFy",
                            "type": "text",
                            "title": "Capital for 1 April 2023 to 31 March 2024",
                            "answer": "$capital_funding"
                        },
                        {
                            "key": "pppiYl",
                            "type": "text",
                            "title": "Capital for 1 April 2024 to 31 March 2025",
                            "answer": "$capital_funding"
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "LABTna",
                    "question": "How much funding are you applying for?"
                },
                {
                    "fields": [
                        {
                            "key": "mCbbyN",
                            "type": "multiInput",
                            "title": "Revenue costs",
                            "answer": [
                                {
                                    "TrTaZQ": "Test Funding Required NS Form",
                                    "dpDFgB": "Test Funding Required NS Form",
                                    "iZdZrr": 40,
                                    "leIxEX": "1 April 2023 to 31 March 2024"
                                }
                            ]
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "LABTna",
                    "question": "Revenue funding"
                },
                {
                    "fields": [
                        {
                            "key": "XsAoTv",
                            "type": "multiInput",
                            "title": "Capital costs",
                            "answer": [
                                {
                                    "JtBjFp": 50,
                                    "cpFthG": "Test Funding Required NS Form",
                                    "mmwzGc": "1 April 2024 to 31 March 2025",
                                    "pMffVz": null
                                }
                            ]
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "LABTna",
                    "question": "Capital funding"
                }
            ]
        },
        {
            "name": "organisation-information-ns",
            "status": "COMPLETED",
            "questions": [
                {
                    "fields": [
                        {
                            "key": "opFJRm",
                            "type": "text",
                            "title": "Organisation name",
                            "answer": "$org_name"
                        },
                        {
                            "key": "mhYQzL",
                            "type": "text",
                            "title": "Organisation address",
                            "answer": "Test Organisation Information NS Form, null, Test Organisation Information NS Form, null, $location_postcode"
                        },
                        {
                            "key": "AVShTf",
                            "type": "text",
                            "title": "Which region of England do you work in?",
                            "answer": "Test Organisation Information NS Form"
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "VoIhVi",
                    "question": "Organisation details"
                },
                {
                    "fields": [
                        {
                            "key": "BwbIlM",
                            "type": "freeText",
                            "title": "What is your organisation's main purpose?",
                            "answer": "<p>Test Organisation Information NS Form</p>"
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "VoIhVi",
                    "question": "What is your organisation's main purpose?"
                },
                {
                    "fields": [
                        {
                            "key": "RxbebZ",
                            "type": "freeText",
                            "title": "What are your organisation’s charitable objects?",
                            "answer": "<p>Test Organisation Information NS Form</p>"
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "VoIhVi",
                    "question": "What are your organisation’s charitable objects?"
                },
                {
                    "fields": [
                        {
                            "key": "YauUjZ",
                            "type": "text",
                            "title": "Annual turnover for 1 April 2022 to 31 March 2023",
                            "answer": "444"
                        },
                        {
                            "key": "zuCRBk",
                            "type": "text",
                            "title": "Annual turnover for 1 April 2021 to 31 March 2022",
                            "answer": "235"
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "VoIhVi",
                    "question": "What is your organisation's annual turnover?"
                },
                {
                    "fields": [
                        {
                            "key": "NENGMj",
                            "type": "list",
                            "title": "Which membership organisations are you a member of?",
                            "answer": "both"
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "VoIhVi",
                    "question": "Which membership organisations are you a member of?"
                }
            ]
        },
        {
            "name": "organisation-type-ns",
            "status": "COMPLETED",
            "questions": [
                {
                    "fields": [
                        {
                            "key": "ChXWIQ",
                            "type": "list",
                            "title": "How is your organisation classified?",
                            "answer": [
                                "none"
                            ]
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "qaFvvN",
                    "question": "How is your organisation classified?"
                },
                {
                    "fields": [
                        {
                            "key": "ETJaFn",
                            "type": "text",
                            "title": "How is your organisation classified?",
                            "answer": "Test Organisation Type Form"
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "qaFvvN",
                    "question": "How is your organisation classified?"
                },
                {
                    "fields": [
                        {
                            "key": "ILVEOG",
                            "type": "multiInput",
                            "title": "Your trustees or committee members",
                            "answer": [
                                {
                                    "mrCotx": "Test Organisation Type Form"
                                }
                            ]
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "qaFvvN",
                    "question": "Names of trustees or committee members"
                },
                {
                    "fields": [
                        {
                            "key": "TgBzyM",
                            "type": "list",
                            "title": "How long has your organisation been operating?",
                            "answer": "more-than-2-years-but-less-than-3"
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "qaFvvN",
                    "question": "How long has your organisation been operating?"
                },
                {
                    "fields": [
                        {
                            "key": "sVlFcN",
                            "type": "text",
                            "title": "Upload your organisation's annual accounts that you have available",
                            "answer": "sample.txt"
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "qaFvvN",
                    "question": "Upload your organisation's annual accounts that you have available"
                }
            ]
        },
        {
            "name": "current-services-ns",
            "status": "COMPLETED",
            "questions": [
                {
                    "fields": [
                        {
                            "key": "QOlbCV",
                            "type": "list",
                            "title": "Have you provided a night shelter or emergency accommodation on or after 1 April 2019?",
                            "answer": true
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "xigWzk",
                    "question": "Have you provided a night shelter or emergency accommodation on or after 1 April 2019?"
                },
                {
                    "fields": [
                        {
                            "key": "affVbH",
                            "type": "list",
                            "title": "Is the night shelter or emergency accommodation communal?",
                            "answer": true
                        },
                        {
                            "key": "ttEOXi",
                            "type": "list",
                            "title": "Is the night shelter or emergency accommodation single room accommodation?",
                            "answer": true
                        },
                        {
                            "key": "dSdeYa",
                            "type": "text",
                            "title": "How many bed spaces did the night shelter or emergency accommodation provide from 1 April 2022 to 31 March 2023?",
                            "answer": "323"
                        },
                        {
                            "key": "gXvnZA",
                            "type": "list",
                            "title": "Is the night shelter or emergency accommodation used for SWEP (severe weather emergency protocol)?",
                            "answer": false
                        },
                        {
                            "key": "vStFMu",
                            "type": "list",
                            "title": "Do you accept referrals from the local authority or other agencies for available bed spaces?",
                            "answer": false
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "xigWzk",
                    "question": "Night shelter or emergency accommodation"
                },
                {
                    "fields": [
                        {
                            "key": "YyMRdP",
                            "type": "text",
                            "title": "How many nights did the night shelter or emergency accommodation open from 1 April 2022 to 31 March 2023?",
                            "answer": "7"
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "xigWzk",
                    "question": "How many nights did the night shelter or emergency accommodation open from 1 April 2022 to 31 March 2023?"
                },
                {
                    "fields": [
                        {
                            "key": "STfdvD",
                            "type": "list",
                            "title": "Do you currently provide day provision?",
                            "answer": true
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "xigWzk",
                    "question": "Do you currently provide day provision?"
                },
                {
                    "fields": [
                        {
                            "key": "bCXNtj",
                            "type": "monthYear",
                            "title": "When did you start providing day provision?",
                            "answer": "2023-06"
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "xigWzk",
                    "question": "When did you start providing day provision?"
                },
                {
                    "fields": [
                        {
                            "key": "ULPcAU",
                            "type": "list",
                            "title": "Which day provision services are you currently providing?",
                            "answer": [
                                "other"
                            ]
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "xigWzk",
                    "question": "Which day provision services are you currently providing?"
                },
                {
                    "fields": [
                        {
                            "key": "zwQHCl",
                            "type": "freeText",
                            "title": "Which other day provision do you currently provide?",
                            "answer": "<p>Test Current Services NS Form</p>"
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "xigWzk",
                    "question": "Which other day provision do you currently provide?"
                },
                {
                    "fields": [
                        {
                            "key": "GBfYfn",
                            "type": "list",
                            "title": "Do you currently provide any other services?",
                            "answer": true
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "xigWzk",
                    "question": "Do you currently provide any other services?"
                },
                {
                    "fields": [
                        {
                            "key": "wViAiU",
                            "type": "freeText",
                            "title": "What other services are you currently providing?",
                            "answer": "<p>Test Current Services NS Form</p>"
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "xigWzk",
                    "question": "What other services are you currently providing?"
                },
                {
                    "fields": [
                        {
                            "key": "umAyqH",
                            "type": "list",
                            "title": "Do you currently provide specialist support?",
                            "answer": true
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "xigWzk",
                    "question": "Do you currently provide specialist support?"
                },
                {
                    "fields": [
                        {
                            "key": "JCUQcR",
                            "type": "list",
                            "title": "Who do you currently provide targeted specialist support to?",
                            "answer": [
                                "women"
                            ]
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "xigWzk",
                    "question": "Who do you currently provide targeted specialist support to?"
                }
            ]
        },
        {
            "name": "building-works-ns",
            "status": "COMPLETED",
            "questions": [
                {
                    "fields": [
                        {
                            "key": "lifPop",
                            "type": "list",
                            "title": "Will you use the funding to conduct building works?",
                            "answer": true
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "EDNaie",
                    "question": "Will you use the funding to conduct building works?"
                },
                {
                    "fields": [
                        {
                            "key": "fmcTtE",
                            "type": "text",
                            "title": "Number of new single room units (optional)",
                            "answer": "344"
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "EDNaie",
                    "question": "Number of new single room units (optional)"
                },
                {
                    "fields": [
                        {
                            "key": "xGnWEW",
                            "type": "list",
                            "title": "Do you need planning approval for your proposal?",
                            "answer": "yes"
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "EDNaie",
                    "question": "Do you need planning approval for your proposal?"
                },
                {
                    "fields": [
                        {
                            "key": "KhISvR",
                            "type": "list",
                            "title": "Have you made an application for planning permission?",
                            "answer": false
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "EDNaie",
                    "question": "Have you made an application for planning permission?"
                },
                {
                    "fields": [
                        {
                            "key": "YFPgTB",
                            "type": "list",
                            "title": "Have you received any pre-application planning advice?",
                            "answer": true
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "EDNaie",
                    "question": "Have you received any pre-application planning advice?"
                },
                {
                    "fields": [
                        {
                            "key": "mADkNz",
                            "type": "text",
                            "title": "Give a brief summary of the advice you received",
                            "answer": "Test Building Works NS Form"
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "EDNaie",
                    "question": "Give a brief summary of the advice you received"
                },
                {
                    "fields": [
                        {
                            "key": "AYDIPX",
                            "type": "list",
                            "title": "Will you procure a construction contract for the building works?",
                            "answer": true
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "EDNaie",
                    "question": "Will you procure a construction contract for the building works?"
                },
                {
                    "fields": [
                        {
                            "key": "nyusrL",
                            "type": "list",
                            "title": "Will you use any professional advisors for the proposal?",
                            "answer": true
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "EDNaie",
                    "question": "Will you use any professional advisors for the proposal?"
                },
                {
                    "fields": [
                        {
                            "key": "SQEpBt",
                            "type": "multiInput",
                            "title": "Details of professional advisors",
                            "answer": [
                                {
                                    "cbYcqS": "Test Building Works NS Form",
                                    "muRwiL": "Test Building Works NS Form"
                                }
                            ]
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "EDNaie",
                    "question": "Details of professional advisors"
                },
                {
                    "fields": [
                        {
                            "key": "rYAgMN",
                            "type": "list",
                            "title": "Will you be hiring contractors to complete the building works?",
                            "answer": false
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "EDNaie",
                    "question": "Will you be hiring contractors to complete the building works?"
                },
                {
                    "fields": [
                        {
                            "key": "wUFaUF",
                            "type": "list",
                            "title": "Do you have a cost estimate for the building works?",
                            "answer": true
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "EDNaie",
                    "question": "Do you have a cost estimate for the building works?"
                },
                {
                    "fields": [
                        {
                            "key": "NOMwBb",
                            "type": "text",
                            "title": "Upload cost estimate",
                            "answer": "sample.txt"
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "EDNaie",
                    "question": "Upload cost estimate"
                },
                {
                    "fields": [
                        {
                            "key": "ZmYhgR",
                            "type": "list",
                            "title": "Do you have a condition survey?",
                            "answer": true
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "EDNaie",
                    "question": "Do you have a condition survey?"
                },
                {
                    "fields": [
                        {
                            "key": "aTxAPP",
                            "type": "text",
                            "title": "Upload a condition survey",
                            "answer": "sample.txt"
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "EDNaie",
                    "question": "Upload a condition survey"
                },
                {
                    "fields": [
                        {
                            "key": "SdwIUb",
                            "type": "list",
                            "title": "Do you have a buildings and contents insurance certificate?",
                            "answer": true
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "EDNaie",
                    "question": "Do you have a buildings and contents insurance certificate?"
                },
                {
                    "fields": [
                        {
                            "key": "NlDVCg",
                            "type": "text",
                            "title": "Upload buildings and contents insurance certificate",
                            "answer": "sample.txt"
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "EDNaie",
                    "question": "Upload buildings and contents insurance certificate"
                },
                {
                    "fields": [
                        {
                            "key": "RXIYZY",
                            "type": "list",
                            "title": "Do you own the premises?",
                            "answer": false
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "EDNaie",
                    "question": "Do you own the premises?"
                },
                {
                    "fields": [
                        {
                            "key": "rMvZDG",
                            "type": "text",
                            "title": "Upload the land owner's consent",
                            "answer": "sample.txt"
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "EDNaie",
                    "question": "Upload the land owner's consent"
                },
                {
                    "fields": [
                        {
                            "key": "muhnok",
                            "type": "list",
                            "title": "How long is left on the lease agreement?",
                            "answer": "less-than-4-years"
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "EDNaie",
                    "question": "How long is left on the lease agreement?"
                },
                {
                    "fields": [
                        {
                            "key": "GLOpmu",
                            "type": "text",
                            "title": "Upload correspondence from your landlord to show that lease renewal discussions have started",
                            "answer": "sample.txt"
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "EDNaie",
                    "question": "Upload correspondence from your landlord to show that lease renewal discussions have started"
                },
                {
                    "fields": [
                        {
                            "key": "kQJIbS",
                            "type": "text",
                            "title": "Upload heads of terms outlining new lease agreement",
                            "answer": "sample.txt"
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "EDNaie",
                    "question": "Upload heads of terms outlining new lease agreement"
                },
                {
                    "fields": [
                        {
                            "key": "skBfqS",
                            "type": "list",
                            "title": "Is the building listed?",
                            "answer": true
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "EDNaie",
                    "question": "Is the building listed?"
                },
                {
                    "fields": [
                        {
                            "key": "abdbzq",
                            "type": "text",
                            "title": "Upload listed building consent",
                            "answer": "sample.txt"
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "EDNaie",
                    "question": "Upload listed building consent"
                }
            ]
        }
    ]
}
"""
)

cypr1_application_store_json_template = Template(
    """
{
  "id": "$app_id",
  "status": "SUBMITTED",
  "fund_id": "$fund_id",
  "language": "en",
  "round_id": "$round_id",
  "reference": "$short_ref",
  "account_id": "2f82785f-f207-4f80-aed3-be0a17be161a",
  "round_name": "Round 1",
  "started_at": "2023-09-26T13:42:54.933640",
  "last_edited": "2023-09-26T13:51:31.987290",
  "project_name": "$project_name",
  "date_submitted": "2023-09-26T13:52:12.186807",
  "forms": [
    {
      "name": "risk-and-deliverability-cyp",
      "questions": [
        {
          "category": "hhbMar",
          "fields": [
            {
              "answer": [
                {
                  "CzoasH": "test",
                  "MPHvIr": "Medium",
                  "SKQluJ": "test",
                  "eADHGN": "High"
                }
              ],
              "key": "qQLYzL",
              "title": "Risks to the project",
              "type": "multiInput"
            }
          ],
          "index": 0,
          "question": "Risks to the project",
          "status": "COMPLETED"
        },
        {
          "category": "hhbMar",
          "fields": [
            {
              "answer": "test",
              "key": "KHESdE",
              "title": "Who is owns the overall risk register?",
              "type": "text"
            }
          ],
          "index": 0,
          "question": "Who owns for the overall risk register?",
          "status": "COMPLETED"
        },
        {
          "category": "hhbMar",
          "fields": [
            {
              "answer": "<p>tsst</p>",
              "key": "KHESFr",
              "title": "Tell us about your organisation's governance structure",
              "type": "freeText"
            }
          ],
          "index": 0,
          "question": "Tell us about your organisation's governance structure",
          "status": "COMPLETED"
        },
        {
          "category": null,
          "fields": [
            {
              "answer": true,
              "key": "markAsComplete",
              "title": "Do you want to mark this section as complete?",
              "type": "boolean"
            }
          ],
          "question": "MarkAsComplete",
          "status": "COMPLETED"
        }
      ],
      "status": "COMPLETED"
    },
    {
      "name": "location-of-activities-cyp",
      "questions": [
        {
          "category": "wxOzRK",
          "fields": [
            {
              "answer": true,
              "key": "iqqqTk",
              "title": "Is the project taking place regionally?",
              "type": "list"
            }
          ],
          "index": 0,
          "question": "Is the project taking place regionally?",
          "status": "COMPLETED"
        },
        {
          "category": "wxOzRK",
          "fields": [
            {
              "answer": [
                {
                  "kaQUSV": "test"
                }
              ],
              "key": "tApPKx",
              "title": "Which local authority areas will you work across?",
              "type": "multiInput"
            }
          ],
          "index": 0,
          "question": "Which local authority areas will you work across?",
          "status": "COMPLETED"
        },
        {
          "category": null,
          "fields": [
            {
              "answer": true,
              "key": "markAsComplete",
              "title": "Do you want to mark this section as complete?",
              "type": "boolean"
            }
          ],
          "question": "MarkAsComplete",
          "status": "COMPLETED"
        }
      ],
      "status": "COMPLETED"
    },
    {
      "name": "skills-and-experience-cyp",
      "questions": [
        {
          "category": "pyQhSV",
          "fields": [
            {
              "answer": false,
              "key": "HrGXKi",
              "title": "Have you delivered projects like this before?",
              "type": "list"
            }
          ],
          "index": 0,
          "question": "Have you delivered projects like this before?",
          "status": "COMPLETED"
        },
        {
          "category": null,
          "fields": [
            {
              "answer": true,
              "key": "markAsComplete",
              "title": "Do you want to mark this section as complete?",
              "type": "boolean"
            }
          ],
          "question": "MarkAsComplete",
          "status": "COMPLETED"
        }
      ],
      "status": "COMPLETED"
    },
    {
      "name": "applicant-information-cyp",
      "questions": [
        {
          "category": "pyQsHV",
          "fields": [
            {
              "answer": "Tester",
              "key": "rKHBnt",
              "title": "Name of lead contact",
              "type": "text"
            },
            {
              "answer": "Data",
              "key": "yWtfkb",
              "title": "Alternative name",
              "type": "text"
            },
            {
              "answer": "Test Engineer",
              "key": "kbOHaM",
              "title": "Lead contact job title",
              "type": "text"
            },
            {
              "answer": "test@test.com",
              "key": "BKOHaM",
              "title": "Lead contact email address",
              "type": "text"
            },
            {
              "answer": "00000111111",
              "key": "CyANDT",
              "title": "Lead contact telephone number",
              "type": "text"
            },
            {
              "answer": true,
              "key": "DbFHbD",
              "title": "Is the lead contact the same person as the authorised signatory?",
              "type": "list"
            }
          ],
          "index": 0,
          "question": "Lead contact details",
          "status": "COMPLETED"
        },
        {
          "category": null,
          "fields": [
            {
              "answer": true,
              "key": "markAsComplete",
              "title": "Do you want to mark this section as complete?",
              "type": "boolean"
            }
          ],
          "question": "MarkAsComplete",
          "status": "COMPLETED"
        }
      ],
      "status": "COMPLETED"
    },
    {
      "name": "existing-work-cyp",
      "questions": [
        {
          "category": "PPssHV",
          "fields": [
            {
              "answer": "<p>test</p>",
              "key": "MbDkNZ",
              "title": "How will you avoid duplicating existing work or projects in this area?",
              "type": "freeText"
            }
          ],
          "index": 0,
          "question": "How will you avoid duplicating existing work or projects in this area?",
          "status": "COMPLETED"
        },
        {
          "category": null,
          "fields": [
            {
              "answer": true,
              "key": "markAsComplete",
              "title": "Do you want to mark this section as complete?",
              "type": "boolean"
            }
          ],
          "question": "MarkAsComplete",
          "status": "COMPLETED"
        }
      ],
      "status": "COMPLETED"
    },
    {
      "name": "project-milestones-cyp",
      "questions": [
        {
          "category": "zACCPu",
          "fields": [
            {
              "answer": [
                {
                  "HpLJDu": "milestone",
                  "LZbOBu": {
                    "LZbOBu__month": 3,
                    "LZbOBu__year": 2022
                  }
                }
              ],
              "key": "tAoOKx",
              "title": "Project milestones",
              "type": "multiInput"
            }
          ],
          "index": 0,
          "question": "Project milestones",
          "status": "COMPLETED"
        },
        {
          "category": null,
          "fields": [
            {
              "answer": true,
              "key": "markAsComplete",
              "title": "Do you want to mark this section as complete?",
              "type": "boolean"
            }
          ],
          "question": "MarkAsComplete",
          "status": "COMPLETED"
        }
      ],
      "status": "COMPLETED"
    },
    {
      "name": "name-your-application-cyp",
      "questions": [
        {
          "category": "XDnkqz",
          "fields": [
            {
              "answer": "$project_name",
              "key": "bsUoNG",
              "title": "Name your application",
              "type": "text"
            }
          ],
          "index": 0,
          "question": "Name your application",
          "status": "COMPLETED"
        },
        {
          "category": null,
          "fields": [
            {
              "answer": true,
              "key": "markAsComplete",
              "title": "Do you want to mark this section as complete?",
              "type": "boolean"
            }
          ],
          "question": "MarkAsComplete",
          "status": "COMPLETED"
        }
      ],
      "status": "COMPLETED"
    },
    {
      "name": "value-for-money-cyp",
      "questions": [
        {
          "category": "xYdwyD",
          "fields": [
            {
              "answer": "$revenue_funding",
              "key": "JXKUcj",
              "title": "27 September 2023 to 31 March 2024",
              "type": "text"
            },
            {
              "answer": "$revenue_funding",
              "key": "OnPeeS",
              "title": "1 April 2024 to 31 March 2025",
              "type": "text"
            }
          ],
          "index": 0,
          "question": "Funding requested",
          "status": "COMPLETED"
        },
        {
          "category": "xYdwyD",
          "fields": [
            {
              "answer": [
                {
                  "JizgZP": $revenue_funding,
                  "gLQlyJ": "test",
                  "kjuHtl": "1 April 2024 to 31 March 2025"
                }
              ],
              "key": "qwktzL",
              "title": "Item of expenditure",
              "type": "multiInput"
            }
          ],
          "index": 0,
          "question": "Item of expenditure",
          "status": "COMPLETED"
        },
        {
          "category": "xYdwyD",
          "fields": [
            {
              "answer": true,
              "key": "qwktlZ",
              "title": "Will you use additional funding for your project?",
              "type": "list"
            }
          ],
          "index": 0,
          "question": "Will you use additional funding for your project?",
          "status": "COMPLETED"
        },
        {
          "category": "xYdwyD",
          "fields": [
            {
              "answer": [
                {
                  "HpLJyL": {
                    "HpLJyL__month": 3,
                    "HpLJyL__year": 2022
                  },
                  "MadvIr": "Capital",
                  "gLqiyJ": "test",
                  "yuzbjT": 3
                }
              ],
              "key": "qqktzL",
              "title": "Funding source",
              "type": "multiInput"
            }
          ],
          "index": 0,
          "question": "Additional funding",
          "status": "COMPLETED"
        },
        {
          "category": null,
          "fields": [
            {
              "answer": true,
              "key": "markAsComplete",
              "title": "Do you want to mark this section as complete?",
              "type": "boolean"
            }
          ],
          "question": "MarkAsComplete",
          "status": "COMPLETED"
        }
      ],
      "status": "COMPLETED"
    },
    {
      "name": "declarations-cyp",
      "questions": [
        {
          "category": "OEGHno",
          "fields": [
            {
              "answer": true,
              "key": "sdeLyR",
              "title": "Confirm your organisation adheres to the government code of conduct",
              "type": "list"
            },
            {
              "answer": true,
              "key": "SUTxtj",
              "title": "Confirm your organisation has a data handling process in place",
              "type": "list"
            },
            {
              "answer": false,
              "key": "WWHYDI",
              "title": "Confirm you have a bank account set up and associated with the organisation you are applying on behalf of",
              "type": "list"
            },
            {
              "answer": true,
              "key": "WGmcyu",
              "title": "Confirm that your organisation's safegaurding policies are up to date",
              "type": "list"
            },
            {
              "answer": false,
              "key": "WGmDZu",
              "title": "Confirm that the information you've provided in this application is accurate to the best of your knowledge on the date of submission",
              "type": "list"
            }
          ],
          "index": 0,
          "question": "Agree to the final confirmations",
          "status": "COMPLETED"
        },
        {
          "category": null,
          "fields": [
            {
              "answer": true,
              "key": "markAsComplete",
              "title": "Do you want to mark this section as complete?",
              "type": "boolean"
            }
          ],
          "question": "MarkAsComplete",
          "status": "COMPLETED"
        }
      ],
      "status": "COMPLETED"
    },
    {
      "name": "working-with-fund-beneficiaries-cyp",
      "questions": [
        {
          "category": "Nyppws",
          "fields": [
            {
              "answer": "<p>test</p>",
              "key": "XPDbsh",
              "title": "Tell us how you will identify and work with the intended fund beneficiaries",
              "type": "freeText"
            }
          ],
          "index": 0,
          "question": "Tell us how you will identify and work with the intended fund beneficiaries",
          "status": "COMPLETED"
        },
        {
          "category": null,
          "fields": [
            {
              "answer": true,
              "key": "markAsComplete",
              "title": "Do you want to mark this section as complete?",
              "type": "boolean"
            }
          ],
          "question": "MarkAsComplete",
          "status": "COMPLETED"
        }
      ],
      "status": "COMPLETED"
    },
    {
      "name": "about-your-organisation-cyp",
      "questions": [
        {
          "category": "uLwBuz",
          "fields": [
            {
              "answer": "$org_name",
              "key": "JbmcJE",
              "title": "Organisation name",
              "type": "text"
            },
            {
              "answer": false,
              "key": "KUdOhN",
              "title": "Does your organisation use any other names?",
              "type": "list"
            }
          ],
          "index": 0,
          "question": "Organisation details",
          "status": "COMPLETED"
        },
        {
          "category": "uLwBuz",
          "fields": [
            {
              "answer": "<p>test</p>",
              "key": "kxgOne",
              "title": "Activity 1",
              "type": "freeText"
            },
            {
              "answer": null,
              "key": "kxgTwo",
              "title": "Activity 2 (optional)",
              "type": "freeText"
            },
            {
              "answer": null,
              "key": "kxgThr",
              "title": "Activity 3 (optional)",
              "type": "freeText"
            }
          ],
          "index": 0,
          "question": "Tell us about your organisation's main activities",
          "status": "COMPLETED"
        },
        {
          "category": "uLwBuz",
          "fields": [
            {
              "answer": "other",
              "key": "jcmcJE",
              "title": "Organisation classification",
              "type": "list"
            }
          ],
          "index": 0,
          "question": "How is your organisation classified?",
          "status": "COMPLETED"
        },
        {
          "category": "uLwBuz",
          "fields": [
            {
              "answer": "test",
              "key": "jemcJE",
              "title": "How is your organisation classified?",
              "type": "text"
            }
          ],
          "index": 0,
          "question": "How is your organisation classified? (other)",
          "status": "COMPLETED"
        },
        {
          "category": "uLwBuz",
          "fields": [
            {
              "answer": "test, null, te3 2nf, null, $location_postcode",
              "key": "rmBPvK",
              "title": "Registered organisation address",
              "type": "text"
            }
          ],
          "index": 0,
          "question": "Registered organisation address",
          "status": "COMPLETED"
        },
        {
          "category": "uLwBuz",
          "fields": [
            {
              "answer": null,
              "key": "smBPvK",
              "title": "Alternative organisation address",
              "type": "text"
            }
          ],
          "index": 0,
          "question": "Alternative organisation address (optional)",
          "status": "COMPLETED"
        },
        {
          "category": "uLwBuz",
          "fields": [
            {
              "answer": true,
              "key": "MRdGKt",
              "title": "Is your application a joint bid in partnership with other organisations?",
              "type": "list"
            }
          ],
          "index": 0,
          "question": "Is your application a joint bid in partnership with other organisations?",
          "status": "COMPLETED"
        },
        {
          "category": "uLwBuz",
          "fields": [
            {
              "answer": [
                {
                  "GpLJDu": "test",
                  "IXjMWp": {
                    "addressLine1": "test",
                    "addressLine2": "",
                    "county": "",
                    "postcode": "te4 2nf",
                    "town": "test "
                  },
                  "MKbOlA": "https://forms.test.gids.dev/about-your-organisation-cyp/partner-organisation-details?form_session_identifier=1ed50390-dc21-4838-97c7-f054e4e5a475",
                  "OghGGr": null,
                  "RphKTp": null
                }
              ],
              "key": "tZoOKx",
              "title": "Partner organisation details",
              "type": "multiInput"
            }
          ],
          "index": 0,
          "question": "Partner organisation details",
          "status": "COMPLETED"
        },
        {
          "category": "uLwBuz",
          "fields": [
            {
              "answer": "<p>test</p>",
              "key": "xPcbJX",
              "title": "Tell us about how you plan to work with the partner organisations",
              "type": "freeText"
            }
          ],
          "index": 0,
          "question": "Tell us about how you plan to work with the partner organisations",
          "status": "COMPLETED"
        },
        {
          "category": "uLwBuz",
          "fields": [
            {
              "answer": true,
              "key": "RUdOhN",
              "title": "Does an agreement currently exists between your organisations and the partnership organisations?",
              "type": "list"
            }
          ],
          "index": 0,
          "question": "Does an agreement currently exists between your organisations and the partnership organisations?",
          "status": "COMPLETED"
        },
        {
          "category": "uLwBuz",
          "fields": [
            {
              "answer": [
                {
                  "EShKlA": "https://forms.test.gids.dev/about-your-organisation-cyp/partner-organisation-details?form_session_identifier=1ed50390-dc21-4838-97c7-f054e4e5a475"
                }
              ],
              "key": "tYoOqx",
              "title": "Website and social media",
              "type": "multiInput"
            }
          ],
          "index": 0,
          "question": "Website and social media",
          "status": "COMPLETED"
        },
        {
          "category": null,
          "fields": [
            {
              "answer": true,
              "key": "markAsComplete",
              "title": "Do you want to mark this section as complete?",
              "type": "boolean"
            }
          ],
          "question": "MarkAsComplete",
          "status": "COMPLETED"
        }
      ],
      "status": "COMPLETED"
    },
    {
      "name": "outputs-and-outcomes-cyp",
      "questions": [
        {
          "category": "vhPnrc",
          "fields": [
            {
              "answer": "<p>test</p>",
              "key": "MADkNZ",
              "title": "Give a brief summary of your project, including what you hope to achieve",
              "type": "freeText"
            }
          ],
          "index": 0,
          "question": "Give a brief summary of your project, including what you hope to achieve",
          "status": "COMPLETED"
        },
        {
          "category": "vhPnrc",
          "fields": [
            {
              "answer": "<p>test</p>",
              "key": "nbDkNZ",
              "title": "How will you measure the outcome of your project?",
              "type": "freeText"
            }
          ],
          "index": 0,
          "question": "How will you measure the outcome of your project?",
          "status": "COMPLETED"
        },
        {
          "category": "vhPnrc",
          "fields": [
            {
              "answer": [
                "maintaining-links-to-culture"
              ],
              "key": "fHodTO",
              "title": "What is the main focus of your project?",
              "type": "list"
            }
          ],
          "index": 0,
          "question": "What is the main focus of your project?",
          "status": "COMPLETED"
        },
        {
          "category": "vhPnrc",
          "fields": [
            {
              "answer": [
                "ukrainian-schemes"
              ],
              "key": "vYYoAC",
              "title": "Which cohort will your project focus on?",
              "type": "list"
            }
          ],
          "index": 0,
          "question": "Which cohort will your project focus on?",
          "status": "COMPLETED"
        },
        {
          "category": "vhPnrc",
          "fields": [
            {
              "answer": "444",
              "key": "tAtJGz",
              "title": "How many fund recipients from the Ukraine schemes do you expect your project to support with the funding?",
              "type": "text"
            }
          ],
          "index": 0,
          "question": "How many fund recipients from the Ukraine schemes do you expect your project to support with the funding?",
          "status": "COMPLETED"
        },
        {
          "category": null,
          "fields": [
            {
              "answer": true,
              "key": "markAsComplete",
              "title": "Do you want to mark this section as complete?",
              "type": "boolean"
            }
          ],
          "question": "MarkAsComplete",
          "status": "COMPLETED"
        }
      ],
      "status": "COMPLETED"
    },
    {
      "name": "objectives-and-activities-cyp",
      "questions": [
        {
          "category": "zzpzem",
          "fields": [
            {
              "answer": [
                {
                  "HpLJCu": "test",
                  "kaQUfV": "test"
                }
              ],
              "key": "tAoPKx",
              "title": "Project milestones",
              "type": "multiInput"
            }
          ],
          "index": 0,
          "question": "Objectives and activities",
          "status": "COMPLETED"
        },
        {
          "category": null,
          "fields": [
            {
              "answer": true,
              "key": "markAsComplete",
              "title": "Do you want to mark this section as complete?",
              "type": "boolean"
            }
          ],
          "question": "MarkAsComplete",
          "status": "COMPLETED"
        }
      ],
      "status": "COMPLETED"
    }
  ]
}
"""
)

dpifr2_application_store_json_template = Template(
    """
{
  "id": "$app_id",
  "status": "SUBMITTED",
  "fund_id": "$fund_id",
  "language": "en",
  "round_id": "$round_id",
  "reference": "$short_ref",
  "account_id": "2f82785f-f207-4f80-aed3-be0a17be161a",
  "round_name": "Round 1",
  "started_at": "2023-09-26T13:42:54.933640",
  "last_edited": "2023-09-26T13:51:31.987290",
  "project_name": "$project_name",
  "date_submitted": "2023-09-26T13:52:12.186807",
  "forms": [
    {
      "name": "name-your-application",
      "questions": [
        {
          "category": "ScxYon",
          "fields": [
            {
              "answer": "Test Application Name",
              "key": "JAAhRP",
              "title": "Name your application",
              "type": "text"
            }
          ],
          "index": 0,
          "question": "1.1 Name your application",
          "status": "COMPLETED"
        },
        {
          "category": null,
          "fields": [
            {
              "answer": true,
              "key": "markAsComplete",
              "title": "Do you want to mark this section as complete?",
              "type": "boolean"
            }
          ],
          "question": "MarkAsComplete",
          "status": "COMPLETED"
        }
      ],
      "status": "COMPLETED"
    },
    {
      "name": "organisation-information-dpi",
      "questions": [
        {
          "category": "TFJTit",
          "fields": [
            {
              "answer": "$org_name",
              "key": "nYJiWy",
              "title": "Organisation name",
              "type": "text"
            }
          ],
          "index": 0,
          "question": "Organisation name",
          "status": "COMPLETED"
        },
        {
          "category": "TFJTit",
          "fields": [
            {
              "answer": "Version 1 Sponsor team",
              "key": "uYsivE",
              "title": "Name of project sponsor",
              "type": "text"
            },
            {
              "answer": "test@test.com",
              "key": "xgrxxv",
              "title": "Project sponsor email address",
              "type": "text"
            },
            {
              "answer": "12345678901",
              "key": "xbOBdn",
              "title": "Project sponsor telephone number",
              "type": "text"
            }
          ],
          "index": 0,
          "question": "Project sponsor details",
          "status": "COMPLETED"
        },
        {
          "category": "TFJTit",
          "fields": [
            {
              "answer": "Burt",
              "key": "cPpwET",
              "title": "Name of section 151 officer",
              "type": "text"
            },
            {
              "answer": "burt@reynolds.com",
              "key": "EMukio",
              "title": "Section 151 officer email address",
              "type": "text"
            },
            {
              "answer": "25469874562",
              "key": "GPxiGe",
              "title": "Section 151 officer telephone number",
              "type": "text"
            }
          ],
          "index": 0,
          "question": "Section 151 officer details",
          "status": "COMPLETED"
        },
        {
          "category": "TFJTit",
          "fields": [
            {
              "answer": "Gommez Addams",
              "key": "AYmilW",
              "title": "Name of lead contact",
              "type": "text"
            },
            {
              "answer": "Dev",
              "key": "UjZJtC",
              "title": "Lead contact job title",
              "type": "text"
            },
            {
              "answer": "gommez@adams.com",
              "key": "IRugBv",
              "title": "Lead contact email address",
              "type": "text"
            },
            {
              "answer": "5656854682132",
              "key": "jvfZpA",
              "title": "Lead contact telephone number",
              "type": "text"
            }
          ],
          "index": 0,
          "question": "Lead contact details",
          "status": "COMPLETED"
        },
        {
          "category": null,
          "fields": [
            {
              "answer": true,
              "key": "markAsComplete",
              "title": "Do you want to mark this section as complete?",
              "type": "boolean"
            }
          ],
          "question": "MarkAsComplete",
          "status": "COMPLETED"
        }
      ],
      "status": "COMPLETED"
    },
    {
      "name": "declarations-dpi",
      "questions": [
        {
          "category": "HgUinB",
          "fields": [
            {
              "answer": true,
              "key": "JUgCya",
              "title": "You have signed the Local Digital Declaration and agree to follow the 5 core principles",
              "type": "list"
            },
            {
              "answer": true,
              "key": "vbmqwB",
              "title": "Your section 151 officer consents to the funds being carried over and spent in the next financial year (March 2024-25) and beyond if deemed necessary in project budget planning",
              "type": "list"
            },
            {
              "answer": true,
              "key": "EQffUz",
              "title": "You agree to let all outputs from this work be published under open licence with a view to any organisation accessing, using or adopting them freely",
              "type": "list"
            },
            {
              "answer": true,
              "key": "kPYiQE",
              "title": "The information you have provided is accurate",
              "type": "list"
            }
          ],
          "index": 0,
          "question": "Agree to the final confirmations",
          "status": "COMPLETED"
        },
        {
          "category": null,
          "fields": [
            {
              "answer": true,
              "key": "markAsComplete",
              "title": "Do you want to mark this section as complete?",
              "type": "boolean"
            }
          ],
          "question": "MarkAsComplete",
          "status": "COMPLETED"
        }
      ],
      "status": "COMPLETED"
    },
    {
      "name": "your-skills-and-experience-dpi",
      "questions": [
        {
          "category": "akREtH",
          "fields": [
            {
              "answer": true,
              "key": "rGADMs",
              "title": "Has your organisation delivered projects like this before?",
              "type": "list"
            }
          ],
          "index": 0,
          "question": "Has your organisation delivered projects like this before?",
          "status": "COMPLETED"
        },
        {
          "category": "akREtH",
          "fields": [
            {
              "answer": "<p>This is a bunch of test text</p>",
              "key": "zHgZBx",
              "title": "Tell us about how your organisation has worked on similar previous projects",
              "type": "freeText"
            }
          ],
          "index": 0,
          "question": "Tell us about how your organisation has worked on similar previous projects",
          "status": "COMPLETED"
        },
        {
          "category": null,
          "fields": [
            {
              "answer": true,
              "key": "markAsComplete",
              "title": "Do you want to mark this section as complete?",
              "type": "boolean"
            }
          ],
          "question": "MarkAsComplete",
          "status": "COMPLETED"
        }
      ],
      "status": "COMPLETED"
    },
    {
      "name": "roles-and-recruitment-dpi",
      "questions": [
        {
          "category": "nJcRTz",
          "fields": [
            {
              "answer": true,
              "key": "vuZiab",
              "title": "Do you have a team in place ready to deliver the project?",
              "type": "list"
            }
          ],
          "index": 0,
          "question": "Do you have a team in place ready to deliver the project?",
          "status": "COMPLETED"
        },
        {
          "category": "nJcRTz",
          "fields": [
            {
              "answer": "<p>this is&nbsp; some test text</p>",
              "key": "OPOrME",
              "title": "Tell us about the shape of the project team",
              "type": "freeText"
            }
          ],
          "index": 0,
          "question": "Tell us about the shape of the project team",
          "status": "COMPLETED"
        },
        {
          "category": "nJcRTz",
          "fields": [
            {
              "answer": true,
              "key": "gSQPxs",
              "title": "Will you need to backfill any roles in your organisation?",
              "type": "list"
            }
          ],
          "index": 0,
          "question": "Will you need to backfill any roles in your organisation?",
          "status": "COMPLETED"
        },
        {
          "category": "nJcRTz",
          "fields": [
            {
              "answer": "10000",
              "key": "KEnthg",
              "title": "What is the estimated cost of backfilling roles?",
              "type": "text"
            }
          ],
          "index": 0,
          "question": "What is the estimated cost of backfilling roles?",
          "status": "COMPLETED"
        },
        {
          "category": "nJcRTz",
          "fields": [
            {
              "answer": true,
              "key": "pRqIkv",
              "title": "Do you know who will lead the day-to-day delivery of the project in your organisation?",
              "type": "list"
            }
          ],
          "index": 0,
          "question": "Do you know who will lead the day-to-day delivery of the project in your organisation?",
          "status": "COMPLETED"
        },
        {
          "category": "nJcRTz",
          "fields": [
            {
              "answer": "Gommez Addams",
              "key": "eWmNSY",
              "title": "Who will lead the day-to-day delivery of the project in your organisation?",
              "type": "text"
            }
          ],
          "index": 0,
          "question": "Who will lead the day-to-day delivery of the project in your organisation?",
          "status": "COMPLETED"
        },
        {
          "category": null,
          "fields": [
            {
              "answer": true,
              "key": "markAsComplete",
              "title": "Do you want to mark this section as complete?",
              "type": "boolean"
            }
          ],
          "question": "MarkAsComplete",
          "status": "COMPLETED"
        }
      ],
      "status": "COMPLETED"
    },
    {
      "name": "engaging-the-odp-community-dpi",
      "questions": [
        {
          "category": "QiDJsl",
          "fields": [
            {
              "answer": "<p>This is some test text</p>",
              "key": "mmTkva",
              "title": "Why do you want to be a part of the ODP (Open Digital Planning) community?",
              "type": "freeText"
            }
          ],
          "index": 0,
          "question": "Why do you want to be a part of the ODP (Open Digital Planning) community?",
          "status": "COMPLETED"
        },
        {
          "category": null,
          "fields": [
            {
              "answer": true,
              "key": "markAsComplete",
              "title": "Do you want to mark this section as complete?",
              "type": "boolean"
            }
          ],
          "question": "MarkAsComplete",
          "status": "COMPLETED"
        }
      ],
      "status": "COMPLETED"
    },
    {
      "name": "engaging-the-organisation-dpi",
      "questions": [
        {
          "category": "LjAoZK",
          "fields": [
            {
              "answer": "<p>This is some test text</p>",
              "key": "bpzrMJ",
              "title": "How will you make sure team members engage with other parts of your organisation?",
              "type": "freeText"
            }
          ],
          "index": 0,
          "question": "How will you make sure team members engage with other parts of your organisation?",
          "status": "COMPLETED"
        },
        {
          "category": "LjAoZK",
          "fields": [
            {
              "answer": "<p>Luke, I am your Father&nbsp;</p>",
              "key": "oFyZJS",
              "title": "How will you share the progress of the work across your organisation?",
              "type": "freeText"
            }
          ],
          "index": 0,
          "question": "How will you share the progress of the work across your organisation?",
          "status": "COMPLETED"
        },
        {
          "category": null,
          "fields": [
            {
              "answer": true,
              "key": "markAsComplete",
              "title": "Do you want to mark this section as complete?",
              "type": "boolean"
            }
          ],
          "question": "MarkAsComplete",
          "status": "COMPLETED"
        }
      ],
      "status": "COMPLETED"
    },
    {
      "name": "dataset-information-dpi",
      "questions": [
        {
          "category": "FjGMRE",
          "fields": [
            {
              "answer": true,
              "key": "BQKLZz",
              "title": "Does your organisation collect at least one of the datasets?",
              "type": "list"
            }
          ],
          "index": 0,
          "question": "Does your organisation collect at least one of the datasets?",
          "status": "COMPLETED"
        },
        {
          "category": "FjGMRE",
          "fields": [
            {
              "answer": [
                "conservation-areas",
                "article-4-direction",
                "listed-buildings",
                "tree-preservation-orders"
              ],
              "key": "PfjXKB",
              "title": "Which datasets have you collected?",
              "type": "list"
            }
          ],
          "index": 0,
          "question": "Which datasets have you collected?",
          "status": "COMPLETED"
        },
        {
          "category": "FjGMRE",
          "fields": [
            {
              "answer": [
                "paper",
                "spreadsheet",
                "database",
                "gis-(geographical-information-system)"
              ],
              "key": "gBIWQr",
              "title": "Which format is your dataset in for conservation areas?",
              "type": "list"
            }
          ],
          "index": 0,
          "question": "Which format is your dataset in for conservation areas?",
          "status": "COMPLETED"
        },
        {
          "category": "FjGMRE",
          "fields": [
            {
              "answer": [
                "paper",
                "spreadsheet",
                "database",
                "gis-(geographical-information-system)"
              ],
              "key": "JootFe",
              "title": "Which format is your dataset in for article 4 direction?",
              "type": "list"
            }
          ],
          "index": 0,
          "question": "Which format is your dataset in for article 4 direction?",
          "status": "COMPLETED"
        },
        {
          "category": "FjGMRE",
          "fields": [
            {
              "answer": [
                "paper",
                "spreadsheet",
                "database",
                "gis-(geographical-information-system)"
              ],
              "key": "KmGRXX",
              "title": "Which format is your dataset in for listed buildings?",
              "type": "list"
            }
          ],
          "index": 0,
          "question": "Which format is your dataset in for listed buildings?",
          "status": "COMPLETED"
        },
        {
          "category": "FjGMRE",
          "fields": [
            {
              "answer": [
                "paper",
                "spreadsheet",
                "database",
                "gis-(geographical-information-system)"
              ],
              "key": "eptZkL",
              "title": "Which format is your dataset in for tree preservation orders?",
              "type": "list"
            }
          ],
          "index": 0,
          "question": "Which format is your dataset in for tree preservation orders?",
          "status": "COMPLETED"
        },
        {
          "category": "FjGMRE",
          "fields": [
            {
              "answer": "0-to-3-months",
              "key": "WSaPbE",
              "title": "How long do you think it will take your organisation to publish all 4 datasets?",
              "type": "list"
            }
          ],
          "index": 0,
          "question": "How long do you think it will take your organisation to publish all 4 datasets?",
          "status": "COMPLETED"
        },
        {
          "category": "FjGMRE",
          "fields": [
            {
              "answer": "<p>This is some test text</p>",
              "key": "kgGPmd",
              "title": "What are the current known issues and challenges you have with data quality and publication?",
              "type": "freeText"
            }
          ],
          "index": 0,
          "question": "What are the current known issues and challenges you have with data quality and publication?",
          "status": "COMPLETED"
        },
        {
          "category": null,
          "fields": [
            {
              "answer": true,
              "key": "markAsComplete",
              "title": "Do you want to mark this section as complete?",
              "type": "boolean"
            }
          ],
          "question": "MarkAsComplete",
          "status": "COMPLETED"
        }
      ],
      "status": "COMPLETED"
    },
    {
      "name": "future-work-dpi",
      "questions": [
        {
          "category": "SKgfoO",
          "fields": [
            {
              "answer": [
                "adopting-planX",
                "adopting-bops",
                "working-with-existing-software",
                "working-with-new-software"
              ],
              "key": "DCQllx",
              "title": "Which software improvements are you interested in working on in the future?",
              "type": "list"
            }
          ],
          "index": 0,
          "question": "Which software improvements are you interested in working on in the future?",
          "status": "COMPLETED"
        },
        {
          "category": null,
          "fields": [
            {
              "answer": true,
              "key": "markAsComplete",
              "title": "Do you want to mark this section as complete?",
              "type": "boolean"
            }
          ],
          "question": "MarkAsComplete",
          "status": "COMPLETED"
        }
      ],
      "status": "COMPLETED"
    }
  ]
}
"""
)

cof_eoi_application_store_json_template = Template(
    """
    {
    "id": "$app_id",
    "language": "en",
    "fund_id": "$fund_id",
    "last_edited": "2024-02-12T13:41:23.369370",
    "project_name": null,
    "reference": "$short_ref",
    "round_id": "$round_id",
    "round_name": "Expression of interest",
    "started_at": "2024-02-12T13:34:42.569005",
    "status": "SUBMITTED",
    "account_id": "1e8884e2-b043-427f-ba09-7ec2ca409ef0",
    "date_submitted": "2024-02-12T13:41:26.297195",
    "forms": [
      {
    "name": "organisation-details",
    "questions": [
        {
            "category": "eAEGhH",
            "fields": [
                {
                    "answer": "Test Org",
                    "key": "SMRWjl",
                    "title": "Organisation name",
                    "type": "text"
                },
                {
                    "answer": true,
                    "key": "SxkwhF",
                    "title": "Does your organisation have any alternative names?",
                    "type": "list"
                }
            ],
            "question": "Organisation names",
            "status": "COMPLETED"
        },
        {
            "category": "eAEGhH",
            "fields": [
                {
                    "answer": "Test org alt",
                    "key": "qkNYMP",
                    "title": "Alternative name 1",
                    "type": "text"
                },
                {
                    "answer": null,
                    "key": "mVxvon",
                    "title": "Alternative name 2",
                    "type": "text"
                },
                {
                    "answer": null,
                    "key": "DaIVVm",
                    "title": "Alternative name 3",
                    "type": "text"
                }
            ],
            "question": "Alternative names of your organisation",
            "status": "COMPLETED"
        },
        {
            "category": "eAEGhH",
            "fields": [
                {
                    "answer": "001 cemetery lane, null, Chelmsford, null, ss12ss",
                    "key": "OpeSdM",
                    "title": "Organisation address",
                    "type": "text"
                }
            ],
            "question": "Organisation address",
            "status": "COMPLETED"
        },
        {
            "category": "eAEGhH",
            "fields": [
                {
                    "answer": "Charitable incorporated organisation",
                    "key": "uYiLsv",
                    "title": "Organisation classification",
                    "type": "list"
                }
            ],
            "question": "How your organisation is classified",
            "status": "COMPLETED"
        },
        {
            "category": "eAEGhH",
            "fields": [
                {
                    "answer": true,
                    "key": "NcQSbU",
                    "title": "Is your organisation subject to any insolvency actions?",
                    "type": "list"
                }
            ],
            "question": "Is your organisation subject to any insolvency actions?",
            "status": "COMPLETED"
        }
    ],
    "status": "COMPLETED"
},
{
    "name": "development-support-provider",
    "questions": [
        {
            "category": "IEwDfr",
            "fields": [
                {
                    "answer": true,
                    "key": "iXmKyq",
                    "title": "Do you wish to be contacted by the development support provider, if eligible for in-depth support?",
                    "type": "list"
                }
            ],
            "question": "Do you wish to be contacted by the development support provider, if eligible for in-depth support?",
            "status": "COMPLETED"
        },
        {
            "category": "IEwDfr",
            "fields": [
                {
                    "answer": "<p>Test main things</p>",
                    "key": "ObIBSx",
                    "title": "What are the main things you feel you need support with to submit a good COF application?",
                    "type": "freeText"
                }
            ],
            "question": "What are the main things you feel you need support with to submit a good COF application?",
            "status": "COMPLETED"
        },
        {
            "category": "IEwDfr",
            "fields": [
                {
                    "answer": "<p>Test Describe</p>",
                    "key": "MxzEYq",
                    "title": "Describe your project and its aims",
                    "type": "freeText"
                }
            ],
            "question": "Describe your project and its aims",
            "status": "COMPLETED"
        },
        {
            "category": "IEwDfr",
            "fields": [
                {
                    "answer": "Test name lead",
                    "key": "xWnVof",
                    "title": "Name of lead contact",
                    "type": "text"
                },
                {
                    "answer": "a@a.com",
                    "key": "NQoGIm",
                    "title": "Lead contact email address",
                    "type": "text"
                },
                {
                    "answer": "1515665",
                    "key": "srxZmv",
                    "title": "Lead contact telephone number",
                    "type": "text"
                }
            ],
            "question": "Lead contact details",
            "status": "COMPLETED"
        }
    ],
    "status": "COMPLETED"
},
{
    "name": "declaration",
    "questions": [
        {
            "fields": [
                {
                    "answer": "confirm",
                    "key": "YRDRQa",
                    "title": "I confirm",
                    "type": "list"
                }
            ],
            "question": "Declaration",
            "status": "COMPLETED"
        }
    ],
    "status": "COMPLETED"
},
{
    "name": "your-funding-request",
    "questions": [
        {
            "category": "seZPbt",
            "fields": [
                {
                    "answer": [
                        "Renovate a leasehold"
                    ],
                    "key": "aocRmv",
                    "title": "What do you plan to use COF's funding for?",
                    "type": "list"
                }
            ],
            "question": "What do you plan to use COF's funding for?",
            "status": "COMPLETED"
        },
        {
            "category": "seZPbt",
            "fields": [
                {
                    "answer": true,
                    "key": "foQgiy",
                    "title": "Will the leasehold have at least 15 years when your organisation submits a full application?",
                    "type": "list"
                }
            ],
            "question": "Will the leasehold have at least 15 years when your organisation submits a full application?",
            "status": "COMPLETED"
        },
        {
            "category": "seZPbt",
            "fields": [
                {
                    "answer": "75678678",
                    "key": "fZAMFv",
                    "title": "How much capital funding are you requesting from COF?",
                    "type": "text"
                }
            ],
            "question": "How much capital funding are you requesting from COF?",
            "status": "COMPLETED"
        },
        {
            "category": "seZPbt",
            "fields": [
                {
                    "answer": true,
                    "key": "oblxxv",
                    "title": "Do you plan to request any revenue funding?",
                    "type": "list"
                }
            ],
            "question": "Do you plan to request any revenue funding?",
            "status": "COMPLETED"
        },
        {
            "category": "seZPbt",
            "fields": [
                {
                    "answer": true,
                    "key": "eOWKoO",
                    "title": "Do you plan to secure match funding?",
                    "type": "list"
                }
            ],
            "question": "Do you plan to secure match funding? (either cash or in-kind)",
            "status": "COMPLETED"
        },
        {
            "category": "seZPbt",
            "fields": [
                {
                    "answer": [
                        "Community share offer"
                    ],
                    "key": "BykoQQ",
                    "title": "In-kind match funding",
                    "type": "list"
                },
                {
                    "answer": [
                        "Fundraising in your community"
                    ],
                    "key": "qgytim",
                    "title": "Cash match funding",
                    "type": "list"
                },
                {
                    "answer": [
                        "Not sure"
                    ],
                    "key": "daJkaD",
                    "title": "Or",
                    "type": "list"
                }
            ],
            "question": "Where do you plan to source match funding?",
            "status": "COMPLETED"
        },
        {
            "category": "seZPbt",
            "fields": [
                {
                    "answer": true,
                    "key": "yZxdeJ",
                    "title": "Does your project include an element of housing?",
                    "type": "list"
                }
            ],
            "question": "Does your project include an element of housing?",
            "status": "COMPLETED"
        },
        {
            "category": "seZPbt",
            "fields": [
                {
                    "answer": "Yes",
                    "key": "UORyaF",
                    "title": "Will you need planning permission for your project?",
                    "type": "list"
                }
            ],
            "question": "Will you need planning permission for your project?",
            "status": "COMPLETED"
        }
    ],
    "status": "COMPLETED"
},
{
    "name": "about-your-asset",
    "questions": [
        {
            "category": "McpePG",
            "fields": [
                {
                    "answer": true,
                    "key": "eEaDGz",
                    "title": "Does your organisation plan both to receive the funding and run the project?",
                    "type": "list"
                }
            ],
            "question": "Does your organisation plan both to receive the funding and run the project?",
            "status": "COMPLETED"
        },
        {
            "category": "McpePG",
            "fields": [
                {
                    "answer": "Community centre",
                    "key": "Ihjjyi",
                    "title": "Type of asset",
                    "type": "list"
                }
            ],
            "question": "Type of asset",
            "status": "COMPLETED"
        },
        {
            "category": "McpePG",
            "fields": [
                {
                    "answer": true,
                    "key": "zurxox",
                    "title": "Is the asset based in the UK?",
                    "type": "list"
                }
            ],
            "question": "Is the asset based in the UK?",
            "status": "COMPLETED"
        },
        {
            "category": "McpePG",
            "fields": [
                {
                    "answer": "002 That way, test, Test town, null, aa59dd",
                    "key": "dnqIdW",
                    "title": "Address of the asset",
                    "type": "text"
                }
            ],
            "question": "Address of the asset",
            "status": "COMPLETED"
        },
        {
            "category": "McpePG",
            "fields": [
                {
                    "answer": true,
                    "key": "lLQmNb",
                    "title": "Is the asset at risk?",
                    "type": "list"
                }
            ],
            "question": "Is the asset at risk?",
            "status": "COMPLETED"
        },
        {
            "category": "McpePG",
            "fields": [
                {
                    "answer": [
                        "Closure or end of lease"
                    ],
                    "key": "ilMbMH",
                    "title": "What is the risk to the asset?",
                    "type": "list"
                }
            ],
            "question": "What is the risk to the asset?",
            "status": "COMPLETED"
        },
        {
            "category": "McpePG",
            "fields": [
                {
                    "answer": true,
                    "key": "fBhSNc",
                    "title": "Has the asset ever been used by or had significance to the community?",
                    "type": "list"
                }
            ],
            "question": "Has the asset ever been used by or had significance to the community?",
            "status": "COMPLETED"
        },
        {
            "category": "McpePG",
            "fields": [
                {
                    "answer": true,
                    "key": "cPcZos",
                    "title": "Do you already own the asset?",
                    "type": "list"
                }
            ],
            "question": "Do you already own the asset?",
            "status": "COMPLETED"
        }
    ],
    "status": "COMPLETED"
}
  ]
  }
"""
)

hsra_rp_application_store_json_template = Template(
    """
    {
    "id": "$app_id",
    "language": "en",
    "fund_id": "$fund_id",
    "reference": "$short_ref",
    "round_id": "$round_id",
    "status": "SUBMITTED",
    "account_id": "e83dcdf2-2bcb-41d3-955f-3d900851c45a",
    "round_name": "Refurbishment project",
    "started_at": "2024-12-22T22:58:28.190162",
    "last_edited": "2024-12-22T23:23:14.119328",
    "project_name": "test",
    "date_submitted": "2024-12-22T23:23:18.770254+00:00",
    "forms": [
        {
            "name": "vacant-property-details-hsra-rp",
            "status": "COMPLETED",
            "questions": [
                {
                    "fields": [
                        {
                            "key": "dwLpZU",
                            "type": "text",
                            "title": "What is the vacant property's address?",
                            "answer": "796 South New Boulevard, Nam voluptates do tempora sit ducimus sit voluptas maiores dicta quia sit eu commodo, Ex voluptas sapiente sed voluptate autem et, Est perferendis exercitation est autem, NN5 7aZ"
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "ISBazm",
                    "question": "What is the vacant property's address?"
                },
                {
                    "fields": [
                        {
                            "key": "rFpLZQ",
                            "type": "text",
                            "title": "What is the total commercial floorspace of the property, in metres squared?",
                            "answer": "12"
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "ISBazm",
                    "question": "What is the total commercial floorspace of the property, in metres squared?"
                },
                {
                    "fields": [
                        {
                            "key": "ndpQJk",
                            "type": "text",
                            "title": "Upload the initial notice you served the landlord",
                            "answer": "Screenshot 2024-12-19 at 15.27.08.png"
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "ISBazm",
                    "question": "Upload the initial notice you served the landlord"
                },
                {
                    "fields": [
                        {
                            "key": "markAsComplete",
                            "type": "boolean",
                            "title": "Do you want to mark this section as complete?",
                            "answer": true
                        }
                    ],
                    "status": "COMPLETED",
                    "category": null,
                    "question": "MarkAsComplete"
                }
            ]
        },
        {
            "name": "application-name-hsra-rp",
            "status": "COMPLETED",
            "questions": [
                {
                    "fields": [
                        {
                            "key": "qbBtUh",
                            "type": "text",
                            "title": "What would you like to name your application?",
                            "answer": "test"
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "CiYZae",
                    "question": "What would you like to name your application?"
                },
                {
                    "fields": [
                        {
                            "key": "markAsComplete",
                            "type": "boolean",
                            "title": "Do you want to mark this section as complete?",
                            "answer": true
                        }
                    ],
                    "status": "COMPLETED",
                    "category": null,
                    "question": "MarkAsComplete"
                }
            ]
        },
        {
            "name": "applicant-information-hsra-rp",
            "status": "COMPLETED",
            "questions": [
                {
                    "fields": [
                        {
                            "key": "OkKkMd",
                            "type": "text",
                            "title": "Full name",
                            "answer": "Vaughan Decker"
                        },
                        {
                            "key": "Lwkcam",
                            "type": "text",
                            "title": "Job title",
                            "answer": "Vel et voluptatibus "
                        },
                        {
                            "key": "XfiUqN",
                            "type": "text",
                            "title": "Email address",
                            "answer": "nivedys@mailinator.com"
                        },
                        {
                            "key": "DlZjvr",
                            "type": "text",
                            "title": "Telephone number",
                            "answer": "+1 (307) 655-2083"
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "bnfUAs",
                    "question": "Who should we contact about this application?"
                },
                {
                    "fields": [
                        {
                            "key": "markAsComplete",
                            "type": "boolean",
                            "title": "Do you want to mark this section as complete?",
                            "answer": true
                        }
                    ],
                    "status": "COMPLETED",
                    "category": null,
                    "question": "MarkAsComplete"
                }
            ]
        },
        {
            "name": "declaration-hsra-rp",
            "status": "COMPLETED",
            "questions": [
                {
                    "fields": [
                        {
                            "key": "QUaOGq",
                            "type": "list",
                            "title": "By submitting this application, you confirm that the information you have provided is correct.",
                            "answer": [
                                "confirm"
                            ]
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "wycNzR",
                    "question": "By submitting this application, you confirm that the information you have provided is correct."
                },
                {
                    "fields": [
                        {
                            "key": "markAsComplete",
                            "type": "boolean",
                            "title": "Do you want to mark this section as complete?",
                            "answer": true
                        }
                    ],
                    "status": "COMPLETED",
                    "category": null,
                    "question": "MarkAsComplete"
                }
            ]
        },
        {
            "name": "organisation-information-hsra-rp",
            "status": "COMPLETED",
            "questions": [
                {
                    "fields": [
                        {
                            "key": "WLddBt",
                            "type": "text",
                            "title": "Which local authority are you applying from?",
                            "answer": "test"
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "eaktoV",
                    "question": "Which local authority are you applying from?"
                },
                {
                    "fields": [
                        {
                            "key": "okHmBB",
                            "type": "text",
                            "title": "Full name",
                            "answer": "Abel Pearson"
                        },
                        {
                            "key": "bQOXTi",
                            "type": "text",
                            "title": "Email address",
                            "answer": "rycytarule@mailinator.com"
                        },
                        {
                            "key": "phaosT",
                            "type": "text",
                            "title": "Telephone number",
                            "answer": "+1 (175) 631-9337"
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "eaktoV",
                    "question": "Who is your section 151 officer?"
                },
                {
                    "fields": [
                        {
                            "key": "markAsComplete",
                            "type": "boolean",
                            "title": "Do you want to mark this section as complete?",
                            "answer": true
                        }
                    ],
                    "status": "COMPLETED",
                    "category": null,
                    "question": "MarkAsComplete"
                }
            ]
        },
        {
            "name": "designated-area-details-hsra-rp",
            "status": "COMPLETED",
            "questions": [
                {
                    "fields": [
                        {
                            "key": "frDgtU",
                            "type": "text",
                            "title": "Which designated high street or town centre is the vacant property in?",
                            "answer": "asfd"
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "YFgsrH",
                    "question": "Which designated high street or town centre is the vacant property in?"
                },
                {
                    "fields": [
                        {
                            "key": "TzGISC",
                            "type": "text",
                            "title": "Share the link with details of the designated area.",
                            "answer": "https://www.zekigopozojyp.cm"
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "YFgsrH",
                    "question": "Share the link with details of the designated area"
                },
                {
                    "fields": [
                        {
                            "key": "markAsComplete",
                            "type": "boolean",
                            "title": "Do you want to mark this section as complete?",
                            "answer": true
                        }
                    ],
                    "status": "COMPLETED",
                    "category": null,
                    "question": "MarkAsComplete"
                }
            ]
        },
        {
            "name": "milestones-hsra-rp",
            "status": "COMPLETED",
            "questions": [
                {
                    "fields": [
                        {
                            "key": "kkBYPW",
                            "type": "date",
                            "title": "When do you expect the auction to take place?",
                            "answer": "2002-01-23"
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "wtecPW",
                    "question": "When do you expect the auction to take place?"
                },
                {
                    "fields": [
                        {
                            "key": "pTZLiJ",
                            "type": "date",
                            "title": "When do you expect to submit your claim?",
                            "answer": "1989-06-06"
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "wtecPW",
                    "question": "When do you expect to submit your claim?"
                },
                {
                    "fields": [
                        {
                            "key": "ihfalZ",
                            "type": "date",
                            "title": "When do you expect the tenant to sign  the tenancy agreement?",
                            "answer": "1988-04-22"
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "wtecPW",
                    "question": "When do you expect the tenant to sign  the tenancy agreement?"
                },
                {
                    "fields": [
                        {
                            "key": "gLzqSP",
                            "type": "date",
                            "title": "When do you expect to finish the refurbishment works?",
                            "answer": "1995-08-27"
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "wtecPW",
                    "question": "When do you expect to finish the refurbishment works?"
                },
                {
                    "fields": [
                        {
                            "key": "HeqfVH",
                            "type": "date",
                            "title": "When do you expect the tenant to move in?",
                            "answer": "2012-03-17"
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "wtecPW",
                    "question": "When do you expect the tenant to move in?"
                },
                {
                    "fields": [
                        {
                            "key": "markAsComplete",
                            "type": "boolean",
                            "title": "Do you want to mark this section as complete?",
                            "answer": true
                        }
                    ],
                    "status": "COMPLETED",
                    "category": null,
                    "question": "MarkAsComplete"
                }
            ]
        },
        {
            "name": "project-costs-hsra-rp",
            "status": "COMPLETED",
            "questions": [
                {
                    "fields": [
                        {
                            "key": "uJIluf",
                            "type": "text",
                            "title": "How much funding are you applying for? ",
                            "answer": "500000"
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "qavZyX",
                    "question": "How much funding are you applying for? "
                },
                {
                    "fields": [
                        {
                            "key": "LFwJND",
                            "type": "freeText",
                            "title": "Why are your costs higher than the guided price?",
                            "answer": "<p>sdlkjf</p>"
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "qavZyX",
                    "question": "Why are your costs higher than the guided price?"
                },
                {
                    "fields": [
                        {
                            "key": "zORoJy",
                            "type": "text",
                            "title": "Upload the quote for the vacancy register",
                            "answer": "Screenshot 2024-12-16 at 11.30.02.png"
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "qavZyX",
                    "question": "Upload the independent survey of works"
                },
                {
                    "fields": [
                        {
                            "key": "xPzwQq",
                            "type": "text",
                            "title": "Upload quotes for refurbishment",
                            "answer": "Screenshot 2024-12-19 at 15.27.08.png"
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "qavZyX",
                    "question": "Upload quotes for refurbishment"
                },
                {
                    "fields": [
                        {
                            "key": "markAsComplete",
                            "type": "boolean",
                            "title": "Do you want to mark this section as complete?",
                            "answer": true
                        }
                    ],
                    "status": "COMPLETED",
                    "category": null,
                    "question": "MarkAsComplete"
                }
            ]
        }
    ]
    }
    """
)

hsra_vr_application_store_json_template = Template(
    """
  {
    "id": "$app_id",
    "language": "en",
    "fund_id": "$fund_id",
    "reference": "$short_ref",
    "round_id": "$round_id",
    "started_at": "2024-10-23T14:59:11.298036",
    "status": "SUBMITTED",
    "account_id": "e83dcdf2-2bcb-41d3-955f-3d900851c45a",
    "round_name": "Vacancy register project",
    "started_at": "2024-12-22T17:01:59.223327",
    "last_edited": "2024-12-22T17:14:50.560894",
    "project_name": "test",
    "date_submitted": "2024-12-22T17:15:08.218750+00:00",
    "forms": [
        {
            "name": "project-costs-hsra-vr",
            "status": "COMPLETED",
            "questions": [
                {
                    "fields": [
                        {
                            "key": "MIrLuu",
                            "type": "text",
                            "title": "How much funding are you applying for?",
                            "answer": "50000"
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "ObIMZj",
                    "question": "How much funding are you applying for?"
                },
                {
                    "fields": [
                        {
                            "key": "SqqyyB",
                            "type": "text",
                            "title": "Upload the quote for the vacancy register",
                            "answer": "4f53d409-ba39-4eef-8ca2-93b544a2e9dc.txt"
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "ObIMZj",
                    "question": "Upload the quote for the vacancy register"
                },
                {
                    "fields": [
                        {
                            "key": "markAsComplete",
                            "type": "boolean",
                            "title": "Do you want to mark this section as complete?",
                            "answer": true
                        }
                    ],
                    "status": "COMPLETED",
                    "category": null,
                    "question": "MarkAsComplete"
                }
            ]
        },
        {
            "name": "applicant-information-hsra-vr",
            "status": "COMPLETED",
            "questions": [
                {
                    "fields": [
                        {
                            "key": "OkKkMd",
                            "type": "text",
                            "title": "Full name",
                            "answer": "Wing Bell"
                        },
                        {
                            "key": "Lwkcam",
                            "type": "text",
                            "title": "Job title",
                            "answer": "Quis aut suscipit do"
                        },
                        {
                            "key": "XfiUqN",
                            "type": "text",
                            "title": "Email address",
                            "answer": "numakenad@mailinator.com"
                        },
                        {
                            "key": "DlZjvr",
                            "type": "text",
                            "title": "Telephone number",
                            "answer": "+1 (322) 893-3213"
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "bnfUAs",
                    "question": "Who should we contact about this application?"
                },
                {
                    "fields": [
                        {
                            "key": "markAsComplete",
                            "type": "boolean",
                            "title": "Do you want to mark this section as complete?",
                            "answer": true
                        }
                    ],
                    "status": "COMPLETED",
                    "category": null,
                    "question": "MarkAsComplete"
                }
            ]
        },
        {
            "name": "application-name-hsra-vr",
            "status": "COMPLETED",
            "questions": [
                {
                    "fields": [
                        {
                            "key": "qbBtUh",
                            "type": "text",
                            "title": "What would you like to name your application?",
                            "answer": "test"
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "CiYZae",
                    "question": "What would you like to name your application?"
                },
                {
                    "fields": [
                        {
                            "key": "markAsComplete",
                            "type": "boolean",
                            "title": "Do you want to mark this section as complete?",
                            "answer": true
                        }
                    ],
                    "status": "COMPLETED",
                    "category": null,
                    "question": "MarkAsComplete"
                }
            ]
        },
        {
            "name": "declaration-hsra-vr",
            "status": "COMPLETED",
            "questions": [
                {
                    "fields": [
                        {
                            "key": "QUaOGq",
                            "type": "list",
                            "title": "By submitting this application, you confirm that the information you have provided is correct.",
                            "answer": [
                                "confirm"
                            ]
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "wycNzR",
                    "question": "By submitting this application, you confirm that the information you have provided is correct."
                },
                {
                    "fields": [
                        {
                            "key": "markAsComplete",
                            "type": "boolean",
                            "title": "Do you want to mark this section as complete?",
                            "answer": true
                        }
                    ],
                    "status": "COMPLETED",
                    "category": null,
                    "question": "MarkAsComplete"
                }
            ]
        },
        {
            "name": "milestones-hsra-vr",
            "status": "COMPLETED",
            "questions": [
                {
                    "fields": [
                        {
                            "key": "yvpmIv",
                            "type": "date",
                            "title": "When do you expect the vacancy register to be completed?",
                            "answer": "2010-11-07"
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "wtecPW",
                    "question": "When do you expect the vacancy register to be completed?"
                },
                {
                    "fields": [
                        {
                            "key": "KFjxBs",
                            "type": "date",
                            "title": "When do you expect to submit your post-payment assurance form to be submitted?",
                            "answer": "2008-01-11"
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "wtecPW",
                    "question": "When do you expect the post-payment assurance form to be submitted?"
                },
                {
                    "fields": [
                        {
                            "key": "markAsComplete",
                            "type": "boolean",
                            "title": "Do you want to mark this section as complete?",
                            "answer": true
                        }
                    ],
                    "status": "COMPLETED",
                    "category": null,
                    "question": "MarkAsComplete"
                }
            ]
        },
        {
            "name": "designated-area-details-hsra-vr",
            "status": "COMPLETED",
            "questions": [
                {
                    "fields": [
                        {
                            "key": "frDgtU",
                            "type": "text",
                            "title": "Which town or city will the designated area be located in?",
                            "answer": "test"
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "YFgsrH",
                    "question": "Which town or city will the designated area be located in?"
                },
                {
                    "fields": [
                        {
                            "key": "YMqcPf",
                            "type": "text",
                            "title": "Tell us more about the designated area.",
                            "answer": "test"
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "YFgsrH",
                    "question": "Tell us more about the designated area."
                },
                {
                    "fields": [
                        {
                            "key": "markAsComplete",
                            "type": "boolean",
                            "title": "Do you want to mark this section as complete?",
                            "answer": true
                        }
                    ],
                    "status": "COMPLETED",
                    "category": null,
                    "question": "MarkAsComplete"
                }
            ]
        },
        {
            "name": "organisation-information-hsra-vr",
            "status": "COMPLETED",
            "questions": [
                {
                    "fields": [
                        {
                            "key": "WLddBt",
                            "type": "text",
                            "title": "Which local authority are you applying from?",
                            "answer": "test"
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "eaktoV",
                    "question": "Which local authority are you applying from?"
                },
                {
                    "fields": [
                        {
                            "key": "okHmBB",
                            "type": "text",
                            "title": "Full name",
                            "answer": "Marsden Moore"
                        },
                        {
                            "key": "bQOXTi",
                            "type": "text",
                            "title": "Email address",
                            "answer": "qoxicuc@mailinator.com"
                        },
                        {
                            "key": "phaosT",
                            "type": "text",
                            "title": "Telephone number",
                            "answer": "+1 (204) 238-8366"
                        }
                    ],
                    "status": "COMPLETED",
                    "category": "eaktoV",
                    "question": "Who is your section 151 officer?"
                },
                {
                    "fields": [
                        {
                            "key": "markAsComplete",
                            "type": "boolean",
                            "title": "Do you want to mark this section as complete?",
                            "answer": true
                        }
                    ],
                    "status": "COMPLETED",
                    "category": null,
                    "question": "MarkAsComplete"
                }
            ]
        }
    ],
    "status": "SUBMITTED",
    "fund_id": "1e4bd8b0-b399-466d-bbd1-572171bbc7bd",
    "language": "en",
    "round_id": "ae223686-cbcc-4548-8b52-05898c315a59",
    "reference": "HSRA-VR-RXDODR",
    "account_id": "e83dcdf2-2bcb-41d3-955f-3d900851c45a",
    "round_name": "Vacancy register project",
    "started_at": "2024-12-22T17:01:59.223327",
    "last_edited": "2024-12-22T17:14:50.560894",
    "project_name": "test",
    "date_submitted": "2024-12-22T17:15:08.218750+00:00"
  }
  """
)

cof25_eoi_application_store_json_template = Template(
    """
    {
    "id": "$app_id",
    "language": "en",
    "fund_id": "$fund_id",
    "last_edited": "2024-10-23T15:05:06.373533",
    "project_name": "Est sequi iusto veli",
    "reference": "$short_ref",
    "round_id": "$round_id",
    "round_name": "Round 1",
    "started_at": "2024-10-23T14:59:11.298036",
    "status": "SUBMITTED",
    "account_id": "2b395090-5e7b-4d08-9d1e-bb9917418576",
    "date_submitted": "2024-10-23T15:05:49.709130",
    "forms": [
      {
        "name": "organisation-details-25",
        "questions": [
          {
            "fields": [
              {
                "answer": "Est sequi iusto veli",
                "key": "SMRWjl",
                "title": "Organisation name",
                "type": "text"
              },
              {
                "answer": false,
                "key": "SxkwhF",
                "title": "Does your organisation have any alternative names?",
                "type": "list"
              }
            ],
            "question": "Organisation name",
            "status": "COMPLETED"
          },
          {
            "fields": [
              {
                "answer": "832 Milton Parkway, Quam hic voluptas hic ut voluptates pariatur Perspiciatis in iusto pariatur Nisi sed fuga, London, West London, NN5 7AZ",
                "key": "OpeSdM",
                "title": "Organisation address",
                "type": "text"
              }
            ],
            "question": "Organisation address",
            "status": "COMPLETED"
          },
          {
            "fields": [
              {
                "answer": "parish-town-community-councils",
                "key": "uYiLsv",
                "title": "Organisation classification",
                "type": "list"
              }
            ],
            "question": "How your organisation is classified",
            "status": "COMPLETED"
          },
          {
            "fields": [
              {
                "answer": false,
                "key": "NcQSbU",
                "title": "Is your organisation subject to any insolvency actions?",
                "type": "list"
              }
            ],
            "question": "Is your organisation subject to any insolvency actions?",
            "status": "COMPLETED"
          }
        ],
        "status": "COMPLETED"
      },
      {
        "name": "declaration-25",
        "questions": [
          {
            "fields": [
              {
                "answer": [
                  "confirm"
                ],
                "key": "oXFEkV",
                "title": "I confirm the information I've provided is correct",
                "type": "list"
              }
            ],
            "question": "Declaration",
            "status": "COMPLETED"
          }
        ],
        "status": "COMPLETED"
      },
      {
        "name": "about-your-asset-25",
        "questions": [
          {
            "fields": [
              {
                "answer": true,
                "key": "eEaDGz",
                "title": "Does your organisation plan both to receive the funding and run the project?",
                "type": "list"
              }
            ],
            "question": "Does your organisation plan both to receive the funding and run the project?",
            "status": "COMPLETED"
          },
          {
            "fields": [
              {
                "answer": "Community centre",
                "key": "Ihjjyi",
                "title": "Type of asset",
                "type": "list"
              }
            ],
            "question": "Type of asset",
            "status": "COMPLETED"
          },
          {
            "fields": [
              {
                "answer": true,
                "key": "zurxox",
                "title": "Is the asset based in the UK?",
                "type": "list"
              }
            ],
            "question": "Is the asset based in the UK?",
            "status": "COMPLETED"
          },
          {
            "fields": [
              {
                "answer": "Fritz Curry",
                "key": "xYnVof",
                "title": "Name of the asset",
                "type": "text"
              },
              {
                "answer": "921 Oak Parkway, Et nemo id sunt repudiandae aliquam id quidem laboris voluptas pariatur Ut est optio soluta dol, London, West London, NN4 7AZ",
                "key": "dnqIdW",
                "title": "Address of the asset",
                "type": "text"
              }
            ],
            "question": "Address of the asset",
            "status": "COMPLETED"
          },
          {
            "fields": [
              {
                "answer": true,
                "key": "lLQmNb",
                "title": "Is the asset at risk?",
                "type": "list"
              }
            ],
            "question": "Is the asset at risk?",
            "status": "COMPLETED"
          },
          {
            "fields": [
              {
                "answer": [
                  "Closure or end of lease"
                ],
                "key": "ilMbMH",
                "title": "What is the risk to the asset?",
                "type": "list"
              }
            ],
            "question": "What is the risk to the asset?",
            "status": "COMPLETED"
          },
          {
            "fields": [
              {
                "answer": true,
                "key": "fBhSNc",
                "title": "Has the asset ever been used by or had significance to the community?",
                "type": "list"
              }
            ],
            "question": "Has the asset ever been used by or had significance to the community?",
            "status": "COMPLETED"
          },
          {
            "fields": [
              {
                "answer": false,
                "key": "cPcZos",
                "title": "Do you already own the asset?",
                "type": "list"
              }
            ],
            "question": "Do you already own the asset?",
            "status": "COMPLETED"
          },
          {
            "fields": [
              {
                "answer": "Yes, a town, parish or community council",
                "key": "XuAyrs",
                "title": "Does the asset belong to a public authority?",
                "type": "list"
              }
            ],
            "question": "Does the asset belong to a public authority?",
            "status": "COMPLETED"
          },
          {
            "fields": [
              {
                "answer": "Do not know who owner is",
                "key": "oDhZlw",
                "title": "Select the option which best represents the stage you are at in purchasing the asset",
                "type": "list"
              }
            ],
            "question": "Select the option which best represents the stage you are at in purchasing the asset",
            "status": "COMPLETED"
          }
        ],
        "status": "COMPLETED"
      },
      {
        "name": "your-funding-request-25",
        "questions": [
          {
            "fields": [
              {
                "answer": [
                  "Buy a leasehold"
                ],
                "key": "aocRmv",
                "title": "What do you plan to use COF25's funding for?",
                "type": "list"
              }
            ],
            "question": "What do you plan to use COF25's funding for?",
            "status": "COMPLETED"
          },
          {
            "fields": [
              {
                "answer": true,
                "key": "foQgiy",
                "title": "Will the leasehold have at least 15 years when your organisation submits a full application?",
                "type": "list"
              }
            ],
            "question": "Will the leasehold have at least 15 years when your organisation submits a full application?",
            "status": "COMPLETED"
          },
          {
            "fields": [
              {
                "answer": "112",
                "key": "fZAMFv",
                "title": "How much capital funding are you requesting from COF25?",
                "type": "text"
              }
            ],
            "question": "How much capital funding are you requesting from COF25?",
            "status": "COMPLETED"
          },
          {
            "fields": [
              {
                "answer": true,
                "key": "oblxxv",
                "title": "Do you plan to request any revenue funding?",
                "type": "list"
              }
            ],
            "question": "Do you plan to request any revenue funding?",
            "status": "COMPLETED"
          },
          {
            "fields": [
              {
                "answer": true,
                "key": "eOWKoO",
                "title": "Do you plan to secure match funding?",
                "type": "list"
              }
            ],
            "question": "Do you plan to secure match funding? (either cash or in-kind)",
            "status": "COMPLETED"
          },
          {
            "fields": [
              {
                "answer": [
                  "Donation of professional services"
                ],
                "key": "BykoQQ",
                "title": "Where do you plan to source match funding?",
                "type": "list"
              }
            ],
            "question": "Where do you plan to source match funding?",
            "status": "COMPLETED"
          },
          {
            "fields": [
              {
                "answer": "Secured some match funding",
                "key": "kWRuac",
                "title": "What progress have you made to secure this funding?",
                "type": "list"
              }
            ],
            "question": "What progress have you made to secure this funding?",
            "status": "COMPLETED"
          },
          {
            "fields": [
              {
                "answer": true,
                "key": "yZxdeJ",
                "title": "Does your project include an element of housing?",
                "type": "list"
              }
            ],
            "question": "Does your project include an element of housing?",
            "status": "COMPLETED"
          },
          {
            "fields": [
              {
                "answer": "No",
                "key": "UORyaF",
                "title": "Will you need planning permission for your project?",
                "type": "list"
              }
            ],
            "question": "Will you need planning permission for your project?",
            "status": "COMPLETED"
          }
        ],
        "status": "COMPLETED"
      },
      {
        "name": "development-support-provider-25",
        "questions": [
          {
            "fields": [
              {
                "answer": "Yes, I agree to be contacted if eligible",
                "key": "iXmKyq",
                "title": "Do you wish to be contacted by the development support provider, if eligible for in-depth support?",
                "type": "list"
              }
            ],
            "question": "Do you wish to be contacted by the development support provider, if eligible for in-depth support?",
            "status": "COMPLETED"
          },
          {
            "fields": [
              {
                "answer": [
                  "Financial forecasting"
                ],
                "key": "ObIBSx",
                "title": "What are the main things you feel you need support with to submit a good COF25 application?",
                "type": "list"
              }
            ],
            "question": "What are the main things you feel you need support with to submit a good COF25 application?",
            "status": "COMPLETED"
          },
          {
            "fields": [
              {
                "answer": "<p>yui</p>",
                "key": "MxzEYq",
                "title": "Describe your project and its aims",
                "type": "freeText"
              }
            ],
            "question": "Describe your project and its aims",
            "status": "COMPLETED"
          },
          {
            "fields": [
              {
                "answer": "Signe Casey",
                "key": "xWnVof",
                "title": "Name of lead contact",
                "type": "text"
              },
              {
                "answer": "metygacil@mailinator.com",
                "key": "NQoGIm",
                "title": "Lead contact email address",
                "type": "text"
              },
              {
                "answer": "+1 (768) 931-5335",
                "key": "srxZmv",
                "title": "Lead contact telephone number",
                "type": "text"
              }
            ],
            "question": "Lead contact details",
            "status": "COMPLETED"
          }
        ],
        "status": "COMPLETED"
      }
    ]
  }
"""
)
