from datetime import datetime, timezone

from data.models import FundingType
from pre_award.fund_store.config.fund_loader_config.common_fund_config.fund_base_tree_paths import (
    DPI_R2_BASE_PATH,
)
from pre_award.fund_store.config.fund_loader_config.logo import DLUHC_LOGO_PNG

DPI_FUND_ID = "f493d512-5eb4-11ee-8c99-0242ac120002"
DPI_ROUND_2_ID = "0059aad4-5eb5-11ee-8c99-0242ac120002"
APPLICATION_BASE_PATH = ".".join([str(DPI_R2_BASE_PATH), str(1)])
ASSESSMENT_BASE_PATH = ".".join([str(DPI_R2_BASE_PATH), str(2)])
DPI_R2_OPENS_DATE = datetime(2023, 10, 17, 9, 30, 0, tzinfo=timezone.utc)  # 2023-10-17 10:00:00
DPI_R2_DEADLINE_DATE = datetime(2023, 12, 1, 17, 0, 0, tzinfo=timezone.utc)  # 2023-12-1 11:59:00
DPI_R2_ASSESSMENT_DEADLINE_DATE = datetime(2024, 1, 31, 12, 0, 0, tzinfo=timezone.utc)  # 2023-01-31 12:00:00

DPI_PROSPECTS_LINK = "https://www.localdigital.gov.uk/digital-planning/funding/digital-planning-programme-funding-2023"  # noqa
DPI_PRIVACY_NOTICE = "https://www.gov.uk/guidance/digital-planning-improvement-fund-privacy-notice"
DPI_APPLICATION_GUIDANCE = {
    "en": (
        "<h2 class='govuk-heading govuk-heading-s'>Before you start</h2><p"
        f" class='govuk-body'><a href='{DPI_PROSPECTS_LINK}'>Read the fund's prospectus</a>"
        " before you apply.</p><p class='govuk-body'>You can <a"
        " href='{all_questions_url}'>preview the full list of application"
        " questions</a>.</p>"
    )
}

r2_application_sections = [
    {
        "section_name": {"en": "1. Before you start", "cy": ""},
        "tree_path": f"{APPLICATION_BASE_PATH}.1",
    },
    {
        "section_name": {"en": "1.1 Name your application", "cy": ""},
        "form_name_json": {"en": "name-your-application", "cy": ""},
        "tree_path": f"{APPLICATION_BASE_PATH}.1.1",
    },
    {
        "section_name": {"en": "2. About your organisation", "cy": ""},
        "tree_path": f"{APPLICATION_BASE_PATH}.2",
        "requires_feedback": True,
    },
    {
        "section_name": {"en": "2.1 Organisation information", "cy": ""},
        "form_name_json": {"en": "organisation-information-dpi", "cy": ""},
        "tree_path": f"{APPLICATION_BASE_PATH}.2.1",
    },
    {
        "section_name": {"en": "3. Your skills and experience", "cy": ""},
        "tree_path": f"{APPLICATION_BASE_PATH}.3",
        "weighting": 50,
        "requires_feedback": True,
    },
    {
        "section_name": {"en": "3.1 Your skills and experience", "cy": ""},
        "form_name_json": {"en": "your-skills-and-experience-dpi", "cy": ""},
        "tree_path": f"{APPLICATION_BASE_PATH}.3.1",
    },
    {
        "section_name": {"en": "3.2 Roles and recruitment", "cy": ""},
        "form_name_json": {"en": "roles-and-recruitment-dpi", "cy": ""},
        "tree_path": f"{APPLICATION_BASE_PATH}.3.2",
    },
    {
        "section_name": {"en": "4. About your project", "cy": ""},
        "tree_path": f"{APPLICATION_BASE_PATH}.4",
        "weighting": 50,
        "requires_feedback": True,
    },
    {
        "section_name": {"en": "4.1 Engaging the ODP community", "cy": ""},
        "form_name_json": {"en": "engaging-the-odp-community-dpi", "cy": ""},
        "tree_path": f"{APPLICATION_BASE_PATH}.4.1",
    },
    {
        "section_name": {"en": "4.2 Engaging the organisation", "cy": ""},
        "form_name_json": {"en": "engaging-the-organisation-dpi", "cy": ""},
        "tree_path": f"{APPLICATION_BASE_PATH}.4.2",
    },
    {
        "section_name": {"en": "4.3 Dataset information", "cy": ""},
        "form_name_json": {"en": "dataset-information-dpi", "cy": ""},
        "tree_path": f"{APPLICATION_BASE_PATH}.4.3",
    },
    {
        "section_name": {"en": "5. Future work", "cy": ""},
        "tree_path": f"{APPLICATION_BASE_PATH}.5",
        "requires_feedback": True,
    },
    {
        "section_name": {"en": "5.1 Future work", "cy": ""},
        "form_name_json": {"en": "future-work-dpi", "cy": ""},
        "tree_path": f"{APPLICATION_BASE_PATH}.5.1",
    },
    {
        "section_name": {"en": "6. Declarations", "cy": ""},
        "tree_path": f"{APPLICATION_BASE_PATH}.6",
    },
    {
        "section_name": {"en": "6.1 Declarations", "cy": ""},
        "form_name_json": {"en": "declarations-dpi", "cy": ""},
        "tree_path": f"{APPLICATION_BASE_PATH}.6.1",
    },
]

fund_config = {
    "id": DPI_FUND_ID,
    "name_json": {
        "en": "Digital Planning Improvement Fund",
        "cy": "",
    },
    "title_json": {
        "en": "funding to begin your digital planning improvement journey",
        "cy": "",
    },
    "short_name": "DPIF",
    "funding_type": FundingType.COMPETITIVE,
    "description_json": {"en": "", "cy": ""},
    "welsh_available": False,
    "owner_organisation_name": "Department for Levelling Up, Housing and Communities",
    "owner_organisation_shortname": "DLUHC",
    "owner_organisation_logo_uri": DLUHC_LOGO_PNG,
}

round_config = [
    {
        "id": DPI_ROUND_2_ID,
        "fund_id": DPI_FUND_ID,
        "title_json": {"en": "Round 2", "cy": ""},
        "short_name": "R2",
        "opens": DPI_R2_OPENS_DATE,
        "assessment_start": None,
        "deadline": DPI_R2_DEADLINE_DATE,
        "application_reminder_sent": True,
        "reminder_date": None,
        "assessment_deadline": DPI_R2_ASSESSMENT_DEADLINE_DATE,
        "prospectus": DPI_PROSPECTS_LINK,
        "privacy_notice": DPI_PRIVACY_NOTICE,
        "contact_email": "digitalplanningteam@communities.gov.uk",
        "instructions_json": None,
        "feedback_link": "",
        "project_name_field_id": "JAAhRP",
        "application_guidance_json": DPI_APPLICATION_GUIDANCE,
        "guidance_url": (
            "https://docs.google.com/document/d/1cF5eKphoBWEUe0Zv5HBwv0R3n1svCk16kUFRJhKnIQY"
            "/edit#heading=h.b0vrhm5gih2k"
        ),
        "all_uploaded_documents_section_available": False,
        "application_fields_download_available": True,
        "display_logo_on_pdf_exports": False,
        "mark_as_complete_enabled": True,
        "is_expression_of_interest": False,
        "feedback_survey_config": {
            "has_feedback_survey": True,
            "has_section_feedback": True,
            "is_feedback_survey_optional": True,
            "is_section_feedback_optional": True,
        },
        "eligibility_config": {"has_eligibility": False},
        "eoi_decision_schema": None,
    }
]
