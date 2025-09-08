# flake8: noqa
import textwrap
from datetime import datetime
from datetime import timezone

from pre_award.fund_store.config.fund_loader_config.cof.shared import COF_APPLICATION_GUIDANCE
from pre_award.fund_store.config.fund_loader_config.cof.shared import fund_config
from pre_award.fund_store.config.fund_loader_config.common_fund_config.fund_base_tree_paths import (
    COF_R2_W2_BASE_PATH,
)

COF_FUND_ID = fund_config["id"]
COF_ROUND_2_WINDOW_2_ID = "c603d114-5364-4474-a0c4-c41cbf4d3bbd"
COF_ROUND_2_WINDOW_3_ID = "5cf439bf-ef6f-431e-92c5-a1d90a4dd32f"
APPLICATION_BASE_PATH = ".".join([str(COF_R2_W2_BASE_PATH), str(1)])
ASSESSMENT_BASE_PATH = ".".join([str(COF_R2_W2_BASE_PATH), str(2)])
COF_R2_OPENS_DATE = datetime(2022, 10, 4, 12, 0, 0, tzinfo=timezone.utc)  # 2022-10-04 12:00:00
COF_R2_DEADLINE_DATE = datetime(2022, 12, 14, 11, 59, 0, tzinfo=timezone.utc)  # 2022-12-14 11:59:00
COF_R2_ASSESSMENT_DEADLINE_DATE = datetime(2023, 3, 30, 12, 0, 0, tzinfo=timezone.utc)  # 2023-03-30 12:00:00

rounds_config = [
    {
        "id": COF_ROUND_2_WINDOW_2_ID,
        "title_json": {
            "en": "Round 2 Window 2",
            "cy": "Round 2 Window 2",
        },  # TODO: Provide welsh translation
        "short_name": "R2W2",
        "opens": COF_R2_OPENS_DATE,
        "assessment_start": None,
        "deadline": COF_R2_DEADLINE_DATE,
        "application_reminder_sent": True,
        "reminder_date": None,
        "fund_id": "47aef2f5-3fcb-4d45-acb5-f0152b5f03c4",
        "assessment_deadline": COF_R2_ASSESSMENT_DEADLINE_DATE,
        "prospectus": "https://www.gov.uk/government/publications/community-ownership-fund-prospectus",
        "privacy_notice": (
            (
                "https://www.gov.uk/government/publications/community-ownership-fund-privacy-notice/"
                "community-ownership-fund-privacy-notice"
            ),
        ),
        "contact_email": "COF@communities.gov.uk",
        "instructions_json": {
            "en": (
                "You must have received an invitation to apply. If we did not invite you,"
                " first <a"
                ' href="https://www.gov.uk/government/publications/community-ownership-fund-prospectus">'
                " express your interest in the fund</a>."
            ),
            "cy": (
                "You must have received an invitation to apply. If we did not invite you,"
                " first <a"
                ' href="https://www.gov.uk/government/publications/community-ownership-fund-prospectus">'
                " express your interest in the fund</a>."
            ),
        },
        "feedback_link": (
            "https://forms.office.com/Pages/ResponsePage.aspx?id="
            "EGg0v32c3kOociSi7zmVqN48ORk8WN5LlJITE3Swt-lURUNCR0dHMjgxWFZOMTMxQzlOTVIxVkQ0Sy4u"
        ),
        "project_name_field_id": "KAgrBz",
        "application_guidance_json": COF_APPLICATION_GUIDANCE,
        "guidance_url": (
            "https://mhclg.sharepoint.com.mcas.ms/:w:/s/CommunityOwnershipFund"
            "/Ecv3iM7U0AtKtyHnzRrQ9dsB0HdMPvHWqAoGn1WrWM7EMA?e=6QpdUT"
        ),
        "all_uploaded_documents_section_available": True,
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
    },
    {
        "id": COF_ROUND_2_WINDOW_3_ID,
        "title_json": {
            "en": "Round 2 Window 3",
            "cy": "Round 2 Window 3",
        },  # TODO: Provide welsh translation
        "short_name": "R2W3",
        "opens": "2022-10-04 12:00:00",
        "assessment_start": None,
        "deadline": "2023-04-14 11:59:00",
        "application_reminder_sent": True,
        "reminder_date": None,
        "fund_id": "47aef2f5-3fcb-4d45-acb5-f0152b5f03c4",
        "assessment_deadline": "2023-05-17 12:00:00",
        "prospectus": "https://www.gov.uk/government/publications/community-ownership-fund-prospectus",
        "privacy_notice": (
            "https://www.gov.uk/government/publications/community-ownership-fund-privacy-notice/"
            "community-ownership-fund-privacy-notice"
        ),
        "contact_email": "COF@communities.gov.uk",
        "instructions_json": {
            "en": (
                "You must have received an invitation to apply. If we did not invite you,"
                " first <a"
                ' href="https://www.gov.uk/government/publications/community-ownership-fund-prospectus">'
                " express your interest in the fund</a>."
            ),
            "cy": (
                "You must have received an invitation to apply. If we did not invite you,"
                " first <a"
                ' href="https://www.gov.uk/government/publications/community-ownership-fund-prospectus">'
                " express your interest in the fund</a>."
            ),
        },
        "feedback_link": (
            "https://forms.office.com/Pages/ResponsePage.aspx?id="
            "EGg0v32c3kOociSi7zmVqFJBHpeOL2tNnpiwpdL2iElUREIySU9OWTU4R0RTNjhBUDE1Q1VYVFBEMi4u"
        ),
        "project_name_field_id": "KAgrBz",
        "application_guidance_json": COF_APPLICATION_GUIDANCE,
        "guidance_url": (
            "https://mhclg.sharepoint.com.mcas.ms/:w:/s/CommunityOwnershipFund"
            "/Ecv3iM7U0AtKtyHnzRrQ9dsB0HdMPvHWqAoGn1WrWM7EMA?e=6QpdUT"
        ),
        "all_uploaded_documents_section_available": True,
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
    },
]

cof_r2_sections = [
    {
        "section_name": {
            "en": "1. About your organisation",
            "cy": "1. Ynglŷn â'ch sefydliad",
        },
        "tree_path": f"{APPLICATION_BASE_PATH}.1",
    },
    {
        "section_name": {
            "en": "Organisation Information",
            "cy": "Gwybodaeth am y sefydliad",
        },
        "tree_path": f"{APPLICATION_BASE_PATH}.1.1",
        "form_name_json": {
            "en": "cof-r2-en-organisation-information",
            "cy": "gwybodaeth-am-y-sefydliad",
        },
    },
    {
        "section_name": {
            "en": "Applicant Information",
            "cy": "Gwybodaeth am yr ymgeisydd",
        },
        "tree_path": f"{APPLICATION_BASE_PATH}.1.2",
        "form_name_json": {
            "en": "applicant-information",
            "cy": "gwybodaeth-am-y-ymgeisydd",
        },
    },
    {
        "section_name": {
            "en": "2. About your project",
            "cy": "2. Ynglŷn â'ch prosiect",
        },
        "tree_path": f"{APPLICATION_BASE_PATH}.2",
    },
    {
        "section_name": {"en": "Project Information", "cy": "Gwybodaeth am y prosiect"},
        "tree_path": f"{APPLICATION_BASE_PATH}.2.1",
        "form_name_json": {
            "en": "project-information",
            "cy": "gwybodaeth-am-y-prosiect",
        },
    },
    {
        "section_name": {"en": "Asset Information", "cy": "Gwybodaeth am yr ased"},
        "tree_path": f"{APPLICATION_BASE_PATH}.2.2",
        "form_name_json": {"en": "asset-information", "cy": "gwybodaeth-am-yr-ased"},
    },
    {
        "section_name": {"en": "3. Strategic case", "cy": "3. Achos strategol"},
        "tree_path": f"{APPLICATION_BASE_PATH}.3",
        "weighting": 30,
    },
    {
        "section_name": {"en": "Community Use", "cy": "Defnydd Cymunedol"},
        "tree_path": f"{APPLICATION_BASE_PATH}.3.1",
        "form_name_json": {"en": "community-use", "cy": "defnydd-cymunedol"},
    },
    {
        "section_name": {"en": "Community Engagement", "cy": "Ymgysylltu â'r gymuned"},
        "tree_path": f"{APPLICATION_BASE_PATH}.3.2",
        "form_name_json": {
            "en": "community-engagement",
            "cy": "ymgysylltu-a'r-gymuned",
        },
    },
    {
        "section_name": {"en": "Local Support", "cy": "Cefnogaeth leol"},
        "tree_path": f"{APPLICATION_BASE_PATH}.3.3",
        "form_name_json": {"en": "local-support", "cy": "cefnogaeth-leol"},
    },
    {
        "section_name": {
            "en": "Environmental Sustainability",
            "cy": "Cynaliadwyedd amgylcheddol",
        },
        "tree_path": f"{APPLICATION_BASE_PATH}.3.4",
        "form_name_json": {
            "en": "environmental-sustainability",
            "cy": "cynaliadwyedd-amgylcheddol",
        },
    },
    {
        "section_name": {"en": "4. Management case", "cy": "4. Achos rheoli"},
        "tree_path": f"{APPLICATION_BASE_PATH}.4",
        "weighting": 30,
    },
    {
        "section_name": {"en": "Funding Required", "cy": "Cyllid sydd ei angen"},
        "tree_path": f"{APPLICATION_BASE_PATH}.4.1",
        "form_name_json": {"en": "funding-required", "cy": "cyllid-sydd-ei-angen"},
    },
    {
        "section_name": {"en": "Feasibility", "cy": "Dichonoldeb"},
        "tree_path": f"{APPLICATION_BASE_PATH}.4.2",
        "form_name_json": {"en": "feasibility", "cy": "cynhwysiant-ac-integreiddio"},
    },
    {
        "section_name": {"en": "Risk", "cy": "Risg"},
        "tree_path": f"{APPLICATION_BASE_PATH}.4.3",
        "form_name_json": {"en": "risk", "cy": "risg"},
    },
    {
        "section_name": {"en": "Project Costs", "cy": "Costau'r prosiect"},
        "tree_path": f"{APPLICATION_BASE_PATH}.4.4",
        "form_name_json": {"en": "project-costs", "cy": "costau'r-prosiect"},
    },
    {
        "section_name": {"en": "Skills And Resources", "cy": "Sgiliau ac Adnoddau"},
        "tree_path": f"{APPLICATION_BASE_PATH}.4.5",
        "form_name_json": {"en": "skills-and-resources", "cy": "sgiliau-ac-adnoddau"},
    },
    {
        "section_name": {
            "en": "Community Representation",
            "cy": "Cynrychiolaeth gymunedol",
        },
        "tree_path": f"{APPLICATION_BASE_PATH}.4.6",
        "form_name_json": {
            "en": "community-representation",
            "cy": "cynrychiolaeth-gymunedol",
        },
    },
    {
        "section_name": {
            "en": "Inclusiveness And Integration",
            "cy": "Cynhwysiant ac Integreiddio",
        },
        "tree_path": f"{APPLICATION_BASE_PATH}.4.7",
        "form_name_json": {
            "en": "inclusiveness-and-integration",
            "cy": "cynhwysiant-ac-integreiddio",
        },
    },
    {
        "section_name": {
            "en": "Upload Business Plan",
            "cy": "Lanlwythwch y cynllun busnes",
        },
        "tree_path": f"{APPLICATION_BASE_PATH}.4.8",
        "form_name_json": {
            "en": "upload-business-plan",
            "cy": "lanlwythwch-y-cynllun-busnes",
        },
    },
    {
        "section_name": {
            "en": "5. Potential to deliver community benefits",
            "cy": "5. Potensial i gyflawni buddion cymunedol",
        },
        "tree_path": f"{APPLICATION_BASE_PATH}.5",
        "weighting": 30,
    },
    {
        "section_name": {"en": "Community Benefits", "cy": "Buddion cymunedol"},
        "tree_path": f"{APPLICATION_BASE_PATH}.5.1",
        "form_name_json": {"en": "community-benefits", "cy": "ymgysylltu-a'r-gymuned"},
    },
    {
        "section_name": {
            "en": "6. Added value to community",
            "cy": "6. Gwerth ychwanegol i'r gymuned",
        },
        "tree_path": f"{APPLICATION_BASE_PATH}.6",
        "weighting": 10,
    },
    {
        "section_name": {"en": "Value To The Community", "cy": "Gwerth i'r Gymuned"},
        "tree_path": f"{APPLICATION_BASE_PATH}.6.1",
        "form_name_json": {"en": "value-to-the-community", "cy": "gwerth-i'r-gymuned"},
    },
    {
        "section_name": {
            "en": "7. Subsidy control / state aid",
            "cy": "7. Rheoli cymorthdaliadau a chymorth gwladwriaethol",
        },
        "tree_path": f"{APPLICATION_BASE_PATH}.7",
    },
    {
        "section_name": {"en": "Project Qualification", "cy": "Cymhwystra'r prosiect"},
        "tree_path": f"{APPLICATION_BASE_PATH}.7.1",
        "form_name_json": {
            "en": "project-qualification",
            "cy": "cymhwystra'r-prosiect",
        },
    },
    {
        "section_name": {"en": "8. Check declarations", "cy": "8. Gwirio datganiadau"},
        "tree_path": f"{APPLICATION_BASE_PATH}.8",
    },
    {
        "section_name": {"en": "Declarations", "cy": "Datganiadau"},
        "tree_path": f"{APPLICATION_BASE_PATH}.8.1",
        "form_name_json": {"en": "cof-r2-en-declarations", "cy": "datganiadau"},
    },
]
