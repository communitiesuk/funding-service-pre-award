# ruff: noqa: E501

unscored_sections = [
    {
        "id": "unscored",
        "name": "Unscored",
        "sub_criteria": [
            {
                "id": "your-organisation",
                "name": "Your organisation",
                "themes": [
                    {
                        "id": "your-organisation",
                        "name": "Your organisation",
                        "answers": [
                            {
                                "field_id": "WwxTJv",
                                "form_name": "ehcf-apply-your-organisation",
                                "field_type": "textField",
                                "presentation_type": "text",
                                "question": "What is your organisation's name?",
                            },
                            {
                                "field_id": "wqpbOz",
                                "form_name": "ehcf-apply-your-organisation",
                                "field_type": "textField",
                                "presentation_type": "text",
                                "question": "Does your organisation have an alternative name?",
                            },
                            {
                                "field_id": "iXAfvh",
                                "form_name": "ehcf-apply-your-organisation",
                                "field_type": "ukAddressField",
                                "presentation_type": "text",
                                "question": "What is your organisation's address?",
                            },
                            {
                                "field_id": "DJZuCU",
                                "form_name": "ehcf-apply-your-organisation",
                                "field_type": "radiosField",
                                "presentation_type": "text",
                                "question": "What is the legal status of your organisation?",
                            },
                            {
                                "field_id": "siZmOt",
                                "form_name": "ehcf-apply-your-organisation",
                                "field_type": "textField",
                                "presentation_type": "text",
                                "question": "<h3>CHARITABLE INCORPORATED ORGANISATION</h3>What is your registered charity number?",
                            },
                            {
                                "field_id": "NsTZAN",
                                "form_name": "ehcf-apply-your-organisation",
                                "field_type": "textField",
                                "presentation_type": "text",
                                "question": "<h3>CHARITABLE COMPANY LIMITED BY GUARANTEE</h3>What is your registered charity number?",
                            },
                            {
                                "field_id": "AAbTDt",
                                "form_name": "ehcf-apply-your-organisation",
                                "field_type": "checkboxesField",
                                "presentation_type": "text",
                                "question": "My charity is exempt and does not have a charity number",
                            },
                            {
                                "field_id": "fCXecZ",
                                "form_name": "ehcf-apply-your-organisation",
                                "field_type": "textField",
                                "presentation_type": "text",
                                "question": "What is your company registration number?",
                            },
                            {
                                "field_id": "xTJyLj",
                                "form_name": "ehcf-apply-your-organisation",
                                "field_type": "textField",
                                "presentation_type": "text",
                                "question": "<h3>COMMUNITY INTEREST COMPANY</h3>What is your company registration number?",
                            },
                            {
                                "field_id": "mtXRXO",
                                "form_name": "ehcf-apply-your-organisation",
                                "field_type": "textField",
                                "presentation_type": "text",
                                "question": "<h3>COMMUNITY BENEFIT SOCIETY OR CO-OPERATIVE SOCIETY</h3>What is your Financial Conduct Authority reference number?",
                            },
                            {
                                "field_id": "elhXgA",
                                "form_name": "ehcf-apply-your-organisation",
                                "field_type": "textField",
                                "presentation_type": "text",
                                "question": "<h3>Who is the primary contact for this grant?</h3>Full name",
                            },
                            {
                                "field_id": "sHxRrj",
                                "form_name": "ehcf-apply-your-organisation",
                                "field_type": "emailAddressField",
                                "presentation_type": "text",
                                "question": "Email address",
                            },
                            {
                                "field_id": "sLHzMy",
                                "form_name": "ehcf-apply-your-organisation",
                                "field_type": "telephoneNumberField",
                                "presentation_type": "text",
                                "question": "Telephone number",
                            },
                            {
                                "field_id": "hduWVY",
                                "form_name": "ehcf-apply-your-organisation",
                                "field_type": "textField",
                                "presentation_type": "text",
                                "question": "Job title",
                            },
                            {
                                "field_id": "LnKSXL",
                                "form_name": "ehcf-apply-your-organisation",
                                "field_type": "yesNoField",
                                "presentation_type": "text",
                                "question": "Is the primary contact also an authorised signatory?",
                            },
                            {
                                "field_id": "KQDHpr",
                                "form_name": "ehcf-apply-your-organisation",
                                "field_type": "textField",
                                "presentation_type": "text",
                                "question": "<h3>Who is the authorised signatory?</h3>Full name",
                            },
                            {
                                "field_id": "byicLn",
                                "form_name": "ehcf-apply-your-organisation",
                                "field_type": "textField",
                                "presentation_type": "text",
                                "question": "Email address",
                            },
                            {
                                "field_id": "FVhlFB",
                                "form_name": "ehcf-apply-your-organisation",
                                "field_type": "textField",
                                "presentation_type": "text",
                                "question": "Job title",
                            },
                            {
                                "field_id": "LNYBTt",
                                "form_name": "ehcf-apply-your-organisation",
                                "field_type": "yesNoField",
                                "presentation_type": "text",
                                "question": "<h3>Is your application a joint bid in partnership with other organisations?</h3>",
                            },
                            {
                                "field_id": "aCHAZS",
                                "form_name": "ehcf-apply-your-organisation",
                                "field_type": "multiInputField",
                                "presentation_type": "table",
                                "question": [
                                    "Who are the partnership members?",
                                    {
                                        "YprmGA": {
                                            "column_title": "Partnership organisation name",
                                            "type": "textField",
                                        },
                                        "wxAieZ": {
                                            "column_title": "Lead contact name",
                                            "type": "textField",
                                        },
                                        "gJWtrE": {
                                            "column_title": "Role",
                                            "type": "textField",
                                        },
                                    },
                                ],
                            },
                            {
                                "field_id": "QmzwZy",
                                "form_name": "ehcf-apply-your-organisation",
                                "field_type": "clientSideFileUploadField",
                                "presentation_type": "s3bucketPath",
                                "question": "Upload a document that shows the other partnership organisations support this bid",
                                "path": "upload-a-document-that-shows-the-other-partnership-organisations-support-this-bid",
                            },
                        ],
                    }
                ],
            },
            {
                "id": "letter-of-support-and-declarations",
                "name": "Letter of support and declarations",
                "themes": [
                    {
                        "id": "letter-of-support-and-declarations",
                        "name": "Letter of support and declarations",
                        "answers": [
                            {
                                "field_id": "PpAmke",
                                "form_name": "ehcf-apply-declaration",
                                "field_type": "clientSideFileUploadField",
                                "presentation_type": "s3bucketPath",
                                "question": "<h3>Upload your letter of support</h3>",
                                "path": "upload-your-letter-of-support",
                            },
                            {
                                "field_id": "JnHBkv",
                                "form_name": "ehcf-apply-declaration",
                                "field_type": "checkboxesField",
                                "presentation_type": "text",
                                "question": "<h3>Declarations</h3>",  # My organisation has a UK bank account
                            },
                            {
                                "field_id": "thZbZC",
                                "form_name": "ehcf-apply-declaration",
                                "field_type": "checkboxesField",
                                "presentation_type": "text",
                                "question": "",  # My organisation agrees to reporting requirements
                            },
                            {
                                "field_id": "NVVpQT",
                                "form_name": "ehcf-apply-declaration",
                                "field_type": "checkboxesField",
                                "presentation_type": "text",
                                "question": "",  # I confirm that the information provided is accurate
                            },
                        ],
                    },
                ],
            },
        ],
    },
]
