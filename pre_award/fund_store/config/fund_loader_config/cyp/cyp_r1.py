from datetime import datetime, timezone

from data.models import FundingType
from pre_award.fund_store.config.fund_loader_config.common_fund_config.fund_base_tree_paths import (
    CYP_R1_BASE_PATH,
)
from pre_award.fund_store.config.fund_loader_config.logo import DLUHC_LOGO_PNG

CYP_FUND_ID = "1baa0f68-4e0a-4b02-9dfe-b5646f089e65"
CYP_ROUND_1_ID = "888aae3d-7e2c-4523-b9c1-95952b3d1644"
APPLICATION_BASE_PATH = ".".join([str(CYP_R1_BASE_PATH), str(1)])
ASSESSMENT_BASE_PATH = ".".join([str(CYP_R1_BASE_PATH), str(2)])
CYP_R1_OPENS_DATE = datetime(2023, 9, 27, 10, 0, 0, tzinfo=timezone.utc)  # 2023-09-27 10:00:00
CYP_R1_DEADLINE_DATE = datetime(2023, 11, 1, 11, 59, 0, tzinfo=timezone.utc)  # 2023-11-1 11:59:00
CYP_R1_ASSESSMENT_DEADLINE_DATE = datetime(2023, 12, 24, 12, 0, 0, tzinfo=timezone.utc)  # 2023-12-24 12:00:00

CYP_PROSPECTS_LINK = "https://www.gov.uk/government/publications/the-children-and-young-peoples-resettlement-fund-prospectus/the-children-and-young-peoples-resettlement-fund-prospectus"  # noqa
CYP_APPLICATION_GUIDANCE = {
    "en": (
        "<h2 class='govuk-heading govuk-heading-s'>Before you start</h2><p"
        f" class='govuk-body'><a href='{CYP_PROSPECTS_LINK}'>Read the fund's prospectus</a>"
        " before you apply.</p><p class='govuk-body'>You can <a"
        " href='{all_questions_url}'>preview the full list of application"
        " questions</a>.</p>"
    )
}

r1_application_sections = [
    {
        "section_name": {"en": "Before you start", "cy": ""},
        "tree_path": f"{APPLICATION_BASE_PATH}.1",
    },
    {
        "section_name": {"en": "1.1 Name your application", "cy": ""},
        "form_name_json": {"en": "name-your-application-cyp", "cy": ""},
        "tree_path": f"{APPLICATION_BASE_PATH}.1.1",
    },
    {
        "section_name": {"en": "2. About your organisation", "cy": ""},
        "tree_path": f"{APPLICATION_BASE_PATH}.2",
        "requires_feedback": True,
    },
    {
        "section_name": {"en": "2.1 About your organisation", "cy": ""},
        "form_name_json": {"en": "about-your-organisation-cyp", "cy": ""},
        "tree_path": f"{APPLICATION_BASE_PATH}.2.1",
    },
    {
        "section_name": {"en": "2.2 Applicant information", "cy": ""},
        "form_name_json": {"en": "applicant-information-cyp", "cy": ""},
        "tree_path": f"{APPLICATION_BASE_PATH}.2.2",
    },
    {
        "section_name": {"en": "3. Your skills and experience", "cy": ""},
        "tree_path": f"{APPLICATION_BASE_PATH}.3",
        "requires_feedback": True,
    },
    {
        "section_name": {"en": "3.1 Your skills and experience", "cy": ""},
        "form_name_json": {"en": "skills-and-experience-cyp", "cy": ""},
        "tree_path": f"{APPLICATION_BASE_PATH}.3.1",
    },
    {
        "section_name": {"en": "4. Your project", "cy": ""},
        "tree_path": f"{APPLICATION_BASE_PATH}.4",
        "requires_feedback": True,
    },
    {
        "section_name": {"en": "4.1 Outputs and outcomes", "cy": ""},
        "form_name_json": {"en": "outputs-and-outcomes-cyp", "cy": ""},
        "tree_path": f"{APPLICATION_BASE_PATH}.4.1",
    },
    {
        "section_name": {"en": "4.2 Existing work", "cy": ""},
        "form_name_json": {"en": "existing-work-cyp", "cy": ""},
        "tree_path": f"{APPLICATION_BASE_PATH}.4.2",
    },
    {
        "section_name": {"en": "4.3 Project milestones", "cy": ""},
        "form_name_json": {"en": "project-milestones-cyp", "cy": " "},
        "tree_path": f"{APPLICATION_BASE_PATH}.4.3",
    },
    {
        "section_name": {"en": "4.4 Objectives and activities", "cy": ""},
        "form_name_json": {"en": "objectives-and-activities-cyp", "cy": ""},
        "tree_path": f"{APPLICATION_BASE_PATH}.4.4",
    },
    {
        "section_name": {"en": "4.5 Location of activities", "cy": ""},
        "form_name_json": {"en": "location-of-activities-cyp", "cy": ""},
        "tree_path": f"{APPLICATION_BASE_PATH}.4.5",
    },
    {
        "section_name": {"en": "4.6 Working with fund beneficiaries", "cy": ""},
        "form_name_json": {"en": "working-with-fund-beneficiaries-cyp", "cy": ""},
        "tree_path": f"{APPLICATION_BASE_PATH}.4.6",
    },
    {
        "section_name": {"en": "5. Risk and deliverability", "cy": ""},
        "tree_path": f"{APPLICATION_BASE_PATH}.5",
        "requires_feedback": True,
    },
    {
        "section_name": {"en": "5.1 Risk and deliverability", "cy": ""},
        "form_name_json": {"en": "risk-and-deliverability-cyp", "cy": ""},
        "tree_path": f"{APPLICATION_BASE_PATH}.5.1",
    },
    {
        "section_name": {"en": "6. Value for money", "cy": ""},
        "tree_path": f"{APPLICATION_BASE_PATH}.6",
        "requires_feedback": True,
    },
    {
        "section_name": {"en": "6.1 Value for money", "cy": ""},
        "form_name_json": {"en": "value-for-money-cyp", "cy": ""},
        "tree_path": f"{APPLICATION_BASE_PATH}.6.1",
    },
    {
        "section_name": {"en": "7. Declarations", "cy": ""},
        "tree_path": f"{APPLICATION_BASE_PATH}.7",
    },
    {
        "section_name": {"en": "7.1 Declarations", "cy": ""},
        "form_name_json": {"en": "declarations-cyp", "cy": ""},
        "tree_path": f"{APPLICATION_BASE_PATH}.7.1",
    },
]

fund_config = {
    "id": CYP_FUND_ID,
    "name_json": {
        "en": "The Children and Young People's Resettlement Fund",
        "cy": "",
    },
    "title_json": {
        "en": (
            "funding to support children and young people on pathways to the UK from Ukraine, Hong Kong and Afghanistan"
        ),
        "cy": "",
    },
    "short_name": "CYP",
    "funding_type": FundingType.COMPETITIVE,
    "description_json": {"en": "", "cy": ""},
    "welsh_available": False,
    "owner_organisation_name": "Department for Levelling Up, Housing and Communities",
    "owner_organisation_shortname": "DLUHC",
    "owner_organisation_logo_uri": DLUHC_LOGO_PNG,
}

round_config = [
    {
        "id": CYP_ROUND_1_ID,
        "fund_id": CYP_FUND_ID,
        "title_json": {"en": "Round 1", "cy": "Rownd 1"},
        "short_name": "R1",
        "opens": CYP_R1_OPENS_DATE,
        "assessment_start": None,
        "deadline": CYP_R1_DEADLINE_DATE,
        "application_reminder_sent": True,
        "reminder_date": None,
        "assessment_deadline": CYP_R1_ASSESSMENT_DEADLINE_DATE,
        "prospectus": CYP_PROSPECTS_LINK,
        "privacy_notice": "https://www.gov.uk/guidance/the-children-and-young-peoples-resettlement-fund-privacy-notice",
        "contact_email": "cyprfund@communities.gov.uk",
        "instructions_json": None,
        "feedback_link": "",
        "project_name_field_id": "bsUoNG",
        "application_guidance_json": CYP_APPLICATION_GUIDANCE,
        "guidance_url": (
            "https://www.gov.uk/government/publications/"
            "the-children-and-young-peoples-resettlement-"
            "fund-prospectus/the-children-and-young-peoples-"
            "resettlement-fund-prospectus#scoring-criteria"
        ),
        "all_uploaded_documents_section_available": False,
        "application_fields_download_available": False,
        "display_logo_on_pdf_exports": False,
        "mark_as_complete_enabled": True,
        "is_expression_of_interest": False,
        "feedback_survey_config": {
            "has_feedback_survey": True,
            "has_section_feedback": True,
            "is_feedback_survey_optional": False,
            "is_section_feedback_optional": False,
        },
        "eligibility_config": {"has_eligibility": False},
        "eoi_decision_schema": None,
    }
]
