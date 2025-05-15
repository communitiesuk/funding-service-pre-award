from datetime import datetime, timezone

from data.models import FundingType
from pre_award.fund_store.config.fund_loader_config.common_fund_config.fund_base_tree_paths import (
    NSTF_R2_BASE_PATH,
)
from pre_award.fund_store.config.fund_loader_config.logo import DLUHC_LOGO_PNG

NIGHT_SHELTER_FUND_ID = "13b95669-ed98-4840-8652-d6b7a19964db"
NIGHT_SHELTER_ROUND_2_ID = "fc7aa604-989e-4364-98a7-d1234271435a"
APPLICATION_BASE_PATH = ".".join([str(NSTF_R2_BASE_PATH), str(1)])
ASSESSMENT_BASE_PATH = ".".join([str(NSTF_R2_BASE_PATH), str(2)])
NS_R2_OPENS_DATE = datetime(2023, 6, 7, 12, 0, 0, tzinfo=timezone.utc)  # 2023-06-07 12:00:00
NS_R2_DEADLINE_DATE = datetime(2023, 7, 7, 11, 59, 0, tzinfo=timezone.utc)  # 2023-07-07 11:59:00
NS_R2_ASSESSMENT_DEADLINE_DATE = datetime(2023, 8, 9, 12, 0, 0, tzinfo=timezone.utc)  # 2023-08-09 12:00:00

NIGHT_SHELTER_PROSPECTS_LINK = (
    "https://www.gov.uk/government/publications/night-shelter-transformation-fund-round-2-prospectus"
)
NIGHT_SHELTER_APPLICATION_GUIDANCE = {
    "en": (
        "<h2 class='govuk-heading govuk-heading-s'>Before you start</h2><p"
        f" class='govuk-body'><a href='{NIGHT_SHELTER_PROSPECTS_LINK}'>Read the fund's"
        " prospectus</a> before you apply.</p>"
    )
}

r2_application_sections = [
    {
        "section_name": {"en": "Before you start", "cy": ""},
        "tree_path": f"{APPLICATION_BASE_PATH}.1",
    },
    {
        "section_name": {"en": "Name your application", "cy": ""},
        "form_name_json": {"en": "name-your-application-ns", "cy": ""},
        "tree_path": f"{APPLICATION_BASE_PATH}.1.1",
    },
    {
        "section_name": {"en": "1. About your organisation", "cy": ""},
        "tree_path": f"{APPLICATION_BASE_PATH}.2",
    },
    {
        "section_name": {"en": "1.1 Organisation information", "cy": ""},
        "form_name_json": {"en": "organisation-information-ns", "cy": ""},
        "tree_path": f"{APPLICATION_BASE_PATH}.2.1",
    },
    {
        "section_name": {"en": "1.2 Organisation type", "cy": ""},
        "form_name_json": {"en": "organisation-type-ns", "cy": ""},
        "tree_path": f"{APPLICATION_BASE_PATH}.2.2",
    },
    {
        "section_name": {"en": "1.3 Applicant information", "cy": ""},
        "form_name_json": {"en": "applicant-information-ns", "cy": ""},
        "tree_path": f"{APPLICATION_BASE_PATH}.2.3",
    },
    {
        "section_name": {"en": "1.4 Joint applications", "cy": ""},
        "form_name_json": {"en": "joint-applications-ns", "cy": ""},
        "tree_path": f"{APPLICATION_BASE_PATH}.2.4",
    },
    {
        "section_name": {"en": "2. Your skills and experience", "cy": ""},
        "tree_path": f"{APPLICATION_BASE_PATH}.3",
        "weighting": 15,
    },
    {
        "section_name": {"en": "2.1 Staff and volunteers", "cy": ""},
        "form_name_json": {"en": "staff-and-volunteers-ns", "cy": ""},
        "tree_path": f"{APPLICATION_BASE_PATH}.3.1",
    },
    {
        "section_name": {"en": "2.2 Current services", "cy": ""},
        "form_name_json": {"en": "current-services-ns", "cy": ""},
        "tree_path": f"{APPLICATION_BASE_PATH}.3.2",
    },
    {
        "section_name": {"en": "3. Your proposal", "cy": ""},
        "tree_path": f"{APPLICATION_BASE_PATH}.4",
        "weighting": 40,
    },
    {
        "section_name": {"en": "3.1 Objectives and activities", "cy": ""},
        "form_name_json": {"en": "objectives-and-activities-ns", "cy": ""},
        "tree_path": f"{APPLICATION_BASE_PATH}.4.1",
    },
    {
        "section_name": {"en": "3.2 Project milestones", "cy": ""},
        "form_name_json": {"en": "project-milestones-ns", "cy": ""},
        "tree_path": f"{APPLICATION_BASE_PATH}.4.2",
    },
    {
        "section_name": {"en": "3.3 Local need and support", "cy": ""},
        "form_name_json": {"en": "local-need-and-support-ns", "cy": ""},
        "tree_path": f"{APPLICATION_BASE_PATH}.4.3",
    },
    {
        "section_name": {"en": "3.4 Proposed services", "cy": ""},
        "form_name_json": {"en": "proposed-services-ns", "cy": ""},
        "tree_path": f"{APPLICATION_BASE_PATH}.4.4",
    },
    {
        "section_name": {"en": "3.5 Working in partnership", "cy": ""},
        "form_name_json": {"en": "working-in-partnership-ns", "cy": ""},
        "tree_path": f"{APPLICATION_BASE_PATH}.4.5",
    },
    {
        "section_name": {"en": "3.6 Proposal sustainability", "cy": ""},
        "form_name_json": {"en": "proposal-sustainability-ns", "cy": ""},
        "tree_path": f"{APPLICATION_BASE_PATH}.4.6",
    },
    {
        "section_name": {"en": "4. Outputs and outcomes", "cy": ""},
        "tree_path": f"{APPLICATION_BASE_PATH}.5",
        "weighting": 15,
    },
    {
        "section_name": {"en": "4.1 Outputs and outcomes", "cy": ""},
        "form_name_json": {"en": "outputs-and-outcomes-ns", "cy": ""},
        "tree_path": f"{APPLICATION_BASE_PATH}.5.1",
    },
    {
        "section_name": {"en": "5. Risk and deliverability", "cy": ""},
        "tree_path": f"{APPLICATION_BASE_PATH}.6",
        "weighting": 15,
    },
    {
        "section_name": {"en": "5.1 Risk and deliverability", "cy": ""},
        "form_name_json": {"en": "risk-and-deliverability-ns", "cy": ""},
        "tree_path": f"{APPLICATION_BASE_PATH}.6.1",
    },
    {
        "section_name": {"en": "6. Value for money", "cy": ""},
        "tree_path": f"{APPLICATION_BASE_PATH}.7",
        "weighting": 15,
    },
    {
        "section_name": {"en": "6.1 Funding required", "cy": ""},
        "form_name_json": {"en": "funding-required-ns", "cy": ""},
        "tree_path": f"{APPLICATION_BASE_PATH}.7.1",
    },
    {
        "section_name": {"en": "6.2 Building works", "cy": ""},
        "form_name_json": {"en": "building-works-ns", "cy": ""},
        "tree_path": f"{APPLICATION_BASE_PATH}.7.2",
    },
    {
        "section_name": {"en": "6.3 Match funding", "cy": ""},
        "form_name_json": {"en": "match-funding-ns", "cy": ""},
        "tree_path": f"{APPLICATION_BASE_PATH}.7.3",
    },
    {
        "section_name": {"en": "7. Declarations", "cy": ""},
        "tree_path": f"{APPLICATION_BASE_PATH}.8",
    },
    {
        "section_name": {"en": "7.1 Declarations", "cy": ""},
        "form_name_json": {"en": "declarations-ns", "cy": ""},
        "tree_path": f"{APPLICATION_BASE_PATH}.8.1",
    },
]

fund_config = {
    "id": NIGHT_SHELTER_FUND_ID,
    "name_json": {
        "en": "Night Shelter Transformation Fund",
        "cy": "",
    },
    "title_json": {
        "en": "funding to transform your night shelter services in England",
        "cy": "",
    },
    "funding_type": FundingType.COMPETITIVE,
    "short_name": "NSTF",
    "description_json": {"en": "", "cy": ""},
    "welsh_available": False,
    "owner_organisation_name": "Department for Levelling Up, Housing and Communities",
    "owner_organisation_shortname": "DLUHC",
    "owner_organisation_logo_uri": DLUHC_LOGO_PNG,
}

round_config = [
    {
        "id": NIGHT_SHELTER_ROUND_2_ID,
        "fund_id": NIGHT_SHELTER_FUND_ID,
        "title_json": {"en": "Round 2", "cy": ""},
        "short_name": "R2",
        "opens": NS_R2_OPENS_DATE,
        "assessment_start": None,
        "deadline": NS_R2_DEADLINE_DATE,
        "application_reminder_sent": True,
        "reminder_date": None,
        "assessment_deadline": NS_R2_ASSESSMENT_DEADLINE_DATE,
        "prospectus": NIGHT_SHELTER_PROSPECTS_LINK,
        "privacy_notice": "https://www.gov.uk/guidance/night-shelter-transformation-fund-2022-2025-privacy-notice",
        "contact_email": "transformationfund@communities.gov.uk",
        "instructions_json": None,
        "feedback_link": "https://forms.office.com/e/n6J9KPebUy",
        "project_name_field_id": "YVsPtE",
        "application_guidance_json": NIGHT_SHELTER_APPLICATION_GUIDANCE,
        "guidance_url": (
            "https://mhclg.sharepoint.com.mcas.ms/:w:/s/HomelessnessandRoughSleeping/EZn"
            "-Dq3eBvFDtdBqhyEZxUUBj_BP53F9TVyI0imX3NdcPw?e=PtmLwH"
        ),
        "all_uploaded_documents_section_available": False,
        "application_fields_download_available": False,
        "display_logo_on_pdf_exports": False,
        "mark_as_complete_enabled": False,
        "is_expression_of_interest": False,
        "feedback_survey_config": {
            "has_feedback_survey": False,
            "has_section_feedback": False,
            "is_feedback_survey_optional": True,
            "is_section_feedback_optional": True,
        },
        "eligibility_config": {"has_eligibility": False},
        "eoi_decision_schema": None,
    }
]
