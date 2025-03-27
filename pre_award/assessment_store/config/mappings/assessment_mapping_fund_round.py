# ruff: noqa: E501

from uuid import uuid4

from pre_award.assessment_store.config.mappings.cfa_mapping_parts.r1_scored_sections import (
    scored_sections as cfa_r1_scored_sections,
)
from pre_award.assessment_store.config.mappings.cfa_mapping_parts.r1_unscored_sections import (
    unscored_sections as cfa_r1_unscored_sections,
)
from pre_award.assessment_store.config.mappings.cof_mapping_parts.cof25_r1_scored_criteria import (
    scored_criteria as cof25_scored_criteria_r1,
)
from pre_award.assessment_store.config.mappings.cof_mapping_parts.cof25_r1_unscored_sections import (
    unscored_sections as cof25_unscored_sections_r1,
)
from pre_award.assessment_store.config.mappings.cof_mapping_parts.eoi25_unscored_sections import (
    unscored_sections as cof25_unscored_sections_eoi,
)
from pre_award.assessment_store.config.mappings.cof_mapping_parts.eoi_unscored_sections import (
    unscored_sections as cof_unscored_sections_eoi,
)
from pre_award.assessment_store.config.mappings.cof_mapping_parts.r2_scored_criteria import (
    scored_criteria as cof_scored_criteria_r2,
)
from pre_award.assessment_store.config.mappings.cof_mapping_parts.r2_unscored_sections import (
    unscored_sections as cof_unscored_sections_r2,
)
from pre_award.assessment_store.config.mappings.cof_mapping_parts.r3_scored_criteria import (
    scored_criteria as cof_scored_criteria_r3,
)
from pre_award.assessment_store.config.mappings.cof_mapping_parts.r3_unscored_sections import (
    unscored_sections as cof_unscored_sections_r3,
)
from pre_award.assessment_store.config.mappings.cof_mapping_parts.r3w2_scored_criteria import (
    scored_criteria as cof_scored_criteria_r3w2,
)
from pre_award.assessment_store.config.mappings.cof_mapping_parts.r3w2_unscored_sections import (
    unscored_sections as cof_unscored_sections_r3w2,
)
from pre_award.assessment_store.config.mappings.cof_mapping_parts.r3w3_scored_criteria import (
    scored_criteria as cof_scored_criteria_r3w3,
)
from pre_award.assessment_store.config.mappings.cof_mapping_parts.r3w3_unscored_sections import (
    unscored_sections as cof_unscored_sections_r3w3,
)
from pre_award.assessment_store.config.mappings.cof_mapping_parts.r4w1_scored_criteria import (
    scored_criteria as cof_scored_criteria_r4w1,
)
from pre_award.assessment_store.config.mappings.cof_mapping_parts.r4w1_unscored_sections import (
    unscored_sections as cof_unscored_sections_r4w1,
)
from pre_award.assessment_store.config.mappings.cof_mapping_parts.r4w2_scored_criteria import (
    scored_criteria as cof_scored_criteria_r4w2,
)
from pre_award.assessment_store.config.mappings.cof_mapping_parts.r4w2_unscored_sections import (
    unscored_sections as cof_unscored_sections_r4w2,
)
from pre_award.assessment_store.config.mappings.ctdf_mapping_parts.r1_scored_sections import (
    scored_sections as ctdf_scored_sections,
)
from pre_award.assessment_store.config.mappings.ctdf_mapping_parts.r1_unscored_sections import (
    unscored_sections as ctdf_unscored_sections,
)
from pre_award.assessment_store.config.mappings.cyp_mapping_parts.r1_scored_criteria import (
    scored_criteria as cyp_scored_criteria_r1,
)
from pre_award.assessment_store.config.mappings.cyp_mapping_parts.r1_unscored_criteria import (
    unscored_sections as cyp_unscored_sections_r1,
)
from pre_award.assessment_store.config.mappings.dpif_mappping_parts.r2_scored_criteria import (
    scored_criteria as dpif_scored_criteria,
)
from pre_award.assessment_store.config.mappings.dpif_mappping_parts.r2_unscored_criteria import (
    unscored_sections as dpif_unscored_sections,
)
from pre_award.assessment_store.config.mappings.dpif_mappping_parts.r3_scored_criteria import (
    scored_criteria as dpif_scored_criteria_r3,
)
from pre_award.assessment_store.config.mappings.dpif_mappping_parts.r3_unscored_criteria import (
    unscored_sections as dpif_unscored_sections_r3,
)
from pre_award.assessment_store.config.mappings.gbrf_mapping_parts.r1_unscored_criteria import (
    unscored_sections as gbrf_unscored_sections,
)
from pre_award.assessment_store.config.mappings.hsra_mapping_parts.rp_scored_criteria import (
    scored_criteria as hsra_scored_criteria_rp,
)
from pre_award.assessment_store.config.mappings.hsra_mapping_parts.rp_unscored_sections import (
    unscored_sections as hsra_unscored_sections_rp,
)
from pre_award.assessment_store.config.mappings.hsra_mapping_parts.vr_scored_criteria import (
    scored_criteria as hsra_scored_criteria_vr,
)
from pre_award.assessment_store.config.mappings.hsra_mapping_parts.vr_unscored_sections import (
    unscored_sections as hsra_unscored_sections_vr,
)
from pre_award.assessment_store.config.mappings.lpdf_mapping_parts.r1_unscored_criteria import (
    unscored_sections as lpdf_unscored_sections,
)
from pre_award.assessment_store.config.mappings.lpdf_mapping_parts.r2_unscored_criteria import (
    unscored_sections as lpdf_unscored_sections_r2,
)
from pre_award.assessment_store.config.mappings.nstf_mapping_parts.r2_scored_criteria import (
    scored_criteria as nstf_scored_criteria,
)
from pre_award.assessment_store.config.mappings.nstf_mapping_parts.r2_unscored_sections import (
    unscored_sections as nstf_unscored_sections,
)
from pre_award.assessment_store.config.mappings.uf1_mapping_parts.scored_sections import (
    scored_sections as uf1_scored_sections,
)

# FUND AND ROUND CONFIGURATION (Extracted from the fund store)
COF_FUND_ID = "47aef2f5-3fcb-4d45-acb5-f0152b5f03c4"
COF_ROUND_2_ID = "c603d114-5364-4474-a0c4-c41cbf4d3bbd"
COF_ROUND_2_W3_ID = "5cf439bf-ef6f-431e-92c5-a1d90a4dd32f"
COF_ROUND_3_W1_ID = "e85ad42f-73f5-4e1b-a1eb-6bc5d7f3d762"
COF_ROUND_3_W2_ID = "6af19a5e-9cae-4f00-9194-cf10d2d7c8a7"
COF_ROUND_3_W3_ID = "4efc3263-aefe-4071-b5f4-0910abec12d2"
COF_ROUND_4_W1_ID = "33726b63-efce-4749-b149-20351346c76e"
COF_ROUND_4_W2_ID = "27ab26c2-e58e-4bfe-917d-64be10d16496"
COF_EOI_FUND_ID = "54c11ec2-0b16-46bb-80d2-f210e47a8791"
COF_EOI_ROUND_ID = "6a47c649-7bac-4583-baed-9c4e7a35c8b3"
COF25_EOI_FUND_ID = "4db6072c-4657-458d-9f57-9ca59638317b"
COF25_EOI_ROUND_ID = "9104d809-0fb0-4144-b514-55e81cc2b6fa"
COF25_FUND_ID = "604450fe-65c0-4a2e-a4ba-30ccf256056b"
COF25_ROUND_ID = "38914fbf-9c31-41be-8547-c24d997aaba2"

NSTF_FUND_ID = "13b95669-ed98-4840-8652-d6b7a19964db"
NSTF_ROUND_2_ID = "fc7aa604-989e-4364-98a7-d1234271435a"

CYP_FUND_ID = "1baa0f68-4e0a-4b02-9dfe-b5646f089e65"
CYP_ROUND_1_ID = "888aae3d-7e2c-4523-b9c1-95952b3d1644"

DPIF_FUND_ID = "f493d512-5eb4-11ee-8c99-0242ac120002"
DPIF_ROUND_2_ID = "0059aad4-5eb5-11ee-8c99-0242ac120002"
DPIF_ROUND_3_ID = "ac835965-e8c9-4356-b486-c0c016dbb634"

HSRA_FUND_ID = "1e4bd8b0-b399-466d-bbd1-572171bbc7bd"
HSRA_ROUND_VR_ID = "ae223686-cbcc-4548-8b52-05898c315a59"
HSRA_ROUND_RP_ID = "bae275aa-86a5-4d3e-bcc7-0a25d040910d"

CTDF_FUND_ID = "3dcfa617-cff8-4c2c-9edd-9568aa367d13"
CTDF_ROUND_1_ID = "7ecd7d64-1854-44ab-a10c-a7af4b8d68e1"

FFW_FUND_ID = "8b5c5dad-21a4-4ed1-970e-02d8a47dc49c"
FFW_ROUND_1_ID = "c27a5693-50f9-47fa-b5c2-c43b14d74af1"

CF1_FUND_ID = "97e145f0-5b9a-4ed1-9e15-3e0d9fd998f0"
CF1_ROUND_1_ID = "0ba5b16a-b317-480d-8263-3468e42c71c4"
CF1_ROUND_EOI_ID = "7e371c9b-f72d-4ce5-9f38-b21b27a15bfd"
UF1_FUND__ID = "94fb16c1-e04e-49bf-bd70-27eb7562a988"
UF1_ROUND_1_ID = "a2993c27-eef8-431c-b5ac-c2ce9f2c90fc"

GBRF_FUND_ID = "f97e3930-ab32-4353-84a6-3053d05382ae"
GBRF_ROUND_1_ID = "e480f03f-e3e0-4bd0-9026-dfed52cc3982"

LPDF_FUND_ID = "b1c13e1e-8fda-41bd-8abb-28e56f9d9322"
LPDF_ROUND_1_ID = "f1d514da-0282-4a96-82c4-25c09645d0b0"
LPDF_ROUND_2_ID = "4b519371-aa10-4d9d-ae28-1ff1739af5d3"

CFA_FUND_ID = "35418582-d784-4715-8445-3b1f34320e3c"
CFA_ROUND_1_ID = "25cca4ba-9dbe-45c7-ae2d-d14cadcd8bc6"

# ASSESSMENT DISPLAY CONFIGURATION

fund_round_to_assessment_mapping = {
    f"{GBRF_FUND_ID}:{GBRF_ROUND_1_ID}": {
        "schema_id": "gbrf_r1_assessment",
        "unscored_sections": gbrf_unscored_sections,
        "scored_criteria": [],
    },
    f"{LPDF_FUND_ID}:{LPDF_ROUND_1_ID}": {
        "schema_id": "lpdf_r1_assessment",
        "unscored_sections": lpdf_unscored_sections,
        "scored_criteria": [],
    },
    f"{LPDF_FUND_ID}:{LPDF_ROUND_2_ID}": {
        "schema_id": "lpdf_r2_assessment",
        "unscored_sections": lpdf_unscored_sections_r2,
        "scored_criteria": [],
    },
    f"{DPIF_FUND_ID}:{DPIF_ROUND_3_ID}": {
        "schema_id": "DPIF_R3_assessment",
        "unscored_sections": dpif_unscored_sections_r3,
        "scored_criteria": dpif_scored_criteria_r3,
    },
    f"{COF_FUND_ID}:{COF_ROUND_2_ID}": {
        "schema_id": "cof_r2w2_assessment",
        "unscored_sections": cof_unscored_sections_r2,
        "scored_criteria": cof_scored_criteria_r2,
    },
    f"{COF_FUND_ID}:{COF_ROUND_2_W3_ID}": {
        "schema_id": "cof_r2w3_assessment",
        "unscored_sections": cof_unscored_sections_r2,
        "scored_criteria": cof_scored_criteria_r2,
    },
    f"{NSTF_FUND_ID}:{NSTF_ROUND_2_ID}": {
        "schema_id": "nstf_r2_assessment",
        "unscored_sections": nstf_unscored_sections,
        "scored_criteria": nstf_scored_criteria,
    },
    f"{COF_FUND_ID}:{COF_ROUND_3_W1_ID}": {
        "schema_id": "cof_r3w1_assessment",
        "unscored_sections": cof_unscored_sections_r3,
        "scored_criteria": cof_scored_criteria_r3,
    },
    f"{COF_FUND_ID}:{COF_ROUND_3_W2_ID}": {
        "schema_id": "cof_r3w2_assessment",
        "unscored_sections": cof_unscored_sections_r3w2,
        "scored_criteria": cof_scored_criteria_r3w2,
    },
    f"{COF_FUND_ID}:{COF_ROUND_3_W3_ID}": {
        "schema_id": "cof_r3w3_assessment",
        "unscored_sections": cof_unscored_sections_r3w3,
        "scored_criteria": cof_scored_criteria_r3w3,
    },
    f"{COF_FUND_ID}:{COF_ROUND_4_W1_ID}": {
        "schema_id": "cof_r4w1_assessment",
        "unscored_sections": cof_unscored_sections_r4w1,
        "scored_criteria": cof_scored_criteria_r4w1,
    },
    f"{COF_FUND_ID}:{COF_ROUND_4_W2_ID}": {
        "schema_id": "cof_r4w2_assessment",
        "unscored_sections": cof_unscored_sections_r4w2,
        "scored_criteria": cof_scored_criteria_r4w2,
    },
    f"{COF25_FUND_ID}:{COF25_ROUND_ID}": {
        "schema_id": "cof25_r1_assessment",
        "unscored_sections": cof25_unscored_sections_r1,
        "scored_criteria": cof25_scored_criteria_r1,
    },
    f"{COF_EOI_FUND_ID}:{COF_EOI_ROUND_ID}": {
        "schema_id": "cof_eoi_assessment",
        "unscored_sections": cof_unscored_sections_eoi,
        "scored_criteria": [],
    },
    f"{COF25_EOI_FUND_ID}:{COF25_EOI_ROUND_ID}": {
        "schema_id": "cof25_eoi_assessment",
        "unscored_sections": cof25_unscored_sections_eoi,
        "scored_criteria": [],
    },
    f"{CYP_FUND_ID}:{CYP_ROUND_1_ID}": {
        "schema_id": "cyp_r1_assessment",
        "unscored_sections": cyp_unscored_sections_r1,
        "scored_criteria": cyp_scored_criteria_r1,
    },
    f"{DPIF_FUND_ID}:{DPIF_ROUND_2_ID}": {
        "schema_id": "dpif_r2_assessment",
        "unscored_sections": dpif_unscored_sections,
        "scored_criteria": dpif_scored_criteria,
    },
    f"{FFW_FUND_ID}:{FFW_ROUND_1_ID}": {
        "schema_id": "ctdf_r1_assessment",
        "unscored_sections": ctdf_unscored_sections,
        "scored_criteria": ctdf_scored_sections,
    },
    f"{CTDF_FUND_ID}:{CTDF_ROUND_1_ID}": {
        "schema_id": "ctdf_r1_assessment",
        "unscored_sections": ctdf_unscored_sections,
        "scored_criteria": ctdf_scored_sections,
    },
    f"{CF1_FUND_ID}:{CF1_ROUND_1_ID}": {
        "schema_id": "ctdf_r1_assessment",
        "unscored_sections": ctdf_unscored_sections,
        "scored_criteria": ctdf_scored_sections,
    },
    f"{CF1_FUND_ID}:{CF1_ROUND_EOI_ID}": {
        "schema_id": "ctdf_r1_assessment",
        "unscored_sections": ctdf_unscored_sections,
        "scored_criteria": ctdf_scored_sections,
    },
    f"{UF1_FUND__ID}:{UF1_ROUND_1_ID}": {
        "schema_id": "uf1_r1_assessment",
        "unscored_sections": [],
        "scored_criteria": uf1_scored_sections,
    },
    f"{HSRA_FUND_ID}:{HSRA_ROUND_VR_ID}": {
        "schema_id": "hsra_vr_assessment",
        "unscored_sections": hsra_unscored_sections_vr,
        "scored_criteria": hsra_scored_criteria_vr,
    },
    f"{HSRA_FUND_ID}:{HSRA_ROUND_RP_ID}": {
        "schema_id": "hsra_rp_assessment",
        "unscored_sections": hsra_unscored_sections_rp,
        "scored_criteria": hsra_scored_criteria_rp,
    },
    f"{CFA_FUND_ID}:{CFA_ROUND_1_ID}": {
        "schema_id": "cfa_r1_assessment",
        "unscored_sections": cfa_r1_unscored_sections,
        "scored_criteria": cfa_r1_scored_sections,
    },
}

# Key information for header fields (within JSON)
# We extract a number of field to display at a higher level
# in the assessment view (assessor dashboard view), these
# bits of information are extracted from the application_json


fund_round_data_key_mappings = {
    "GBRFR1": {
        "location": None,
        "asset_type": None,
        "funding_one": None,
        "funding_two": None,
    },
    "FFWAOR1": {
        "location": None,
        "asset_type": None,
        "funding_one": None,
        "funding_two": None,
    },
    "LPDFR1": {
        "location": None,
        "asset_type": None,
        "funding_one": None,
        "funding_two": None,
    },
    "LPDFR2": {
        "location": None,
        "asset_type": None,
        "funding_one": None,
        "funding_two": None,
    },
    "DPIFR3": {
        "location": None,
        "asset_type": None,
        "funding_one": None,
        "funding_two": None,
    },
    "CTDFCR1": {
        "location": None,
        "asset_type": None,
        "funding_one": None,
        "funding_two": None,
    },
    "CF1R1": {
        "location": None,
        "asset_type": None,
        "funding_one": None,
        "funding_two": None,
    },
    "CF1EOI": {
        "location": None,
        "asset_type": None,
        "funding_one": None,
        "funding_two": None,
    },
    "UF1R1": {
        "location": None,
        "asset_type": None,
        "funding_one": None,
        "funding_two": None,
    },
    "COFR2W2": {
        "location": "yEmHpp",
        "asset_type": "yaQoxU",
        "funding_one": "JzWvhj",
        "funding_two": "jLIgoi",
    },
    "COFR2W3": {
        "location": "yEmHpp",
        "asset_type": "yaQoxU",
        "funding_one": "JzWvhj",
        "funding_two": "jLIgoi",
    },
    "COFR3W1": {
        "location": "EfdliG",
        "asset_type": "oXGwlA",
        "funding_one": "ABROnB",
        "funding_two": "cLDRvN",
    },
    "COFR3W2": {
        "location": "EfdliG",
        "asset_type": "oXGwlA",
        "funding_one": "ABROnB",
        "funding_two": ["tSKhQQ", "UyaAHw"],
        "funding_field_type": "multiInputField",
    },
    "COFR3W3": {
        "location": "EfdliG",
        "asset_type": "oXGwlA",
        "funding_one": "ABROnB",
        "funding_two": ["tSKhQQ", "UyaAHw"],
        "funding_field_type": "multiInputField",
    },
    "COFR4W1": {
        "location": "EfdliG",
        "asset_type": "oXGwlA",
        "funding_one": "ABROnB",
        "funding_two": ["tSKhQQ", "UyaAHw"],
        "funding_field_type": "multiInputField",
    },
    "COFR4W2": {
        "location": "EfdliG",
        "asset_type": "oXGwlA",
        "funding_one": "ABROnB",
        "funding_two": ["tSKhQQ", "UyaAHw"],
        "funding_field_type": "multiInputField",
    },
    "COF25R1": {
        "location": "EfdliG",
        "asset_type": "oXGwlA",
        "funding_one": "ABROnB",
        "funding_two": ["tSKhQQ", "UyaAHw"],
        "funding_field_type": "multiInputField",
    },
    "COFEOI": {
        "location": None,
        "asset_type": None,
        "funding_one": None,
        "funding_two": None,
    },
    "COF25EOI": {
        "location": None,
        "asset_type": None,
        "funding_one": None,
        "funding_two": None,
    },
    "NSTFR2": {
        "location": "mhYQzL",
        "asset_type": None,
        "funding_one": ["mCbbyN", "iZdZrr"],
        "funding_two": ["XsAoTv", "JtBjFp"],
        "funding_field_type": "multiInputField",
    },
    "CYPR1": {
        "location": "rmBPvK",
        "asset_type": None,
        "funding_one": None,
        "funding_two": ["JXKUcj", "OnPeeS"],  # only revenue funding for cyp
    },
    "DPIFR2": {
        "location": None,
        "asset_type": None,
        "funding_one": None,
        "funding_two": None,
    },
    "HSRAVR": {
        "location": None,
        "asset_type": None,
        "funding_one": "MIrLuu",
        "funding_two": None,
    },
    "HSRARP": {
        "location": None,
        "asset_type": None,
        "funding_one": "uJIluf",
        "funding_two": None,
    },
    "CFAR1": {
        "location": None,
        "asset_type": None,
        "funding_one": "GAqCNS",
        "funding_two": None,
    },
}

applicant_info_mapping = {
    NSTF_FUND_ID: {
        "OUTPUT_TRACKER": {
            "form_fields": {
                "opFJRm": {"en": {"title": "Organisation name"}},
                "fUMWcd": {"en": {"title": "Name of lead contact"}},
                "CDEwxp": {"en": {"title": "Lead contact email address"}},
                "nURkuc": {"en": {"title": "Local Authority"}},
                "pVBwci": {"en": {"title": "Revenue for 1 April 2023 to 31 March 2024"}},
                "WDouQc": {"en": {"title": "Revenue for 1 April 2024 to 31 March 2025"}},
                "SGjmSM": {"en": {"title": "Capital for 1 April 2023 to 31 March 2024"}},
                "wTdyhk": {"en": {"title": "Capital for 1 April 2024 to 31 March 2025"}},
                "GRWtfV": {"en": {"title": "Revenue for 1 April 2023 to 31 March 2024"}},
                "zvPzXN": {"en": {"title": "Revenue for 1 April 2024 to 31 March 2025"}},
                "QUCvFy": {"en": {"title": "Capital for 1 April 2023 to 31 March 2024"}},
                "pppiYl": {"en": {"title": "Capital for 1 April 2024 to 31 March 2025"}},
                "AVShTf": {"en": {"title": "Region"}},
            },
            "score_fields": {
                "Application ID",
                "Short ID",
                "Score",
                "Score Subcriteria",
                "Score Date",
                "Score Time",
            },
        },
        "ASSESSOR_EXPORT": {
            "form_fields": {
                "fUMWcd": {"en": {"title": "Name of lead contact"}},
                "CDEwxp": {"en": {"title": "Lead contact email address"}},
                "DvBqCJ": {"en": {"title": "Lead contact telephone number"}},
                "mhYQzL": {
                    "en": {
                        "title": "Organisation address",
                        "field_type": "ukAddressField",
                    }
                },
            }
        },
    },
    COF_FUND_ID: {
        "ASSESSOR_EXPORT": {
            "form_fields": {
                "SnLGJE": {
                    "en": {"title": "Name of lead contact"},
                    "cy": {"title": "Enw'r cyswllt arweiniol"},
                },
                "NlHSBg": {
                    "en": {"title": "Lead contact email address"},
                    "cy": {"title": "Cyfeiriad e-bost y cyswllt arweiniol"},
                },
                "FhBkJQ": {
                    "en": {"title": "Lead contact telephone number"},
                    "cy": {"title": "Rhif ffôn y cyswllt arweiniol"},
                },
                "ZQolYb": {
                    "en": {
                        "title": "Organisation address",
                        "field_type": "ukAddressField",
                    },
                    "cy": {
                        "title": "Cyfeiriad y sefydliad",
                        "field_type": "ukAddressField",
                    },
                },
                "VhkCbM": {
                    "en": {
                        "title": "Correspondence address",
                        "field_type": "ukAddressField",
                    },
                    "cy": {
                        "title": "Cyfeiriad gohebu",
                        "field_type": "ukAddressField",
                    },
                },
                "WWWWxy": {
                    "en": {"title": "Your expression of interest (EOI) application reference"},
                    "cy": {"title": "Cyfeirnod eich ffurflen mynegi diddordeb (EOI)."},
                },
                "YdtlQZ": {
                    "en": {"title": "Organisation name"},
                    "cy": {"title": "Enw'r sefydliad"},
                },
                "lajFtB": {
                    "en": {
                        "title": "Type of organisation",
                        "field_type": "radiosField",
                    },
                    "cy": {
                        "title": "Math o sefydliad",
                        "field_type": "radiosField",
                    },
                },
                "aHIGbK": {
                    "en": {"title": "Charity number"},
                    "cy": {"title": "Rhif elusen"},
                },
                "GlPmCX": {
                    "en": {"title": "Company registration number"},
                    "cy": {"title": "Rhif cofrestru'r cwmni"},
                },
                "oXGwlA": {
                    "en": {
                        "title": "Asset type",
                        "field_type": "radiosField",
                    },
                    "cy": {
                        "title": "Math o ased",
                        "field_type": "radiosField",
                    },
                },
                "aJGyCR": {
                    "en": {"title": "Type of asset (other)"},
                    "cy": {"title": "Math o eiddo (arall)"},
                },
                "EfdliG": {
                    "en": {"title": "Postcode of asset", "field_type": "uk_postcode"},
                    "cy": {"title": "Cod post o ased", "field_type": "uk_postcode"},
                },
                "ABROnB": {
                    "en": {"title": "Capital funding request"},
                    "cy": {"title": "Cais cyllido cyfalaf"},
                },
                "tSKhQQ": {
                    "en": {
                        "title": "Revenue costs (optional)",
                        "field_type": "sum_list",
                        "field_to_sum": "UyaAHw",
                    },
                    "cy": {"title": "Costau refeniw (dewisol)"},
                },
                "apGjFS": {
                    "en": {"title": "Project name"},
                    "cy": {"title": "Enw'r prosiect"},
                },
            }
        },
        "OUTPUT_TRACKER": {},
    },
    COF25_FUND_ID: {
        "ASSESSOR_EXPORT": {
            "form_fields": {
                "SnLGJE": {
                    "en": {"title": "Name of lead contact"},
                    "cy": {"title": "Enw'r cyswllt arweiniol"},
                },
                "NlHSBg": {
                    "en": {"title": "Lead contact email address"},
                    "cy": {"title": "Cyfeiriad e-bost y cyswllt arweiniol"},
                },
                "FhBkJQ": {
                    "en": {"title": "Lead contact telephone number"},
                    "cy": {"title": "Rhif ffôn y cyswllt arweiniol"},
                },
                "ZQolYb": {
                    "en": {
                        "title": "Organisation address",
                        "field_type": "ukAddressField",
                    },
                    "cy": {
                        "title": "Cyfeiriad y sefydliad",
                        "field_type": "ukAddressField",
                    },
                },
                "VhkCbM": {
                    "en": {
                        "title": "Correspondence address",
                        "field_type": "ukAddressField",
                    },
                    "cy": {
                        "title": "Cyfeiriad gohebu",
                        "field_type": "ukAddressField",
                    },
                },
                "WWWWxy": {
                    "en": {"title": "Your expression of interest (EOI) application reference"},
                    "cy": {"title": "Cyfeirnod eich ffurflen mynegi diddordeb (EOI)."},
                },
                "YdtlQZ": {
                    "en": {"title": "Organisation name"},
                    "cy": {"title": "Enw'r sefydliad"},
                },
                "lajFtB": {
                    "en": {
                        "title": "Type of organisation",
                        "field_type": "radiosField",
                    },
                    "cy": {
                        "title": "Math o sefydliad",
                        "field_type": "radiosField",
                    },
                },
                "aHIGbK": {
                    "en": {"title": "Charity number"},
                    "cy": {"title": "Rhif elusen"},
                },
                "GlPmCX": {
                    "en": {"title": "Company registration number"},
                    "cy": {"title": "Rhif cofrestru'r cwmni"},
                },
                "oXGwlA": {
                    "en": {
                        "title": "Asset type",
                        "field_type": "radiosField",
                    },
                    "cy": {
                        "title": "Math o ased",
                        "field_type": "radiosField",
                    },
                },
                "aJGyCR": {
                    "en": {"title": "Type of asset (other)"},
                    "cy": {"title": "Math o eiddo (arall)"},
                },
                "EfdliG": {
                    "en": {"title": "Postcode of asset", "field_type": "uk_postcode"},
                    "cy": {"title": "Cod post o ased", "field_type": "uk_postcode"},
                },
                "ABROnB": {
                    "en": {"title": "Capital funding request"},
                    "cy": {"title": "Cais cyllido cyfalaf"},
                },
                "tSKhQQ": {
                    "en": {
                        "title": "Revenue costs (optional)",
                        "field_type": "sum_list",
                        "field_to_sum": "UyaAHw",
                    },
                    "cy": {"title": "Costau refeniw (dewisol)"},
                },
                "apGjFS": {
                    "en": {"title": "Project name"},
                    "cy": {"title": "Enw'r prosiect"},
                },
            }
        },
        "OUTPUT_TRACKER": {},
    },
    COF_EOI_FUND_ID: {
        "ASSESSOR_EXPORT": {
            "form_fields": {
                "eEaDGz": {
                    "en": {
                        "title": "Does your organisation plan both to receive the funding and run the project?",
                        "field_type": "yesNoField",
                    },
                    "cy": {
                        "title": "A yw eich sefydliad yn bwriadu cael y cyllid a rhedeg y prosiect?",
                        "field_type": "yesNoField",
                    },
                },
                "Ihjjyi": {
                    "en": {"title": "Type of asset", "field_type": "radiosField"},
                    "cy": {
                        "title": "Y math o ased",
                        "field_type": "radiosField",
                    },
                },
                "zurxox": {
                    "en": {
                        "title": "Is the asset based in the UK?",
                        "field_type": "yesNoField",
                    },
                    "cy": {
                        "title": "A yw'r ased yn y DU?",
                        "field_type": "yesNoField",
                    },
                },
                "dnqIdW": {
                    "en": {
                        "title": "Address of the asset",
                        "field_type": "ukAddressField",
                    },
                    "cy": {
                        "title": "Cyfeiriad yr ased",
                        "field_type": "ukAddressField",
                    },
                },
                "lLQmNb": {
                    "en": {
                        "title": "Is the asset at risk?",
                        "field_type": "yesNoField",
                    },
                    "cy": {
                        "title": "A yw'r ased mewn perygl?",
                        "field_type": "yesNoField",
                    },
                },
                "ilMbMH": {
                    "en": {
                        "title": "What is the risk to the asset?",
                        "field_type": "checkboxesField",
                    },
                    "cy": {
                        "title": "Beth yw'r perygl i'r ased?",
                        "field_type": "checkboxesField",
                    },
                },
                "fBhSNc": {
                    "en": {
                        "title": "Has the asset ever been used by or had significance to the community?",
                        "field_type": "yesNoField",
                    },
                    "cy": {
                        "title": "A yw'r ased erioed wedi cael ei ddefnyddio gan y gymuned neu wedi bod yn arwyddocaol iddi?",
                        "field_type": "yesNoField",
                    },
                },
                "cPcZos": {
                    "en": {
                        "title": "Do you already own the asset?",
                        "field_type": "yesNoField",
                    },
                    "cy": {
                        "title": "A ydych eisoes yn berchen ar yr ased?",
                        "field_type": "yesNoField",
                    },
                },
                "jOpXfi": {
                    "en": {
                        "title": "Help with public authority",
                        "field_type": "details",
                    },
                    "cy": {
                        "title": "Help gydag awdurdod cyhoeddus",
                        "field_type": "details",
                    },
                },
                "XuAyrs": {
                    "en": {
                        "title": "Does the asset belong to a public authority?",
                        "field_type": "radiosField",
                    },
                    "cy": {
                        "title": "A yw'r ased yn perthyn i awdurdod cyhoeddus?",
                        "field_type": "radiosField",
                    },
                },
                "oDhZlw": {
                    "en": {
                        "title": "Select the option which best represents the stage you are at in purchasing the asset",
                        "field_type": "radiosField",
                    },
                    "cy": {
                        "title": "Cam prynu'r ased",
                        "field_type": "radiosField",
                    },
                },
                "oXFEkV": {
                    "en": {
                        "title": "I confirm the information I've provided is correct",
                        "field_type": "checkboxesField",
                    },
                    "cy": {
                        "title": "Cadarnhaf fod y wybodaeth rwyf wedi'i darparu yn gywir",
                        "field_type": "checkboxesField",
                    },
                },
                "SMRWjl": {
                    "en": {"title": "Organisation name", "field_type": "textField"},
                    "cy": {
                        "title": "Enwau'r sefydliad",
                        "field_type": "textField",
                    },
                },
                "SxkwhF": {
                    "en": {
                        "title": "Does your organisation have any alternative names?",
                        "field_type": "yesNoField",
                    },
                    "cy": {
                        "title": "A oes gan eich sefydliad unrhyw enwau amgen?",
                        "field_type": "yesNoField",
                    },
                },
                "OpeSdM": {
                    "en": {
                        "title": "Organisation address",
                        "field_type": "ukAddressField",
                    },
                    "cy": {
                        "title": "Cyfeiriad y sefydliad",
                        "field_type": "ukAddressField",
                    },
                },
                "Fepkam": {
                    "en": {
                        "title": "Help with organisation type",
                        "field_type": "details",
                    },
                    "cy": {
                        "title": "Help gyda'r math o sefydliad",
                        "field_type": "details",
                    },
                },
                "uYiLsv": {
                    "en": {
                        "title": "Organisation classification",
                        "field_type": "radiosField",
                    },
                    "cy": {
                        "title": "Dosbarthiad y sefydliad",
                        "field_type": "radiosField",
                    },
                },
                "jGoBGp": {
                    "en": {"title": "Help with insolvency", "field_type": "details"},
                    "cy": {
                        "title": "Help with insolvency",
                        "field_type": "details",
                    },
                },
                "NcQSbU": {
                    "en": {
                        "title": "Is your organisation subject to any insolvency actions?",
                        "field_type": "yesNoField",
                    },
                    "cy": {
                        "title": "A yw eich sefydliad yn destun unrhyw gamau ansolfedd?",
                        "field_type": "yesNoField",
                    },
                },
                "qkNYMP": {
                    "en": {"title": "Alternative name 1", "field_type": "textField"},
                    "cy": {
                        "title": "Enw amgen 1",
                        "field_type": "textField",
                    },
                },
                "mVxvon": {
                    "en": {"title": "Alternative name 2", "field_type": "textField"},
                    "cy": {
                        "title": "Enw amgen 2",
                        "field_type": "textField",
                    },
                },
                "DaIVVm": {
                    "en": {"title": "Alternative name 3", "field_type": "textField"},
                    "cy": {
                        "title": "Enw amgen 3",
                        "field_type": "textField",
                    },
                },
                "aocRmv": {
                    "en": {
                        "title": "What do you plan to use COF's funding for?",
                        "field_type": "checkboxesField",
                    },
                    "cy": {
                        "title": "At ba ddiben ydych chi'n bwriadu defnyddio cyllid o'r Gronfa Perchnogaeth Gymunedol?",
                        "field_type": "checkboxesField",
                    },
                },
                "foQgiy": {
                    "en": {
                        "title": "Will the leasehold have at least 15 years when your organisation submits a full application?",
                        "field_type": "yesNoField",
                    },
                    "cy": {
                        "title": "A fydd gan y lesddaliad o leiaf 15 mlynedd pan fydd eich sefydliad yn cyflwyno cais llawn?",
                        "field_type": "yesNoField",
                    },
                },
                "fZAMFv": {
                    "en": {
                        "title": "How much capital funding are you requesting from COF?",
                        "field_type": "numberField",
                    },
                    "cy": {
                        "title": "Faint o gyllid cyfalaf ydych chi'n gwneud cais amdano o'r Gronfa Perchnogaeth Gymunedol?",
                        "field_type": "numberField",
                    },
                },
                "oblxxv": {
                    "en": {
                        "title": "Do you plan to request any revenue funding?",
                        "field_type": "yesNoField",
                    },
                    "cy": {
                        "title": "A ydych yn bwriadu gwneud cais am unrhyw gyllid refeniw?",
                        "field_type": "yesNoField",
                    },
                },
                "eOWKoO": {
                    "en": {
                        "title": "Do you plan to secure match funding?",
                        "field_type": "yesNoField",
                    },
                    "cy": {
                        "title": "A ydych yn bwriadu sicrhau arian cyfatebol?",
                        "field_type": "yesNoField",
                    },
                },
                "BykoQQ": {
                    "en": {
                        "title": "Where do you plan to source match funding?",
                        "field_type": "checkboxesField",
                    },
                    "cy": {
                        "title": "O ble rydych yn bwriadu cael arian cyfatebol?",
                        "field_type": "checkboxesField",
                    },
                },
                "yZxdeJ": {
                    "en": {
                        "title": "Does your project include an element of housing?",
                        "field_type": "yesNoField",
                    },
                    "cy": {
                        "title": "A yw eich prosiect yn cynnwys elfen dai?",
                        "field_type": "yesNoField",
                    },
                },
                "UORyaF": {
                    "en": {
                        "title": "Will you need planning permission for your project?",
                        "field_type": "radiosField",
                    },
                    "cy": {
                        "title": "A fydd angen caniatâd cynllunio ar gyfer eich prosiect?",
                        "field_type": "radiosField",
                    },
                },
                "jICagT": {
                    "en": {
                        "title": "What stage are you at in securing planning permission?",
                        "field_type": "radiosField",
                    },
                    "cy": {
                        "title": "Pa gam ydych chi wedi'i gyrraedd yn y broses o sicrhau caniatâd cynllunio?",
                        "field_type": "radiosField",
                    },
                },
                "kWRuac": {
                    "en": {
                        "title": "What progress have you made to secure this funding?",
                        "field_type": "radiosField",
                    },
                    "cy": {
                        "title": "Pa gynnydd ydych chi wedi'i wneud i sicrhau'r arian hwn?",
                        "field_type": "radiosField",
                    },
                },
                "iXmKyq": {
                    "en": {
                        "title": "Do you wish to be contacted by the development support provider, if eligible for in-depth support?",
                        "field_type": "yesNoField",
                    },
                    "cy": {
                        "title": "A hoffech i'r darparwr cymorth datblygu gysylltu â chi, os ydych yn gymwys i gael cymorth manwl?",
                        "field_type": "yesNoField",
                    },
                },
                "ObIBSx": {
                    "en": {
                        "title": "What are the main things you feel you need support with to submit a good COF application?",
                        "field_type": "checkboxesField",
                    },
                    "cy": {
                        "title": "Beth yw'r prif bethau y mae angen cymorth arnoch gyda nhw er mwyn cyflwyno cais da i'r Gronfa Perchnogaeth Gymunedol yn eich barn chi?",
                        "field_type": "checkboxesField",
                    },
                },
                "MxzEYq": {
                    "en": {
                        "title": "Describe your project and its aims",
                        "field_type": "freeTextField",
                    },
                    "cy": {
                        "title": "Disgrifiwch eich prosiect a'i nodau",
                        "field_type": "freeTextField",
                    },
                },
                "xWnVof": {
                    "en": {"title": "Name of lead contact", "field_type": "textField"},
                    "cy": {
                        "title": "Enw'r prif unigolyn cyswllt",
                        "field_type": "textField",
                    },
                },
                "NQoGIm": {
                    "en": {
                        "title": "Lead contact email address",
                        "field_type": "emailAddressField",
                    },
                    "cy": {
                        "title": "Cyfeiriad e-bost y prif unigolyn cyswllt",
                        "field_type": "emailAddressField",
                    },
                },
                "srxZmv": {
                    "en": {
                        "title": "Lead contact telephone number",
                        "field_type": "telephoneNumberField",
                    },
                    "cy": {
                        "title": "Rhif ffôn y prif unigolyn cyswllt",
                        "field_type": "telephoneNumberField",
                    },
                },
            }
        },
        "OUTPUT_TRACKER": {},
    },
    COF25_EOI_FUND_ID: {
        "ASSESSOR_EXPORT": {
            "form_fields": {
                "eEaDGz": {
                    "en": {
                        "title": "Does your organisation plan both to receive the funding and run the project?",
                        "field_type": "yesNoField",
                    },
                    "cy": {
                        "title": "A yw eich sefydliad yn bwriadu cael y cyllid a rhedeg y prosiect?",
                        "field_type": "yesNoField",
                    },
                },
                "Ihjjyi": {
                    "en": {"title": "Type of asset", "field_type": "radiosField"},
                    "cy": {
                        "title": "Y math o ased",
                        "field_type": "radiosField",
                    },
                },
                "zurxox": {
                    "en": {
                        "title": "Is the asset based in the UK?",
                        "field_type": "yesNoField",
                    },
                    "cy": {
                        "title": "A yw'r ased yn y DU?",
                        "field_type": "yesNoField",
                    },
                },
                "dnqIdW": {
                    "en": {
                        "title": "Address of the asset",
                        "field_type": "ukAddressField",
                    },
                    "cy": {
                        "title": "Cyfeiriad yr ased",
                        "field_type": "ukAddressField",
                    },
                },
                "lLQmNb": {
                    "en": {
                        "title": "Is the asset at risk?",
                        "field_type": "yesNoField",
                    },
                    "cy": {
                        "title": "A yw'r ased mewn perygl?",
                        "field_type": "yesNoField",
                    },
                },
                "ilMbMH": {
                    "en": {
                        "title": "What is the risk to the asset?",
                        "field_type": "checkboxesField",
                    },
                    "cy": {
                        "title": "Beth yw'r perygl i'r ased?",
                        "field_type": "checkboxesField",
                    },
                },
                "fBhSNc": {
                    "en": {
                        "title": "Has the asset ever been used by or had significance to the community?",
                        "field_type": "yesNoField",
                    },
                    "cy": {
                        "title": "A yw'r ased erioed wedi cael ei ddefnyddio gan y gymuned neu wedi bod yn arwyddocaol iddi?",
                        "field_type": "yesNoField",
                    },
                },
                "cPcZos": {
                    "en": {
                        "title": "Do you already own the asset?",
                        "field_type": "yesNoField",
                    },
                    "cy": {
                        "title": "A ydych eisoes yn berchen ar yr ased?",
                        "field_type": "yesNoField",
                    },
                },
                "jOpXfi": {
                    "en": {
                        "title": "Help with public authority",
                        "field_type": "details",
                    },
                    "cy": {
                        "title": "Help gydag awdurdod cyhoeddus",
                        "field_type": "details",
                    },
                },
                "XuAyrs": {
                    "en": {
                        "title": "Does the asset belong to a public authority?",
                        "field_type": "radiosField",
                    },
                    "cy": {
                        "title": "A yw'r ased yn perthyn i awdurdod cyhoeddus?",
                        "field_type": "radiosField",
                    },
                },
                "oDhZlw": {
                    "en": {
                        "title": "Select the option which best represents the stage you are at in purchasing the asset",
                        "field_type": "radiosField",
                    },
                    "cy": {
                        "title": "Cam prynu'r ased",
                        "field_type": "radiosField",
                    },
                },
                "oXFEkV": {
                    "en": {
                        "title": "I confirm the information I've provided is correct",
                        "field_type": "checkboxesField",
                    },
                    "cy": {
                        "title": "Cadarnhaf fod y wybodaeth rwyf wedi'i darparu yn gywir",
                        "field_type": "checkboxesField",
                    },
                },
                "SMRWjl": {
                    "en": {"title": "Organisation name", "field_type": "textField"},
                    "cy": {
                        "title": "Enwau'r sefydliad",
                        "field_type": "textField",
                    },
                },
                "SxkwhF": {
                    "en": {
                        "title": "Does your organisation have any alternative names?",
                        "field_type": "yesNoField",
                    },
                    "cy": {
                        "title": "A oes gan eich sefydliad unrhyw enwau amgen?",
                        "field_type": "yesNoField",
                    },
                },
                "OpeSdM": {
                    "en": {
                        "title": "Organisation address",
                        "field_type": "ukAddressField",
                    },
                    "cy": {
                        "title": "Cyfeiriad y sefydliad",
                        "field_type": "ukAddressField",
                    },
                },
                "Fepkam": {
                    "en": {
                        "title": "Help with organisation type",
                        "field_type": "details",
                    },
                    "cy": {
                        "title": "Help gyda'r math o sefydliad",
                        "field_type": "details",
                    },
                },
                "uYiLsv": {
                    "en": {
                        "title": "Organisation classification",
                        "field_type": "radiosField",
                    },
                    "cy": {
                        "title": "Dosbarthiad y sefydliad",
                        "field_type": "radiosField",
                    },
                },
                "jGoBGp": {
                    "en": {"title": "Help with insolvency", "field_type": "details"},
                    "cy": {
                        "title": "Help with insolvency",
                        "field_type": "details",
                    },
                },
                "NcQSbU": {
                    "en": {
                        "title": "Is your organisation subject to any insolvency actions?",
                        "field_type": "yesNoField",
                    },
                    "cy": {
                        "title": "A yw eich sefydliad yn destun unrhyw gamau ansolfedd?",
                        "field_type": "yesNoField",
                    },
                },
                "qkNYMP": {
                    "en": {"title": "Alternative name 1", "field_type": "textField"},
                    "cy": {
                        "title": "Enw amgen 1",
                        "field_type": "textField",
                    },
                },
                "mVxvon": {
                    "en": {"title": "Alternative name 2", "field_type": "textField"},
                    "cy": {
                        "title": "Enw amgen 2",
                        "field_type": "textField",
                    },
                },
                "DaIVVm": {
                    "en": {"title": "Alternative name 3", "field_type": "textField"},
                    "cy": {
                        "title": "Enw amgen 3",
                        "field_type": "textField",
                    },
                },
                "aocRmv": {
                    "en": {
                        "title": "What do you plan to use COF's funding for?",
                        "field_type": "checkboxesField",
                    },
                    "cy": {
                        "title": "At ba ddiben ydych chi'n bwriadu defnyddio cyllid o'r Gronfa Perchnogaeth Gymunedol?",
                        "field_type": "checkboxesField",
                    },
                },
                "foQgiy": {
                    "en": {
                        "title": "Will the leasehold have at least 15 years when your organisation submits a full application?",
                        "field_type": "yesNoField",
                    },
                    "cy": {
                        "title": "A fydd gan y lesddaliad o leiaf 15 mlynedd pan fydd eich sefydliad yn cyflwyno cais llawn?",
                        "field_type": "yesNoField",
                    },
                },
                "fZAMFv": {
                    "en": {
                        "title": "How much capital funding are you requesting from COF?",
                        "field_type": "numberField",
                    },
                    "cy": {
                        "title": "Faint o gyllid cyfalaf ydych chi'n gwneud cais amdano o'r Gronfa Perchnogaeth Gymunedol?",
                        "field_type": "numberField",
                    },
                },
                "oblxxv": {
                    "en": {
                        "title": "Do you plan to request any revenue funding?",
                        "field_type": "yesNoField",
                    },
                    "cy": {
                        "title": "A ydych yn bwriadu gwneud cais am unrhyw gyllid refeniw?",
                        "field_type": "yesNoField",
                    },
                },
                "eOWKoO": {
                    "en": {
                        "title": "Do you plan to secure match funding?",
                        "field_type": "yesNoField",
                    },
                    "cy": {
                        "title": "A ydych yn bwriadu sicrhau arian cyfatebol?",
                        "field_type": "yesNoField",
                    },
                },
                "BykoQQ": {
                    "en": {
                        "title": "Where do you plan to source match funding?",
                        "field_type": "checkboxesField",
                    },
                    "cy": {
                        "title": "O ble rydych yn bwriadu cael arian cyfatebol?",
                        "field_type": "checkboxesField",
                    },
                },
                "yZxdeJ": {
                    "en": {
                        "title": "Does your project include an element of housing?",
                        "field_type": "yesNoField",
                    },
                    "cy": {
                        "title": "A yw eich prosiect yn cynnwys elfen dai?",
                        "field_type": "yesNoField",
                    },
                },
                "UORyaF": {
                    "en": {
                        "title": "Will you need planning permission for your project?",
                        "field_type": "radiosField",
                    },
                    "cy": {
                        "title": "A fydd angen caniatâd cynllunio ar gyfer eich prosiect?",
                        "field_type": "radiosField",
                    },
                },
                "jICagT": {
                    "en": {
                        "title": "What stage are you at in securing planning permission?",
                        "field_type": "radiosField",
                    },
                    "cy": {
                        "title": "Pa gam ydych chi wedi'i gyrraedd yn y broses o sicrhau caniatâd cynllunio?",
                        "field_type": "radiosField",
                    },
                },
                "kWRuac": {
                    "en": {
                        "title": "What progress have you made to secure this funding?",
                        "field_type": "radiosField",
                    },
                    "cy": {
                        "title": "Pa gynnydd ydych chi wedi'i wneud i sicrhau'r arian hwn?",
                        "field_type": "radiosField",
                    },
                },
                "iXmKyq": {
                    "en": {
                        "title": "Do you wish to be contacted by the development support provider, if eligible for in-depth support?",
                        "field_type": "yesNoField",
                    },
                    "cy": {
                        "title": "A hoffech i'r darparwr cymorth datblygu gysylltu â chi, os ydych yn gymwys i gael cymorth manwl?",
                        "field_type": "yesNoField",
                    },
                },
                "ObIBSx": {
                    "en": {
                        "title": "What are the main things you feel you need support with to submit a good COF application?",
                        "field_type": "checkboxesField",
                    },
                    "cy": {
                        "title": "Beth yw'r prif bethau y mae angen cymorth arnoch gyda nhw er mwyn cyflwyno cais da i'r Gronfa Perchnogaeth Gymunedol yn eich barn chi?",
                        "field_type": "checkboxesField",
                    },
                },
                "MxzEYq": {
                    "en": {
                        "title": "Describe your project and its aims",
                        "field_type": "freeTextField",
                    },
                    "cy": {
                        "title": "Disgrifiwch eich prosiect a'i nodau",
                        "field_type": "freeTextField",
                    },
                },
                "xWnVof": {
                    "en": {"title": "Name of lead contact", "field_type": "textField"},
                    "cy": {
                        "title": "Enw'r prif unigolyn cyswllt",
                        "field_type": "textField",
                    },
                },
                "NQoGIm": {
                    "en": {
                        "title": "Lead contact email address",
                        "field_type": "emailAddressField",
                    },
                    "cy": {
                        "title": "Cyfeiriad e-bost y prif unigolyn cyswllt",
                        "field_type": "emailAddressField",
                    },
                },
                "srxZmv": {
                    "en": {
                        "title": "Lead contact telephone number",
                        "field_type": "telephoneNumberField",
                    },
                    "cy": {
                        "title": "Rhif ffôn y prif unigolyn cyswllt",
                        "field_type": "telephoneNumberField",
                    },
                },
            }
        },
        "OUTPUT_TRACKER": {},
    },
    CYP_FUND_ID: {
        "ASSESSOR_EXPORT": {
            "form_fields": {
                "JbmcJE": {"en": {"title": "Organisation name"}},
                "rmBPvK": {
                    "en": {
                        "title": "Registered organisation address",
                        "field_type": "ukAddressField",
                    }
                },
                "smBPvK": {
                    "en": {
                        "title": "Alternative organisation address (optional)",
                        "field_type": "ukAddressField",
                    }
                },
                "jeocJE": {"en": {"title": "registered charity number"}},
                "JXKUcj": {"en": {"title": "27 September 2023 to 31 March 2024"}},
                "OnPeeS": {"en": {"title": "1 April 2024 to 31 March 2025"}},
                "vYYoAC": {"en": {"title": "Cohort"}},
                "fHodTO": {"en": {"title": "What is the main focus of your project?"}},
                "MADkNZ": {"en": {"title": "Give a brief summary of your project, including what you hope to achieve"}},
                "tZoOKx": {"en": {"title": "Partner organisation details"}},
            }
        },
        "OUTPUT_TRACKER": {"form_fields": {"fHodTO": {"en": {"title": "What is the main focus of your project?"}}}},
    },
    DPIF_FUND_ID: {
        "ASSESSOR_EXPORT": {
            "form_fields": {
                "nYJiWy": {"en": {"title": "Organisation name"}},
                "uYsivE": {"en": {"title": "Project sponsor name"}},
                "xgrxxv": {"en": {"title": "Project sponsor email"}},
                "cPpwET": {"en": {"title": "Section 151 officer name"}},
                "EMukio": {"en": {"title": "Section 151 officer email"}},
                "AYmilW": {"en": {"title": "Lead contact name"}},
                "IRugBv": {"en": {"title": "Lead contact email"}},
                "JUgCya": {
                    "en": {
                        "title": "You have signed the Local Digital Declaration and agree to follow the 5 core principles"
                    }
                },
                "vbmqwB": {
                    "en": {
                        "title": "Your section 151 officer consents to the funds being carried over and spent in the next financial year (March 2024-25) and beyond if deemed necessary in project budget planning"
                    }
                },
                "EQffUz": {
                    "en": {
                        "title": "You agree to let all outputs from this work be published under open licence with a view to any organisation accessing, using or adopting them freely"
                    }
                },
                "kPYiQE": {"en": {"title": "The information you have provided is accurate"}},
            }
        },
        "OUTPUT_TRACKER": {},
    },
    HSRA_FUND_ID: {
        "ASSESSOR_EXPORT": {
            "form_fields": {
                "qbBtUh": {"en": {"title": "Application name"}},
                "okHmBB": {"en": {"title": "Section 151 officer full name"}},
                "bQOXTi": {"en": {"title": "Section 151 officer email"}},
                "phaosT": {"en": {"title": "Section 151 officer telephone number"}},
                "WLddBt": {"en": {"title": "Local authority name"}},
                "OkKkMd": {"en": {"title": "Lead contact full name"}},
                "Lwkcam": {"en": {"title": "Lead contact job title"}},
                "XfiUqN": {"en": {"title": "Lead contact email address"}},
                "DlZjvr": {"en": {"title": "Lead contact telephone number"}},
                "frDgtU": {"en": {"title": "Town or city for designated area"}},
            },
        },
        "OUTPUT_TRACKER": {},
    },
    GBRF_FUND_ID: {
        "ASSESSOR_EXPORT": {
            "form_fields": {
                "RoLhhf": {"en": {"title": "Local authority name", "field_type": "textField"}},
                "sdrrOT": {"en": {"title": "Lead contact first name", "field_type": "textField"}},
                "itKcJz": {"en": {"title": "Lead contact last name", "field_type": "textField"}},
                "gswBOa": {"en": {"title": "Lead contact job title", "field_type": "textField"}},
                "BkuACU": {"en": {"title": "Lead contact email address", "field_type": "textField"}},
                "hRxtWX": {
                    "en": {
                        "title": "Is this expression of interest being submitted jointly with another local authority?",
                        "field_type": "yesNoField",
                    }
                },
                "MhgGgD": {
                    "en": {
                        "title": "Tell us which local authorities you are submitting this joint expression of interest with",
                        "field_type": "freeTextField",
                    }
                },
                "csFGxz": {
                    "en": {
                        "title": "Do you have agreement from all of the local authorities involved in this joint expression of interest",
                        "field_type": "yesNoField",
                    }
                },
                "OlCBjB": {
                    "en": {
                        "title": "Which local authority will act as the accountable body for the funding and monitoring?",
                        "field_type": "textField",
                    }
                },
                "WIOGzl": {"en": {"title": "Spending proposals", "field_type": "checkboxesField"}},
                "cePdOW": {
                    "en": {
                        "title": "Tell us what other types of activities this funding will be used to support",
                        "field_type": "textField",
                    }
                },
                "ncrZUY": {"en": {"title": "Open Digital Planning", "field_type": "yesNoField"}},
                "FLpMfV": {
                    "en": {
                        "title": "I intend to undertake a Green Belt review to accommodate an increase in our needs",
                        "field_type": "yesNoField",
                    }
                },
                "PdObhd": {
                    "en": {
                        "title": "I agree to collaborate with MHCLG over monitoring and evaluation requirements",
                        "field_type": "yesNoField",
                    }
                },
                "hsWqpW": {
                    "en": {
                        "title": "I confirm that our section 151 officer, or deputy section 151 officer, supports this submission",
                        "field_type": "yesNoField",
                    }
                },
                "YwlIXX": {
                    "en": {
                        "title": "I commit to have proposals in place by March 2025 on how we will spend the funding",
                        "field_type": "yesNoField",
                    }
                },
            },
        },
        "OUTPUT_TRACKER": {},
    },
    LPDF_FUND_ID: {
        "ASSESSOR_EXPORT": {
            "form_fields": {
                "RoLhhf": {"en": {"title": "Local authority name", "field_type": "textField"}},
                "sdrrOT": {"en": {"title": "Lead contact first name", "field_type": "textField"}},
                "itKcJz": {"en": {"title": "Lead contact last name", "field_type": "textField"}},
                "gswBOa": {"en": {"title": "Lead contact job title", "field_type": "textField"}},
                "BkuACU": {"en": {"title": "Lead contact email address", "field_type": "textField"}},
                "hRxtWX": {
                    "en": {
                        "title": "Is this expression of interest being submitted jointly with another local authority?",
                        "field_type": "yesNoField",
                    }
                },
                "MhgGgD": {
                    "en": {
                        "title": "Tell us which local authorities you are submitting this joint expression of interest with",
                        "field_type": "freeTextField",
                    }
                },
                "csFGxz": {
                    "en": {
                        "title": "Do you have agreement from all of the local authorities involved in this joint expression of interest",
                        "field_type": "yesNoField",
                    }
                },
                "OlCBjB": {
                    "en": {
                        "title": "Which local authority will act as the accountable body for the funding and monitoring?",
                        "field_type": "textField",
                    }
                },
                "WIOGzl": {"en": {"title": "Spending proposals", "field_type": "checkboxesField"}},
                "cePdOW": {
                    "en": {
                        "title": "Tell us what other types of activities this funding will be used to support",
                        "field_type": "textField",
                    }
                },
                "ncrZUY": {"en": {"title": "Open Digital Planning", "field_type": "yesNoField"}},
                "PdObhd": {
                    "en": {
                        "title": "I confirm our plan’s draft housing requirement meets less than 80% of our revised local housing need (as published on GOV.UK)",
                        "field_type": "yesNoField",
                    }
                },
                "hsWqpW": {
                    "en": {
                        "title": "I confirm that we will need to revise our draft plan to reflect the revised NPPF and local housing need prior to submitting the document for examination",
                        "field_type": "yesNoField",
                    }
                },
                "PnGUpK": {
                    "en": {
                        "title": "I confirm I anticipate submitting our plan by the deadline set out in the National Planning Policy Framework (by June or December 2026 as appropriate)",
                        "field_type": "yesNoField",
                    }
                },
                "oYfyOJ": {
                    "en": {
                        "title": "I agree to respond to MHCLG’s requests to submit an updated local plan timetable (Local Development Scheme or LDS) to MHCLG within 12 weeks of the publication of the revised National Planning Policy Framework, and to provide regular updates on our progress against milestones",
                        "field_type": "yesNoField",
                    }
                },
                "CTerDe": {
                    "en": {
                        "title": "I agree to collaborate with MHCLG over monitoring and evaluation requirements",
                        "field_type": "yesNoField",
                    }
                },
                "uIGuiD": {
                    "en": {
                        "title": "I confirm our section 151 officer, or deputy section 151 officer, supports this submission",
                        "field_type": "yesNoField",
                    }
                },
                "VtcHob": {
                    "en": {
                        "title": "I commit to have proposals in place by March 2025 on how we will spend the funding",
                        "field_type": "yesNoField",
                    }
                },
            },
        },
        "OUTPUT_TRACKER": {},
    },
    f"{LPDF_FUND_ID}:{LPDF_ROUND_1_ID}": {
        "ASSESSOR_EXPORT": {
            "form_fields": {
                "RoLhhf": {"en": {"title": "Local authority name", "field_type": "textField"}},
                "sdrrOT": {"en": {"title": "Lead contact first name", "field_type": "textField"}},
                "itKcJz": {"en": {"title": "Lead contact last name", "field_type": "textField"}},
                "gswBOa": {"en": {"title": "Lead contact job title", "field_type": "textField"}},
                "BkuACU": {"en": {"title": "Lead contact email address", "field_type": "textField"}},
                "hRxtWX": {
                    "en": {
                        "title": "Is this expression of interest being submitted jointly with another local authority?",
                        "field_type": "yesNoField",
                    }
                },
                "MhgGgD": {
                    "en": {
                        "title": "Tell us which local authorities you are submitting this joint expression of interest with",
                        "field_type": "freeTextField",
                    }
                },
                "csFGxz": {
                    "en": {
                        "title": "Do you have agreement from all of the local authorities involved in this joint expression of interest",
                        "field_type": "yesNoField",
                    }
                },
                "OlCBjB": {
                    "en": {
                        "title": "Which local authority will act as the accountable body for the funding and monitoring?",
                        "field_type": "textField",
                    }
                },
                "WIOGzl": {"en": {"title": "Spending proposals", "field_type": "checkboxesField"}},
                "cePdOW": {
                    "en": {
                        "title": "Tell us what other types of activities this funding will be used to support",
                        "field_type": "textField",
                    }
                },
                "ncrZUY": {"en": {"title": "Open Digital Planning", "field_type": "yesNoField"}},
                "PdObhd": {
                    "en": {
                        "title": "I confirm our plan’s draft housing requirement meets less than 80% of our revised local housing need (as published on GOV.UK)",
                        "field_type": "yesNoField",
                    }
                },
                "hsWqpW": {
                    "en": {
                        "title": "I confirm that we will need to revise our draft plan to reflect the revised NPPF and local housing need prior to submitting the document for examination",
                        "field_type": "yesNoField",
                    }
                },
                "PnGUpK": {
                    "en": {
                        "title": "I confirm I anticipate submitting our plan by the deadline set out in the National Planning Policy Framework (by June or December 2026 as appropriate)",
                        "field_type": "yesNoField",
                    }
                },
                "oYfyOJ": {
                    "en": {
                        "title": "I agree to respond to MHCLG’s requests to submit an updated local plan timetable (Local Development Scheme or LDS) to MHCLG within 12 weeks of the publication of the revised National Planning Policy Framework, and to provide regular updates on our progress against milestones",
                        "field_type": "yesNoField",
                    }
                },
                "CTerDe": {
                    "en": {
                        "title": "I agree to collaborate with MHCLG over monitoring and evaluation requirements",
                        "field_type": "yesNoField",
                    }
                },
                "uIGuiD": {
                    "en": {
                        "title": "I confirm our section 151 officer, or deputy section 151 officer, supports this submission",
                        "field_type": "yesNoField",
                    }
                },
                "VtcHob": {
                    "en": {
                        "title": "I commit to have proposals in place by March 2025 on how we will spend the funding",
                        "field_type": "yesNoField",
                    }
                },
            },
        },
        "OUTPUT_TRACKER": {},
    },
    f"{LPDF_FUND_ID}:{LPDF_ROUND_2_ID}": {
        "ASSESSOR_EXPORT": {
            "form_fields": {
                "RoLhhf": {"en": {"title": "Local authority name", "field_type": "textField"}},
                "sdrrOT": {"en": {"title": "Lead contact name", "field_type": "textField"}},
                "gswBOa": {"en": {"title": "Lead contact job title", "field_type": "textField"}},
                "BkuACU": {"en": {"title": "Lead contact email address", "field_type": "textField"}},
                "hRxtWX": {
                    "en": {
                        "title": "Is this expression of interest being submitted jointly with another local authority?",
                        "field_type": "yesNoField",
                    }
                },
                "MhgGgD": {
                    "en": {
                        "title": "Tell us which local authorities you are submitting this joint expression of interest with",
                        "field_type": "freeTextField",
                    }
                },
                "csFGxz": {
                    "en": {
                        "title": "Do you have agreement from all of the local authorities involved in this joint expression of interest",
                        "field_type": "yesNoField",
                    }
                },
                "OlCBjB": {
                    "en": {
                        "title": "Accountable local authority",
                        "field_type": "textField",
                    }
                },
                "WIOGzl": {
                    "en": {
                        "title": "Which types of activities will this funding be used to support?",
                        "field_type": "checkboxesField",
                    }
                },
                "cePdOW": {
                    "en": {
                        "title": "Tell us what other types of activities this funding will be used to support",
                        "field_type": "textField",
                    }
                },
                "ncrZUY": {
                    "en": {
                        "title": "Would you like to receive more information about the Open Digital Planning community and support to develop digital and data skills in your planning service?",
                        "field_type": "yesNoField",
                    }
                },
                "FLpMfV": {
                    "en": {
                        "title": "I confirm our emerging local plan is currently at Regulation 18 stage (as of 14 February 2025)",
                        "field_type": "checkboxesField",
                    }
                },
                "PnGUpK": {
                    "en": {
                        "title": "I confirm I will submit our plan by the deadline set out in the National Planning Policy Framework (by December 2026)",
                        "field_type": "checkboxesField",
                    }
                },
                "oYfyOJ": {
                    "en": {
                        "title": "I agree to respond to MHCLG\u2019s requests to submit an updated local plan timetable (Local Development Scheme or LDS) to MHCLG by 6 March 2025",
                        "field_type": "checkboxesField",
                    }
                },
                "KMcHcx": {
                    "en": {
                        "title": "I agree to provide regular updates on our progress against milestones",
                        "field_type": "checkboxesField",
                    }
                },
                "VtcHob": {
                    "en": {
                        "title": "I commit to have proposals in place by March 2025 on how we will spend the funding",
                        "field_type": "checkboxesField",
                    }
                },
                "CTerDe": {
                    "en": {
                        "title": "I agree to collaborate with MHCLG over monitoring and evaluation requirements",
                        "field_type": "checkboxesField",
                    }
                },
                "uIGuiD": {
                    "en": {
                        "title": "I confirm our section 151 officer, or deputy section 151 officer, supports this submission",
                        "field_type": "checkboxesField",
                    }
                },
            },
        },
        "OUTPUT_TRACKER": {},
    },
    f"{HSRA_FUND_ID}:{HSRA_ROUND_VR_ID}": {
        "ASSESSOR_EXPORT": {
            "form_fields": {
                "qbBtUh": {
                    "en": {
                        "title": "Application name",
                        "field_type": "textField",
                    }
                },
                "WLddBt": {
                    "en": {
                        "title": "Local authority name",
                        "field_type": "textField",
                    }
                },
                "MIrLuu": {
                    "en": {
                        "title": "How much funding are you applying for?",
                        "field_type": "numberField",
                    }
                },
                "okHmBB": {
                    "en": {
                        "title": "Full name of the Section 151 officer",
                        "field_type": "numberField",
                    }
                },
                "bQOXTi": {
                    "en": {
                        "title": "Email address of the Section 151 officer",
                        "field_type": "emailAddressField",
                    }
                },
                "phaosT": {
                    "en": {
                        "title": "Telephone number of the Section 151 officer",
                        "field_type": "numberField",
                    }
                },
                "OkKkMd": {
                    "en": {
                        "title": "Full name of the lead contact",
                        "field_type": "textField",
                    }
                },
                "Lwkcam": {
                    "en": {
                        "title": "Job title of the lead contact",
                        "field_type": "textField",
                    }
                },
                "XfiUqN": {
                    "en": {
                        "title": "Email address of the lead contact",
                        "field_type": "emailAddressField",
                    }
                },
                "DlZjvr": {
                    "en": {
                        "title": "Telephone number of the lead contact",
                        "field_type": "textField",
                    }
                },
                "frDgtU": {
                    "en": {
                        "title": "Town or city for designated area",
                        "field_type": "textField",
                    }
                },
                "YMqcPf": {
                    "en": {
                        "title": "Tell us more about the designated area",
                        "field_type": "textField",
                    }
                },
                "yvpmIv": {
                    "en": {
                        "title": "When do you expect the vacancy register to be completed?",
                        "field_type": "textField",
                    }
                },
                "KFjxBs": {
                    "en": {
                        "title": "When do you expect the post-payment assurance form to be submitted?",
                        "field_type": "textField",
                    }
                },
            }
        },
        "OUTPUT_TRACKER": {
            "form_fields": {
                "MIrLuu": {
                    "en": {
                        "title": "Requested funding",
                        "field_type": "numberField",
                    }
                },
            }
        },
    },
    f"{HSRA_FUND_ID}:{HSRA_ROUND_RP_ID}": {
        "ASSESSOR_EXPORT": {
            "form_fields": {
                "qbBtUh": {
                    "en": {
                        "title": "Application name",
                        "field_type": "textField",
                    }
                },
                "WLddBt": {
                    "en": {
                        "title": "Local authority name",
                        "field_type": "textField",
                    }
                },
                "uJIluf": {
                    "en": {
                        "title": "How much funding are you applying for?",
                        "field_type": "numberField",
                    }
                },
                "okHmBB": {
                    "en": {
                        "title": "Full name of the Section 151 officer",
                        "field_type": "numberField",
                    }
                },
                "bQOXTi": {
                    "en": {
                        "title": "Email address of the Section 151 officer",
                        "field_type": "emailAddressField",
                    }
                },
                "phaosT": {
                    "en": {
                        "title": "Telephone number of the Section 151 officer",
                        "field_type": "numberField",
                    }
                },
                "OkKkMd": {
                    "en": {
                        "title": "Full name of the lead contact",
                        "field_type": "textField",
                    }
                },
                "Lwkcam": {
                    "en": {
                        "title": "Job title of the lead contact",
                        "field_type": "textField",
                    }
                },
                "XfiUqN": {
                    "en": {
                        "title": "Email address of the lead contact",
                        "field_type": "emailAddressField",
                    }
                },
                "DlZjvr": {
                    "en": {
                        "title": "Telephone number of the lead contact",
                        "field_type": "textField",
                    }
                },
                "dwLpZU": {
                    "en": {
                        "title": "Vacant property address",
                        "field_type": "ukAddressField",
                    }
                },
                "rFpLZQ": {
                    "en": {
                        "title": "Total commercial floorspace of the property",
                        "field_type": "numberField",
                    }
                },
                "frDgtU": {
                    "en": {
                        "title": "Location of the designated area",
                        "field_type": "textField",
                    }
                },
                "TzGISC": {
                    "en": {
                        "title": "Details of the designated area",
                        "field_type": "textField",
                    }
                },
                "kkBYPW": {
                    "en": {
                        "title": "Auction date",
                        "field_type": "textField",
                    }
                },
                "pTZLiJ": {
                    "en": {
                        "title": "When do you expect to submit your claim?",
                        "field_type": "textField",
                    }
                },
                "ihfalZ": {
                    "en": {
                        "title": "When do you expect the tenant to sign the tenancy agreement?",
                        "field_type": "textField",
                    }
                },
                "gLzqSP": {
                    "en": {
                        "title": "When do you expect to finish the refurbishment works?",
                        "field_type": "textField",
                    }
                },
                "HeqfVH": {
                    "en": {
                        "title": "When do you expect the tenant to move in?",
                        "field_type": "textField",
                    }
                },
                "LFwJND": {
                    "en": {
                        "title": "Why are your costs higher than the guided price?",
                        "field_type": "textField",
                    }
                },
            }
        },
        "OUTPUT_TRACKER": {
            "form_fields": {
                "uJIluf": {
                    "en": {
                        "title": "Requested funding",
                        "field_type": "numberField",
                    }
                },
            }
        },
    },
    CFA_FUND_ID: {
        "ASSESSOR_EXPORT": {},
        "OUTPUT_TRACKER": {},
    },
}

# APPLICATION SEEDING CONFIGURATION

fund_round_mapping_config = {
    "FFWAOR1": {
        "fund_id": FFW_FUND_ID,
        "round_id": FFW_ROUND_1_ID,
        "type_of_application": "FFW",
    },
    "GBRFR1": {
        "fund_id": GBRF_FUND_ID,
        "round_id": GBRF_ROUND_1_ID,
        "type_of_application": "GBRF",
    },
    "LPDFR1": {
        "fund_id": LPDF_FUND_ID,
        "round_id": LPDF_ROUND_1_ID,
        "type_of_application": "LPDF",
    },
    "LPDFR2": {
        "fund_id": LPDF_FUND_ID,
        "round_id": LPDF_ROUND_2_ID,
        "type_of_application": "LPDF",
    },
    "DPIFR3": {
        "fund_id": DPIF_FUND_ID,
        "round_id": DPIF_ROUND_3_ID,
        "type_of_application": "DPIF",
    },
    "CTDFCR1": {
        "fund_id": CTDF_FUND_ID,
        "round_id": CTDF_ROUND_1_ID,
        "type_of_application": "CTDF",
    },
    "COFR2W2": {
        "fund_id": COF_FUND_ID,
        "round_id": COF_ROUND_2_ID,
        "type_of_application": "COF",
    },
    "COFR2W3": {
        "fund_id": COF_FUND_ID,
        "round_id": COF_ROUND_2_W3_ID,
        "type_of_application": "COF",
    },
    "COFR3W1": {
        "fund_id": COF_FUND_ID,
        "round_id": COF_ROUND_3_W1_ID,
        "type_of_application": "COF",
    },
    "COFR3W2": {
        "fund_id": COF_FUND_ID,
        "round_id": COF_ROUND_3_W2_ID,
        "type_of_application": "COF",
    },
    "COFR3W3": {
        "fund_id": COF_FUND_ID,
        "round_id": COF_ROUND_3_W3_ID,
        "type_of_application": "COF",
    },
    "COFR4W1": {
        "fund_id": COF_FUND_ID,
        "round_id": COF_ROUND_4_W1_ID,
        "type_of_application": "COF",
    },
    "COFR4W2": {
        "fund_id": COF_FUND_ID,
        "round_id": COF_ROUND_4_W2_ID,
        "type_of_application": "COF",
    },
    "COF25R1": {
        "fund_id": COF25_FUND_ID,
        "round_id": COF25_ROUND_ID,
        "type_of_application": "COF25",
    },
    "COFEOI": {
        "fund_id": COF_EOI_FUND_ID,
        "round_id": COF_EOI_ROUND_ID,
        "type_of_application": "COF-EOI",
    },
    "COF25EOI": {
        "fund_id": COF25_EOI_FUND_ID,
        "round_id": COF25_EOI_ROUND_ID,
        "type_of_application": "COF25-EOI",
    },
    "NSTFR2": {
        "fund_id": NSTF_FUND_ID,
        "round_id": NSTF_ROUND_2_ID,
        "type_of_application": "NSTF",
    },
    "CYPR1": {
        "fund_id": CYP_FUND_ID,
        "round_id": CYP_ROUND_1_ID,
        "type_of_application": "CYP",
    },
    "DPIFR2": {
        "fund_id": DPIF_FUND_ID,
        "round_id": DPIF_ROUND_2_ID,
        "type_of_application": "DPIF",
    },
    "HSRAVR": {
        "fund_id": HSRA_FUND_ID,
        "round_id": HSRA_ROUND_VR_ID,
        "type_of_application": "HSRA",
    },
    "HSRARP": {
        "fund_id": HSRA_FUND_ID,
        "round_id": HSRA_ROUND_RP_ID,
        "type_of_application": "HSRA",
    },
    "CFAR1": {
        "fund_id": CFA_FUND_ID,
        "round_id": CFA_ROUND_1_ID,
        "type_of_application": "CFA",
    },
    "RANDOM_FUND_ROUND": {
        "fund_id": uuid4(),
        "round_id": uuid4(),
        "type_of_application": "RFR",
    },
}

fund_round_mapping_config_with_round_id = {
    v["round_id"]: {
        "fund_id": v["fund_id"],
        "type_of_application": v["type_of_application"],
    }
    for k, v in fund_round_mapping_config.items()
}
