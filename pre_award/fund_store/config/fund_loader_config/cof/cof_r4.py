# flake8: noqa
import textwrap
from datetime import datetime
from datetime import timezone

from pre_award.fund_store.config.fund_loader_config.cof.shared import COF_APPLICATION_GUIDANCE
from pre_award.fund_store.config.fund_loader_config.cof.shared import fund_config
from pre_award.fund_store.config.fund_loader_config.common_fund_config.fund_base_tree_paths import (
    COF_R4_W1_BASE_PATH,
)
from pre_award.fund_store.config.fund_loader_config.common_fund_config.fund_base_tree_paths import (
    COF_R4_W2_BASE_PATH,
)

COF_FUND_ID = fund_config["id"]
COF_ROUND_4_WINDOW_1_ID = "33726b63-efce-4749-b149-20351346c76e"
COF_ROUND_4_WINDOW_2_ID = "27ab26c2-e58e-4bfe-917d-64be10d16496"

APPLICATION_BASE_PATH_COF_R4_W1 = ".".join([str(COF_R4_W1_BASE_PATH), str(1)])
ASSESSMENT_BASE_PATH_COF_R4_W1 = ".".join([str(COF_R4_W1_BASE_PATH), str(2)])

APPLICATION_BASE_PATH_COF_R4_W2 = ".".join([str(COF_R4_W2_BASE_PATH), str(1)])
ASSESSMENT_BASE_PATH_COF_R4_W2 = ".".join([str(COF_R4_W2_BASE_PATH), str(2)])


COF_R4W1_OPENS_DATE = datetime(2024, 3, 25, 14, 00, 0, tzinfo=timezone.utc)  # 2024-03-25 14:00:00
COF_R4W1_SEND_REMINDER_DATE = datetime(2024, 4, 8, 11, 59, 0, tzinfo=timezone.utc)  # 2024-04-08 11:59:00
COF_R4W1_DEADLINE_DATE = datetime(2024, 4, 10, 14, 00, 0, tzinfo=timezone.utc)  # 2024-04-10 14:00:00
COF_R4W1_ASSESSMENT_DEADLINE_DATE = datetime(2024, 6, 23, 12, 0, 0, tzinfo=timezone.utc)  # 2024-06-23 12:00:00


COF_R4W2_OPENS_DATE = datetime(2024, 5, 22, 14, 00, 0, tzinfo=timezone.utc)  # 2024-05-22 14:00:00
COF_R4W2_SEND_REMINDER_DATE = datetime(2024, 5, 22, 11, 59, 0, tzinfo=timezone.utc)  # 2024-05-22 11:59:00
COF_R4W2_DEADLINE_DATE = datetime(2024, 6, 26, 14, 00, 0, tzinfo=timezone.utc)  # 2024-06-26 14:00:00
COF_R4W2_ASSESSMENT_START_DATE = datetime(2024, 5, 22, 14, 00, 0, tzinfo=timezone.utc)  # 2024-05-22 14:00:00
COF_R4W2_ASSESSMENT_DEADLINE_DATE = datetime(2024, 7, 31, 12, 0, 0, tzinfo=timezone.utc)  # 2024-07-31 12:00:00

# Date far in the future as a temporary measure to stop this going live by accident
COF_R4W2_HOLD_DATE = datetime(2124, 1, 1, 11, 59, 0)  # 2124-01-01 11:59:00


cof_r4w1_sections = [
    {
        "section_name": {
            "en": "1. About your organisation",
            "cy": "1. Ynglŷn â'ch sefydliad",
        },
        "tree_path": f"{APPLICATION_BASE_PATH_COF_R4_W1}.1",
        "requires_feedback": True,
    },
    {
        "section_name": {
            "en": "1.1 Organisation information",
            "cy": "1.1 Gwybodaeth am y sefydliad",
        },
        "form_name_json": {
            "en": "organisation-information-cof",
            "cy": "gwybodaeth-am-y-sefydliad-cof",
        },
        "tree_path": f"{APPLICATION_BASE_PATH_COF_R4_W1}.1.1",
    },
    {
        "section_name": {
            "en": "1.2 Applicant information",
            "cy": "1.2 Gwybodaeth am yr ymgeisydd",
        },
        "form_name_json": {
            "en": "applicant-information-cof",
            "cy": "gwybodaeth-am-yr-ymgeisydd-cof",
        },
        "tree_path": f"{APPLICATION_BASE_PATH_COF_R4_W1}.1.2",
    },
    {
        "section_name": {
            "en": "2. About your project",
            "cy": "2. Ynglŷn â'ch prosiect",
        },
        "tree_path": f"{APPLICATION_BASE_PATH_COF_R4_W1}.2",
        "requires_feedback": True,
    },
    {
        "section_name": {
            "en": "2.1 Project information",
            "cy": "2.1 Gwybodaeth am y prosiect",
        },
        "form_name_json": {
            "en": "project-information-cof",
            "cy": "gwybodaeth-am-y-prosiect-cof",
        },
        "tree_path": f"{APPLICATION_BASE_PATH_COF_R4_W1}.2.1",
    },
    {
        "section_name": {
            "en": "2.2 Asset information",
            "cy": "2.2 Gwybodaeth am yr ased",
        },
        "form_name_json": {
            "en": "asset-information-cof",
            "cy": "gwybodaeth-am-yr-ased-cof",
        },
        "tree_path": f"{APPLICATION_BASE_PATH_COF_R4_W1}.2.2",
    },
    {
        "section_name": {"en": "3. Strategic case", "cy": "3. Achos strategol"},
        "tree_path": f"{APPLICATION_BASE_PATH_COF_R4_W1}.3",
        "requires_feedback": True,
        "weighting": 53,
    },
    {
        "section_name": {
            "en": "3.1 Community use/significance",
            "cy": "3.1 Defnydd/arwyddocâd cymunedol",
        },
        "form_name_json": {
            "en": "community-use-cof",
            "cy": "defnydd-cymunedol-cof",
        },
        "tree_path": f"{APPLICATION_BASE_PATH_COF_R4_W1}.3.1",
    },
    {
        "section_name": {
            "en": "3.2 Community engagement",
            "cy": "3.2 Ymgysylltu â'r gymuned",
        },
        "form_name_json": {
            "en": "community-engagement-cof",
            "cy": "ymgysylltiad-cymunedol-cof",
        },
        "tree_path": f"{APPLICATION_BASE_PATH_COF_R4_W1}.3.2",
    },
    {
        "section_name": {"en": "3.3 Local support", "cy": "3.3 Cefnogaeth leol"},
        "form_name_json": {
            "en": "local-support-cof",
            "cy": "cefnogaeth-leol-cof",
        },
        "tree_path": f"{APPLICATION_BASE_PATH_COF_R4_W1}.3.3",
    },
    {
        "section_name": {
            "en": "3.4 Community benefits",
            "cy": "3.4 Buddion cymunedol",
        },
        "form_name_json": {
            "en": "community-benefits-cof",
            "cy": "buddion-cymunedol-cof",
        },
        "tree_path": f"{APPLICATION_BASE_PATH_COF_R4_W1}.3.4",
    },
    {
        "section_name": {
            "en": "3.5 Environmental sustainability",
            "cy": "3.5 Cynaliadwyedd amgylcheddol",
        },
        "form_name_json": {
            "en": "environmental-sustainability-cof",
            "cy": "cynaliadwyedd-amgylcheddol-cof",
        },
        "tree_path": f"{APPLICATION_BASE_PATH_COF_R4_W1}.3.5",
    },
    {
        "section_name": {"en": "4. Management case", "cy": "4. Achos rheoli"},
        "tree_path": f"{APPLICATION_BASE_PATH_COF_R4_W1}.4",
        "weighting": 47,
        "requires_feedback": True,
    },
    {
        "section_name": {
            "en": "4.1 Funding required",
            "cy": "4.1 Cyllid sydd ei angen",
        },
        "form_name_json": {
            "en": "funding-required-cof",
            "cy": "cyllid-sydd-ei-angen-cof",
        },
        "tree_path": f"{APPLICATION_BASE_PATH_COF_R4_W1}.4.1",
    },
    {
        "section_name": {"en": "4.2 Feasibility", "cy": "4.2 Dichonoldeb"},
        "form_name_json": {
            "en": "feasibility-cof",
            "cy": "dichonoldeb-cof",
        },
        "tree_path": f"{APPLICATION_BASE_PATH_COF_R4_W1}.4.2",
    },
    {
        "section_name": {"en": "4.3 Risk", "cy": "4.3 Risg"},
        "form_name_json": {"en": "risk-cof", "cy": "risg-cof"},
        "tree_path": f"{APPLICATION_BASE_PATH_COF_R4_W1}.4.3",
    },
    {
        "section_name": {"en": "4.4 Operational costs", "cy": "4.4 Costau gweithredol"},
        "form_name_json": {
            "en": "operational-costs-cof",
            "cy": "costau-gweithredol-cof",
        },
        "tree_path": f"{APPLICATION_BASE_PATH_COF_R4_W1}.4.4",
    },
    {
        "section_name": {
            "en": "4.5 Skills and resources",
            "cy": "4.5 Sgiliau ac adnoddau",
        },
        "form_name_json": {
            "en": "skills-and-resources-cof",
            "cy": "sgiliau-ac-adnoddau-cof",
        },
        "tree_path": f"{APPLICATION_BASE_PATH_COF_R4_W1}.4.5",
    },
    {
        "section_name": {
            "en": "4.6 Community representation",
            "cy": "4.6 Cynrychiolaeth gymunedol",
        },
        "form_name_json": {
            "en": "community-representation-cof",
            "cy": "cynrychiolaeth-gymunedol-cof",
        },
        "tree_path": f"{APPLICATION_BASE_PATH_COF_R4_W1}.4.6",
    },
    {
        "section_name": {
            "en": "4.7 Inclusiveness and integration",
            "cy": "4.7 Cynhwysiant ac integreiddio",
        },
        "form_name_json": {
            "en": "inclusiveness-and-integration-cof",
            "cy": "cynhwysiant-ac-integreiddio-cof",
        },
        "tree_path": f"{APPLICATION_BASE_PATH_COF_R4_W1}.4.7",
    },
    {
        "section_name": {
            "en": "4.8 Upload business plan",
            "cy": "4.8 Lanlwythwch y cynllun busnes",
        },
        "form_name_json": {
            "en": "upload-business-plan-cof",
            "cy": "lanlwythwch-y-cynllun-busnes-cof",
        },
        "tree_path": f"{APPLICATION_BASE_PATH_COF_R4_W1}.4.8",
    },
    {
        "section_name": {"en": "5. Check declarations", "cy": "5. Gwirio datganiadau"},
        "tree_path": f"{APPLICATION_BASE_PATH_COF_R4_W1}.5",
    },
    {
        "section_name": {"en": "5.1 Declarations", "cy": "5.1 Datganiadau"},
        "form_name_json": {
            "en": "declarations-cof",
            "cy": "cadarnhadau-terfynol-cof",
        },
        "tree_path": f"{APPLICATION_BASE_PATH_COF_R4_W1}.5.1",
    },
]

cof_r4w2_sections = [
    {
        "section_name": {
            "en": "1. About your organisation",
            "cy": "1. Ynglŷn â'ch sefydliad",
        },
        "tree_path": f"{APPLICATION_BASE_PATH_COF_R4_W2}.1",
        "requires_feedback": True,
    },
    {
        "section_name": {
            "en": "1.1 Organisation information",
            "cy": "1.1 Gwybodaeth am y sefydliad",
        },
        "form_name_json": {
            "en": "organisation-information-cof",
            "cy": "gwybodaeth-am-y-sefydliad-cof",
        },
        "tree_path": f"{APPLICATION_BASE_PATH_COF_R4_W2}.1.1",
    },
    {
        "section_name": {
            "en": "1.2 Applicant information",
            "cy": "1.2 Gwybodaeth am yr ymgeisydd",
        },
        "form_name_json": {
            "en": "applicant-information-cof",
            "cy": "gwybodaeth-am-yr-ymgeisydd-cof",
        },
        "tree_path": f"{APPLICATION_BASE_PATH_COF_R4_W2}.1.2",
    },
    {
        "section_name": {
            "en": "2. About your project",
            "cy": "2. Ynglŷn â'ch prosiect",
        },
        "tree_path": f"{APPLICATION_BASE_PATH_COF_R4_W2}.2",
        "requires_feedback": True,
    },
    {
        "section_name": {
            "en": "2.1 Project information",
            "cy": "2.1 Gwybodaeth am y prosiect",
        },
        "form_name_json": {
            "en": "project-information-cof",
            "cy": "gwybodaeth-am-y-prosiect-cof",
        },
        "tree_path": f"{APPLICATION_BASE_PATH_COF_R4_W2}.2.1",
    },
    {
        "section_name": {
            "en": "2.2 Asset information",
            "cy": "2.2 Gwybodaeth am yr ased",
        },
        "form_name_json": {
            "en": "asset-information-cof",
            "cy": "gwybodaeth-am-yr-ased-cof",
        },
        "tree_path": f"{APPLICATION_BASE_PATH_COF_R4_W2}.2.2",
    },
    {
        "section_name": {"en": "3. Strategic case", "cy": "3. Achos strategol"},
        "tree_path": f"{APPLICATION_BASE_PATH_COF_R4_W2}.3",
        "requires_feedback": True,
        "weighting": 53,
    },
    {
        "section_name": {
            "en": "3.1 Community use/significance",
            "cy": "3.1 Defnydd/arwyddocâd cymunedol",
        },
        "form_name_json": {
            "en": "community-use-cof",
            "cy": "defnydd-cymunedol-cof",
        },
        "tree_path": f"{APPLICATION_BASE_PATH_COF_R4_W2}.3.1",
    },
    {
        "section_name": {
            "en": "3.2 Community engagement",
            "cy": "3.2 Ymgysylltu â'r gymuned",
        },
        "form_name_json": {
            "en": "community-engagement-cof",
            "cy": "ymgysylltiad-cymunedol-cof",
        },
        "tree_path": f"{APPLICATION_BASE_PATH_COF_R4_W2}.3.2",
    },
    {
        "section_name": {"en": "3.3 Local support", "cy": "3.3 Cefnogaeth leol"},
        "form_name_json": {
            "en": "local-support-cof",
            "cy": "cefnogaeth-leol-cof",
        },
        "tree_path": f"{APPLICATION_BASE_PATH_COF_R4_W2}.3.3",
    },
    {
        "section_name": {
            "en": "3.4 Community benefits",
            "cy": "3.4 Buddion cymunedol",
        },
        "form_name_json": {
            "en": "community-benefits-cof",
            "cy": "buddion-cymunedol-cof",
        },
        "tree_path": f"{APPLICATION_BASE_PATH_COF_R4_W2}.3.4",
    },
    {
        "section_name": {
            "en": "3.5 Environmental sustainability",
            "cy": "3.5 Cynaliadwyedd amgylcheddol",
        },
        "form_name_json": {
            "en": "environmental-sustainability-cof",
            "cy": "cynaliadwyedd-amgylcheddol-cof",
        },
        "tree_path": f"{APPLICATION_BASE_PATH_COF_R4_W2}.3.5",
    },
    {
        "section_name": {"en": "4. Management case", "cy": "4. Achos rheoli"},
        "tree_path": f"{APPLICATION_BASE_PATH_COF_R4_W2}.4",
        "weighting": 47,
        "requires_feedback": True,
    },
    {
        "section_name": {
            "en": "4.1 Funding required",
            "cy": "4.1 Cyllid sydd ei angen",
        },
        "form_name_json": {
            "en": "funding-required-cof",
            "cy": "cyllid-sydd-ei-angen-cof",
        },
        "tree_path": f"{APPLICATION_BASE_PATH_COF_R4_W2}.4.1",
    },
    {
        "section_name": {"en": "4.2 Feasibility", "cy": "4.2 Dichonoldeb"},
        "form_name_json": {
            "en": "feasibility-cof",
            "cy": "dichonoldeb-cof",
        },
        "tree_path": f"{APPLICATION_BASE_PATH_COF_R4_W2}.4.2",
    },
    {
        "section_name": {"en": "4.3 Risk", "cy": "4.3 Risg"},
        "form_name_json": {"en": "risk-cof", "cy": "risg-cof"},
        "tree_path": f"{APPLICATION_BASE_PATH_COF_R4_W2}.4.3",
    },
    {
        "section_name": {"en": "4.4 Operational costs", "cy": "4.4 Costau gweithredol"},
        "form_name_json": {
            "en": "operational-costs-cof",
            "cy": "costau-gweithredol-cof",
        },
        "tree_path": f"{APPLICATION_BASE_PATH_COF_R4_W2}.4.4",
    },
    {
        "section_name": {
            "en": "4.5 Skills and resources",
            "cy": "4.5 Sgiliau ac adnoddau",
        },
        "form_name_json": {
            "en": "skills-and-resources-cof",
            "cy": "sgiliau-ac-adnoddau-cof",
        },
        "tree_path": f"{APPLICATION_BASE_PATH_COF_R4_W2}.4.5",
    },
    {
        "section_name": {
            "en": "4.6 Community representation",
            "cy": "4.6 Cynrychiolaeth gymunedol",
        },
        "form_name_json": {
            "en": "community-representation-cof",
            "cy": "cynrychiolaeth-gymunedol-cof",
        },
        "tree_path": f"{APPLICATION_BASE_PATH_COF_R4_W2}.4.6",
    },
    {
        "section_name": {
            "en": "4.7 Inclusiveness and integration",
            "cy": "4.7 Cynhwysiant ac integreiddio",
        },
        "form_name_json": {
            "en": "inclusiveness-and-integration-cof",
            "cy": "cynhwysiant-ac-integreiddio-cof",
        },
        "tree_path": f"{APPLICATION_BASE_PATH_COF_R4_W2}.4.7",
    },
    {
        "section_name": {
            "en": "4.8 Upload business plan",
            "cy": "4.8 Lanlwythwch y cynllun busnes",
        },
        "form_name_json": {
            "en": "upload-business-plan-cof",
            "cy": "lanlwythwch-y-cynllun-busnes-cof",
        },
        "tree_path": f"{APPLICATION_BASE_PATH_COF_R4_W2}.4.8",
    },
    {
        "section_name": {"en": "5. Check declarations", "cy": "5. Gwirio datganiadau"},
        "tree_path": f"{APPLICATION_BASE_PATH_COF_R4_W2}.5",
    },
    {
        "section_name": {"en": "5.1 Declarations", "cy": "5.1 Datganiadau"},
        "form_name_json": {
            "en": "declarations-cof",
            "cy": "cadarnhadau-terfynol-cof",
        },
        "tree_path": f"{APPLICATION_BASE_PATH_COF_R4_W2}.5.1",
    },
]

round_config_w1 = [
    {
        "id": COF_ROUND_4_WINDOW_1_ID,
        "fund_id": COF_FUND_ID,
        "title_json": {"en": "Round 4 Window 1", "cy": "Rownd 4 Cyfnod Ymgeisio 1"},
        "short_name": "R4W1",
        "opens": COF_R4W1_OPENS_DATE,
        "assessment_start": None,
        "deadline": COF_R4W1_DEADLINE_DATE,
        "application_reminder_sent": False,
        "reminder_date": COF_R4W1_SEND_REMINDER_DATE,
        "assessment_deadline": COF_R4W1_ASSESSMENT_DEADLINE_DATE,
        "prospectus": "https://www.gov.uk/government/publications/community-ownership-fund-prospectus",
        "privacy_notice": (
            "https://www.gov.uk/government/publications/community-ownership-fund-"
            "privacy-notice/community-ownership-fund-privacy-notice"
        ),
        "reference_contact_page_over_email": True,
        "contact_us_banner_json": {
            "en": textwrap.dedent(
                """
                 <h2 class="govuk-heading-m">Get application support</h2>
                 <p class="govuk-body">
                    <a class="govuk-link" href="https://mycommunity.org.uk/community-ownership-fund">Visit the My Community website</a>
                    for information and guidance on applying to Community Ownership Fund.
                    <a class="govuk-link" href="https://mycommunity.org.uk/community-ownership-fund#enquiry-form">Fill out the enquiry form</a>
                    to request advice from My Community.
                </p>
                <p class="govuk-body">
                    We cannot provide direct support to applicants outside of this service.
                </p>
                <h2 class="govuk-heading-m">Get technical support</h2>
                <p  class="govuk-body">
                    Contact the Department of Levelling Up, Housing and Communities funding team if you need
                    help with accessing or submitting an application form.
                </p>
            """
            ),
            "cy": textwrap.dedent(
                """
                 <h2 class="govuk-heading-m">Cael cymorth â'r cais</h2>
                 <p class="govuk-body">
                    <a class="govuk-link" href="https://mycommunity.org.uk/community-ownership-fund">Ewch i wefan My Community</a>
                    i gael gwybodaeth ac arweiniad ar wneud cais i'r Gronfa Perchnogaeth Gymunedol.
                    <a class="govuk-link" href="https://mycommunity.org.uk/community-ownership-fund#enquiry-form">Llenwch y ffurflen ymholiad</a>
                    i ofyn am gyngor gan My Community.
                </p>
                <p class="govuk-body">
                    Ni allwn ddarparu cymorth uniongyrchol i ymgeiswyr tu hwnt i'r gwasanaeth hwn.
                </p>
                <h2 class="govuk-heading-m">Cael cymorth technegol</h2>
                <p  class="govuk-body">
                    Cysylltwch â thîm cyllid yr Adran Ffyniant Bro, Tai a Chymunedau os oes angen help arnoch i gael at ffurflen gais neu ei chyflwyno.
                </p>
            """
            ),
        },
        "contact_email": "COF@communities.gov.uk",
        "contact_phone": None,
        "contact_textphone": None,
        "support_times": "9am to 5pm",
        "support_days": "Monday to Friday",
        "instructions_json": {
            "en": (
                "You must have received an invitation to apply. If we did not invite you,"
                " first <a"
                ' href="https://www.gov.uk/guidance/community-ownership-fund-round-4-how-'
                'to-express-your-interest-in-applying">'
                " express your interest in the fund</a>."
            ),
            "cy": (
                "Mae'n rhaid i chi fod wedi derbyn gwahoddiad i ymgeisio. Os na wnaethom eich gwahodd, <a"
                ' href="https://www.gov.uk/guidance/community-ownership-fund-round-4-how-'
                'to-express-your-interest-in-applying">'
                " mynegwch eich diddordeb yn y gronfa yn gyntaf</a>."
            ),
        },
        "feedback_link": (
            "https://forms.office.com/Pages/ResponsePage.aspx?id="
            "EGg0v32c3kOociSi7zmVqFJBHpeOL2tNnpiwpdL2iElURUY1WkhaS0NFMlZVQUhYQ1NaN0E4RjlQMC4u"
        ),
        "project_name_field_id": "apGjFS",
        "application_guidance_json": COF_APPLICATION_GUIDANCE,
        "guidance_url": (
            "https://www.gov.uk/government/publications/community-ownership-fund-round-3-application-form"
            "-assessment-criteria-guidance"
        ),
        "all_uploaded_documents_section_available": True,
        "application_fields_download_available": True,
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

round_config_w2 = [
    {
        "id": COF_ROUND_4_WINDOW_2_ID,
        "fund_id": COF_FUND_ID,
        "title_json": {"en": "Round 4 Window 2", "cy": "Rownd 4 Cyfnod Ymgeisio 2"},
        "short_name": "R4W2",
        "opens": COF_R4W2_HOLD_DATE,
        "assessment_start": COF_R4W2_HOLD_DATE,
        "deadline": COF_R4W2_HOLD_DATE,
        "application_reminder_sent": False,
        "reminder_date": COF_R4W2_HOLD_DATE,
        "assessment_deadline": COF_R4W2_HOLD_DATE,
        "prospectus": "https://www.gov.uk/government/publications/community-ownership-fund-prospectus",
        "privacy_notice": (
            "https://www.gov.uk/government/publications/community-ownership-fund-"
            "privacy-notice/community-ownership-fund-privacy-notice"
        ),
        "reference_contact_page_over_email": True,
        "contact_us_banner_json": {
            "en": textwrap.dedent(
                """
                 <h2 class="govuk-heading-m">Get application support</h2>
                 <p class="govuk-body">
                    <a class="govuk-link" href="https://mycommunity.org.uk/community-ownership-fund">Visit the My Community website</a>
                    for information and guidance on applying to Community Ownership Fund.
                    <a class="govuk-link" href="https://mycommunity.org.uk/community-ownership-fund#enquiry-form">Fill out the enquiry form</a>
                    to request advice from My Community.
                </p>
                <p class="govuk-body">
                    We cannot provide direct support to applicants outside of this service.
                </p>
                <h2 class="govuk-heading-m">Get technical support</h2>
                <p  class="govuk-body">
                    Contact the Department of Levelling Up, Housing and Communities funding team if you need
                    help with accessing or submitting an application form.
                </p>
            """
            ),
            "cy": textwrap.dedent(
                """
                 <h2 class="govuk-heading-m">Cael cymorth â'r cais</h2>
                 <p class="govuk-body">
                    <a class="govuk-link" href="https://mycommunity.org.uk/community-ownership-fund">Ewch i wefan My Community</a>
                    i gael gwybodaeth ac arweiniad ar wneud cais i'r Gronfa Perchnogaeth Gymunedol.
                    <a class="govuk-link" href="https://mycommunity.org.uk/community-ownership-fund#enquiry-form">Llenwch y ffurflen ymholiad</a>
                    i ofyn am gyngor gan My Community.
                </p>
                <p class="govuk-body">
                    Ni allwn ddarparu cymorth uniongyrchol i ymgeiswyr tu hwnt i'r gwasanaeth hwn.
                </p>
                <h2 class="govuk-heading-m">Cael cymorth technegol</h2>
                <p  class="govuk-body">
                    Cysylltwch â thîm cyllid yr Adran Ffyniant Bro, Tai a Chymunedau os oes angen help arnoch i gael at ffurflen gais neu ei chyflwyno.
                </p>
            """
            ),
        },
        "contact_email": "COF@communities.gov.uk",
        "contact_phone": None,
        "contact_textphone": None,
        "support_times": "9am to 5pm",
        "support_days": "Monday to Friday",
        "instructions_json": {
            "en": (
                "You must have received an invitation to apply. If we did not invite you,"
                " first <a"
                ' href="https://www.gov.uk/guidance/community-ownership-fund-round-4-how-'
                'to-express-your-interest-in-applying">'
                " express your interest in the fund</a>."
            ),
            "cy": (
                "Mae'n rhaid i chi fod wedi derbyn gwahoddiad i ymgeisio. Os na wnaethom eich gwahodd, <a"
                ' href="https://www.gov.uk/guidance/community-ownership-fund-round-4-how-'
                'to-express-your-interest-in-applying">'
                " mynegwch eich diddordeb yn y gronfa yn gyntaf</a>."
            ),
        },
        "feedback_link": (
            "https://forms.office.com/Pages/ResponsePage.aspx?id="
            "EGg0v32c3kOociSi7zmVqFJBHpeOL2tNnpiwpdL2iElURUY1WkhaS0NFMlZVQUhYQ1NaN0E4RjlQMC4u"
        ),
        "project_name_field_id": "apGjFS",
        "application_guidance_json": COF_APPLICATION_GUIDANCE,
        "guidance_url": (
            "https://www.gov.uk/government/publications/community-ownership-fund-round-3-application-form"
            "-assessment-criteria-guidance"
        ),
        "all_uploaded_documents_section_available": True,
        "application_fields_download_available": True,
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
