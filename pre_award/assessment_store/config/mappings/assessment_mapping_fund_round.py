# ruff: noqa: E501

from uuid import uuid4

from pre_award.assessment_store.config.mappings.cfa_mapping_parts.r1_scored_sections import (
    scored_sections as cfa_r1_scored_sections,
)
from pre_award.assessment_store.config.mappings.cfa_mapping_parts.r1_unscored_sections import (
    unscored_sections as cfa_r1_unscored_sections,
)
from pre_award.assessment_store.config.mappings.cham_mapping_parts.apply_scored_sections import (
    scored_criteria as cham_apply_scored_criteria,
)
from pre_award.assessment_store.config.mappings.cham_mapping_parts.apply_unscored_sections import (
    unscored_sections as cham_apply_unscored_sections,
)
from pre_award.assessment_store.config.mappings.cham_mapping_parts.reg_unscored_sections import (
    unscored_sections as cham_reg_unscored_sections,
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
    scored_sections as ctdf_scored_sections_r1,
)
from pre_award.assessment_store.config.mappings.ctdf_mapping_parts.r1_unscored_sections import (
    unscored_sections as ctdf_unscored_sections_r1,
)
from pre_award.assessment_store.config.mappings.ctdf_mapping_parts.r2_scored_sections import (
    scored_sections as ctdf_scored_sections_r2,
)
from pre_award.assessment_store.config.mappings.ctdf_mapping_parts.r2_unscored_sections import (
    unscored_sections as ctdf_unscored_sections_r2,
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
from pre_award.assessment_store.config.mappings.dpif_mappping_parts.r4_scored_criteria import (
    scored_criteria as dpif_scored_criteria_r4,
)
from pre_award.assessment_store.config.mappings.dpif_mappping_parts.r4_unscored_criteria import (
    unscored_sections as dpif_unscored_sections_r4,
)
from pre_award.assessment_store.config.mappings.ehcf_mapping_parts.apply_scored_sections import (
    scored_sections as ehcf_apply_scored_sections,
)
from pre_award.assessment_store.config.mappings.ehcf_mapping_parts.apply_unscored_sections import (
    unscored_sections as ehcf_apply_unscored_sections,
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
from pre_award.assessment_store.config.mappings.lahf_mapping_parts.lahftu_scored_criteria import (
    scored_sections as lahf_scored_criteria,
)
from pre_award.assessment_store.config.mappings.lahf_mapping_parts.lahftu_unscored_sections import (
    unscored_sections as lahf_unscored_sections,
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
from pre_award.assessment_store.config.mappings.nwp_mapping_parts.pill1_scored_sections import (
    scored_sections as nwp_pill1_scored_sections,
)
from pre_award.assessment_store.config.mappings.nwp_mapping_parts.pill1_unscored_sections import (
    unscored_sections as nwp_pill1_unscored_sections,
)
from pre_award.assessment_store.config.mappings.nwp_mapping_parts.pill2_scored_sections import (
    scored_sections as nwp_pill2_scored_sections,
)
from pre_award.assessment_store.config.mappings.nwp_mapping_parts.pill2_unscored_sections import (
    unscored_sections as nwp_pill2_unscored_sections,
)
from pre_award.assessment_store.config.mappings.nwp_mapping_parts.pill3_scored_sections import (
    scored_sections as nwp_pill3_scored_sections,
)
from pre_award.assessment_store.config.mappings.nwp_mapping_parts.pill3_unscored_sections import (
    unscored_sections as nwp_pill3_unscored_sections,
)
from pre_award.assessment_store.config.mappings.nwp_mapping_parts.pill4_scored_sections import (
    scored_sections as nwp_pill4_scored_sections,
)
from pre_award.assessment_store.config.mappings.nwp_mapping_parts.pill4_unscored_sections import (
    unscored_sections as nwp_pill4_unscored_sections,
)
from pre_award.assessment_store.config.mappings.pfn_mapping_parts.rp_scored_sections import (
    scored_sections as pfn_scored_sections,
)
from pre_award.assessment_store.config.mappings.pfn_mapping_parts.rp_unscored_sections import (
    unscored_sections as pfn_unscored_sections,
)
from pre_award.assessment_store.config.mappings.shif_mapping_parts.apply_scored_sections import (
    scored_sections as shif_apply_scored_sections,
)
from pre_award.assessment_store.config.mappings.shif_mapping_parts.apply_unscored_sections import (
    unscored_sections as shif_apply_unscored_sections,
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
DPIF_ROUND_4_ID = "83d49d14-ced1-4610-a3f5-36b432364b43"

HSRA_FUND_ID = "1e4bd8b0-b399-466d-bbd1-572171bbc7bd"
HSRA_ROUND_VR_ID = "ae223686-cbcc-4548-8b52-05898c315a59"
HSRA_ROUND_RP_ID = "bae275aa-86a5-4d3e-bcc7-0a25d040910d"

CTDF_FUND_ID = "3dcfa617-cff8-4c2c-9edd-9568aa367d13"
CTDF_ROUND_1_ID = "7ecd7d64-1854-44ab-a10c-a7af4b8d68e1"
CTDF_ROUND_2_ID = "8ecd7d64-1854-44ab-a10c-a7af4b8d68e2"

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

CHAM_FUND_ID = "ce1fae51-fbc9-4c0b-8d9f-79948633fab6"
CHAM_ROUND_REG_ID = "b92044ee-17f0-4ed5-b4bb-d2ac04eaab54"
CHAM_ROUND_APPLY_ID = "0ea715b0-8736-4621-9914-51410f9ccafb"

PFN_FUND_ID = "26e831c1-8ae7-4f62-b230-6f409e2700fa"
PFN_ROUND_RP_ID = "9217792e-d8c2-45c8-8170-eed4a8946184"

LAHF_FUND_ID = "28c2f175-eda1-4ba6-9337-e05150708155"
LAHF_ROUND_LAHFTU_ID = "6bb128c7-3ae9-4192-bee4-99b6b5b3b98f"

SHIF_FUND_ID = "217e185c-3bb9-4bd0-b210-fd8a70e0806f"
SHIF_ROUND_APPLY_ID = "798ec042-1f64-4714-bde9-98bef1cb067c"

NWP_FUND_ID = "44676f65-616d-4819-af7a-a457f693f008"
NWP_ROUND_PILL1_ID = "e87283ae-e514-4a5e-bcaa-b32526fad721"
NWP_ROUND_PILL2_ID = "8b48609f-8f2f-4646-95b9-735175b90fc5"
NWP_ROUND_PILL3_ID = "1cdc93fb-1133-4cb9-b791-ca277715fe54"
NWP_ROUND_PILL4_ID = "7f7fb87b-7336-4c2a-b83c-98c7830e835c"

EHCF_FUND_ID = "01f3a07a-1ea8-46d2-9286-d6bf06f4a831"
EHCF_ROUND_APPLY_ID = "e3a99e8c-e5ef-4d40-844d-38e27bf4042f"

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
    f"{DPIF_FUND_ID}:{DPIF_ROUND_4_ID}": {
        "schema_id": "DPIF_R3_assessment",
        "unscored_sections": dpif_unscored_sections_r4,
        "scored_criteria": dpif_scored_criteria_r4,
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
        "unscored_sections": ctdf_unscored_sections_r1,
        "scored_criteria": ctdf_scored_sections_r1,
    },
    f"{CTDF_FUND_ID}:{CTDF_ROUND_1_ID}": {
        "schema_id": "ctdf_r1_assessment",
        "unscored_sections": ctdf_unscored_sections_r1,
        "scored_criteria": ctdf_scored_sections_r1,
    },
    f"{CTDF_FUND_ID}:{CTDF_ROUND_2_ID}": {
        "schema_id": "ctdf_r2_assessment",
        "unscored_sections": ctdf_unscored_sections_r2,
        "scored_criteria": ctdf_scored_sections_r2,
    },
    f"{CF1_FUND_ID}:{CF1_ROUND_1_ID}": {
        "schema_id": "ctdf_r1_assessment",
        "unscored_sections": ctdf_unscored_sections_r1,
        "scored_criteria": ctdf_scored_sections_r1,
    },
    f"{CF1_FUND_ID}:{CF1_ROUND_EOI_ID}": {
        "schema_id": "ctdf_r1_assessment",
        "unscored_sections": ctdf_unscored_sections_r1,
        "scored_criteria": ctdf_scored_sections_r1,
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
    f"{CHAM_FUND_ID}:{CHAM_ROUND_REG_ID}": {
        "schema_id": "cham_reg_assessment",
        "unscored_sections": cham_reg_unscored_sections,
        "scored_criteria": [],
    },
    f"{CHAM_FUND_ID}:{CHAM_ROUND_APPLY_ID}": {
        "schema_id": "cham_apply_assessment",
        "unscored_sections": cham_apply_unscored_sections,
        "scored_criteria": cham_apply_scored_criteria,
    },
    f"{PFN_FUND_ID}:{PFN_ROUND_RP_ID}": {
        "schema_id": "pfn_rp_assessment",
        "unscored_sections": pfn_unscored_sections,
        "scored_criteria": pfn_scored_sections,
    },
    f"{LAHF_FUND_ID}:{LAHF_ROUND_LAHFTU_ID}": {
        "schema_id": "lahf_lahftu_assessment",
        "unscored_sections": lahf_unscored_sections,
        "scored_criteria": lahf_scored_criteria,
    },
    f"{SHIF_FUND_ID}:{SHIF_ROUND_APPLY_ID}": {
        "schema_id": "shif_apply_assessment",
        "unscored_sections": shif_apply_unscored_sections,
        "scored_criteria": shif_apply_scored_sections,
    },
    f"{NWP_FUND_ID}:{NWP_ROUND_PILL1_ID}": {
        "schema_id": "nwp_pill1_assessment",
        "unscored_sections": nwp_pill1_unscored_sections,
        "scored_criteria": nwp_pill1_scored_sections,
    },
    f"{NWP_FUND_ID}:{NWP_ROUND_PILL2_ID}": {
        "schema_id": "nwp_pill2_assessment",
        "unscored_sections": nwp_pill2_unscored_sections,
        "scored_criteria": nwp_pill2_scored_sections,
    },
    f"{NWP_FUND_ID}:{NWP_ROUND_PILL3_ID}": {
        "schema_id": "nwp_pill3_assessment",
        "unscored_sections": nwp_pill3_unscored_sections,
        "scored_criteria": nwp_pill3_scored_sections,
    },
    f"{NWP_FUND_ID}:{NWP_ROUND_PILL4_ID}": {
        "schema_id": "nwp_pill4_assessment",
        "unscored_sections": nwp_pill4_unscored_sections,
        "scored_criteria": nwp_pill4_scored_sections,
    },
    f"{EHCF_FUND_ID}:{EHCF_ROUND_APPLY_ID}": {
        "schema_id": "ehcf_apply_assessment",
        "unscored_sections": ehcf_apply_unscored_sections,
        "scored_criteria": ehcf_apply_scored_sections,
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
    "DPIFR4": {
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
    "CTDFCR2": {
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
    "CHAMREG": {
        "location": None,
        "asset_type": None,
        "funding_one": None,
        "funding_two": None,
    },
    "CHAMAPPLY": {
        "location": None,
        "asset_type": None,
        "funding_one": None,
        "funding_two": None,
    },
    "PFNRP": {
        "location": None,
        "asset_type": None,
        "funding_one": ["JoEKPs", "MaHzlK", "cSAvLl", "lXHVDo"],
        "funding_two": ["YQGJbm", "VmCcNW", "pCCkfZ", "aaOhAH"],
        "funding_field_type": "multiInputField",
    },
    "LAHFLAHFtu": {
        "location": None,
        "asset_type": None,
        "funding_one": "DdMauS",
        "funding_two": None,
    },
    "SHIFAPPLY": {
        "location": None,
        "asset_type": None,
        "funding_one": "UoneMB",  # used when applying for partial project cost funding
        "funding_two": "OdMILX",  # used when applying for total project cost funding
        # shouldn't be done like this, but SHIF have two different questions for total funding,
        # depending on whether the applicant is applying funding to cover the total cost of
        # the project or only part of the cost
    },
    "NWPPILL1": {
        "location": None,
        "asset_type": None,
        "funding_one": "fZBaXW",
        "funding_two": None,
    },
    "NWPPILL2": {
        "location": None,
        "asset_type": None,
        "funding_one": "BmmObA",
        "funding_two": None,
    },
    "NWPPILL3": {
        "location": None,
        "asset_type": None,
        "funding_one": "tNAMxP",
        "funding_two": None,
    },
    "NWPPILL4": {
        "location": None,
        "asset_type": None,
        "funding_one": "mhpCON",
        "funding_two": None,
    },
    "EHCFAPPLY": {
        "location": None,
        "asset_type": None,
        "funding_one": "ddPcod",
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
    f"{CHAM_FUND_ID}:{CHAM_ROUND_REG_ID}": {
        "ASSESSOR_EXPORT": {
            "form_fields": {
                "PSFujj": {"en": {"title": "Full name", "field_type": "textField"}},
                "MUvyMa": {"en": {"title": "Organisation", "field_type": "textField"}},
                "KrgFXy": {"en": {"title": "Role", "field_type": "textField"}},
                "OPgJWR": {"en": {"title": "Email address", "field_type": "emailAddressField"}},
                "MZMsaO": {"en": {"title": "Telephone number", "field_type": "telephoneNumberField"}},
                "trYDMJ": {"en": {"title": "What is the name of your organisation?", "field_type": "textField"}},
                "rocaEG": {
                    "en": {"title": "Does your organisation have an alternative name?", "field_type": "yesNoField"}
                },
                "LAIyWE": {
                    "en": {"title": "What is the alternative name of your organisation?", "field_type": "textField"}
                },
                "PsvKdR": {"en": {"title": "What is your organisation's address?", "field_type": "ukAddressField"}},
                "wMrxig": {
                    "en": {
                        "title": "Has your organisation been established for 2 years or more?",
                        "field_type": "yesNoField",
                    }
                },
                "OgQBfd": {
                    "en": {"title": "What is the legal status of your organisation?", "field_type": "radiosField"}
                },
                "COnttV": {"en": {"title": "Is the organisation a charity?", "field_type": "yesNoField"}},
                "Lwzeak": {"en": {"title": "Where is the charity registered?", "field_type": "radiosField"}},
                "fMjwht": {"en": {"title": "What is your registered charity number?", "field_type": "textField"}},
                "IcYJJz": {
                    "en": {"title": "Specify the legal status of your organisation.", "field_type": "textField"}
                },
                "EQjFsc": {"en": {"title": "Do you have a company registration number?", "field_type": "yesNoField"}},
                "QCszWL": {"en": {"title": "What is your company registration number?", "field_type": "textField"}},
                "iRkMMO": {
                    "en": {"title": "Is your organisation controlled by another entity?", "field_type": "yesNoField"}
                },
                "bKDWQe": {
                    "en": {
                        "title": "What is the name of the entity that controls your organisation?",
                        "field_type": "textField",
                    }
                },
                "QBlbsv": {
                    "en": {
                        "title": "Are you submitting a joint bid for funding with one or more organisations?",
                        "field_type": "yesNoField",
                    }
                },
                "iJgTSg": {
                    "en": {
                        "title": "Will you create a memorandum of understanding (MoU) between partner organisations?",
                        "field_type": "yesNoField",
                    }
                },
                "mexLSQ": {
                    "en": {
                        "title": "Provide the names and details of the partner organisations involved in the joint bid.",
                        "field_type": "freeTextField",
                    }
                },
                "hPIzIm": {
                    "en": {
                        "title": "I confirm that I have read and agree with the declarations",
                        "field_type": "checkboxesField",
                    }
                },
            }
        },
        "OUTPUT_TRACKER": {},
    },
    f"{CHAM_FUND_ID}:{CHAM_ROUND_APPLY_ID}": {
        "ASSESSOR_EXPORT": {
            "form_fields": {
                "Gaibvs": {"en": {"title": "Registration reference number", "field_type": "textField"}},
                "JgqOiG": {"en": {"title": "Full name", "field_type": "textField"}},
                "fSohIv": {"en": {"title": "Organisation", "field_type": "textField"}},
                "JeGsjj": {"en": {"title": "Role", "field_type": "textField"}},
                "bzFqFj": {"en": {"title": "Email address", "field_type": "emailAddressField"}},
                "oWuVdi": {"en": {"title": "Contact number", "field_type": "telephoneNumberField"}},
                "trYDMJ": {"en": {"title": "What is the name of your organisation?", "field_type": "textField"}},
                "rocaEG": {
                    "en": {"title": "Does your organisation have an alternative name?", "field_type": "textField"}
                },
                "LAIyWE": {
                    "en": {"title": "What is the alternative name of your organisation?", "field_type": "textField"}
                },
                "PsvKdR": {"en": {"title": "What is your organisation's address?", "field_type": "ukAddressField"}},
                "wMrxig": {
                    "en": {
                        "title": "Has your organisation been established for 2 years or more?",
                        "field_type": "yesNoField",
                    }
                },
                "OgQBfd": {
                    "en": {"title": "What is the legal status of your organisation?", "field_type": "radiosField"}
                },
                "COnttV": {"en": {"title": "Is the organisation a charity?", "field_type": "yesNoField"}},
                "Lwzeak": {"en": {"title": "Where is the charity registered?", "field_type": "radiosField"}},
                "fMjwht": {"en": {"title": "What is your registered charity number?", "field_type": "textField"}},
                "EQjFsc": {"en": {"title": "Do you have a company registration number?", "field_type": "yesNoField"}},
                "QCszWL": {"en": {"title": "What is your company registration number?", "field_type": "textField"}},
                "iRkMMO": {
                    "en": {"title": "Is your organisation controlled by another entity?", "field_type": "yesNoField"}
                },
                "bKDWQe": {
                    "en": {
                        "title": "What is the name of the entity that controls your organisation?",
                        "field_type": "textField",
                    }
                },
                "sShZrO": {"en": {"title": "Summary of organisation", "field_type": "textField"}},
                "ghzCjW": {"en": {"title": "Success of project", "field_type": "textField"}},
                "zvxncU": {
                    "en": {"title": "relationship with government and other organisations", "field_type": "textField"}
                },
                "aulnWx": {"en": {"title": "Trust of Muslim communities", "field_type": "textField"}},
                "Jpikbj": {"en": {"title": "Activities proposed", "field_type": "textField"}},
                "vuLooU": {"en": {"title": "Key milestones", "field_type": "textField"}},
                "hFwOXS": {
                    "en": {"title": "Establishing a network of local and national partners", "field_type": "textField"}
                },
                "MdgkZt": {"en": {"title": "Building relationships", "field_type": "textField"}},
                "UTdjiQ": {"en": {"title": "Experience and support for individuals", "field_type": "textField"}},
                "hYrOSx": {"en": {"title": "Performance indicatiors and outcomes", "field_type": "textField"}},
                "fwPHTY": {"en": {"title": "Technical systems for reporting", "field_type": "textField"}},
                "lXdDPK": {"en": {"title": "Data collection from complaints", "field_type": "textField"}},
                "oADTGM": {
                    "en": {
                        "title": "Total excepted costs: Year 1 (2025/2026 financial year)",
                        "field_type": "textField",
                    }
                },
                "OpwBcM": {
                    "en": {
                        "title": "Total excepted costs: Year 2 (2026/2027 financial year)",
                        "field_type": "textField",
                    }
                },
                "wfrkZN": {
                    "en": {
                        "title": "Total excepted costs: Year 3 (2027/2028 financial year)",
                        "field_type": "textField",
                    }
                },
                "EEZGWu": {"en": {"title": "Value for money", "field_type": "textField"}},
                "YlivDw": {"en": {"title": "Protect against fraud and other key risks", "field_type": "textField"}},
                "YxXPoy": {"en": {"title": "Reporting to MHCLG", "field_type": "textField"}},
            }
        },
        "OUTPUT_TRACKER": {},
    },
    f"{DPIF_FUND_ID}:{DPIF_ROUND_4_ID}": {
        "ASSESSOR_EXPORT": {
            "form_fields": {
                "hIhsfx": {"en": {"title": "Organisation name", "field_type": "textField"}},
                "KsUjOe": {"en": {"title": "Lead contact name", "field_type": "textField"}},
                "field_id": {"en": {"title": "Lead contact's job title", "field_type": "textField"}},
                "iKcumx": {"en": {"title": "Lead contact email address", "field_type": "emailAddressField"}},
                "jExOjt": {"en": {"title": "Lead contact telephone number", "field_type": "telephoneNumberField"}},
                "sDPMGY": {"en": {"title": "Project sponsor name", "field_type": "textField"}},
                "DkPLbp": {"en": {"title": "Project sponsor email address", "field_type": "emailAddressField"}},
                "VNbFQP": {"en": {"title": "Project sponsor telephone number", "field_type": "telephoneNumberField"}},
                "jHPPTB": {
                    "en": {
                        "title": "Section 151 officer name",
                        "field_type": "textField",
                    }
                },
                "pqCEMQ": {"en": {"title": "Section 151 officer email address?", "field_type": "emailAddressField"}},
                "cyQcaf": {
                    "en": {"title": "Section 151 officer telephone number", "field_type": "telephoneNumberField"}
                },
                "DCQllx": {
                    "en": {
                        "title": "Which software improvements are you interested in working on in the future?",
                        "field_type": "textField",
                    }
                },
            }
        },
        "OUTPUT_TRACKER": {},
    },
    f"{PFN_FUND_ID}:{PFN_ROUND_RP_ID}": {
        "ASSESSOR_EXPORT": {
            "form_fields": {
                "lREPmq": {
                    "en": {
                        "title": "Tell us your indicative spend forecast for capacity funding throughout the programme.",
                        "field_type": "MultiInputField",
                        "formatted_children": {
                            "kzCRNQ": "Capacity funding (2024-25)",
                            "hWffef": "Capacity funding (2025-26)",
                            "exKKtD": "Capacity funding (2026-27)",
                            "SWBFvn": "Capacity funding (2027-28)",
                            "OdZjMh": "Capacity funding (2028-29)",
                            "DbQDzt": "Capacity funding (2029-30)",
                            "mjXkxo": "Capacity funding (2030-31)",
                            "jhEJRB": "Capacity funding (2031-32)",
                            "nZFwqm": "Capacity funding (2032-33)",
                            "IlUUxg": "Capacity funding (2033-34)",
                            "GCnfMS": "Capacity funding (2034-35)",
                            "rQUbSC": "Capacity funding (2035-36)",
                        },
                    }
                },
                "igStco": {
                    "en": {
                        "title": "Tell us your indicative spend forecast for programme delivery funding (capital) throughout the programme.",
                        "field_type": "MultiInputField",
                        "formatted_children": {
                            "JoEKPs": "Programme delivery funding - capital (2026-27)",
                            "MaHzlK": "Programme delivery funding - capital (2027-28)",
                            "cSAvLl": "Programme delivery funding - capital (2028-29)",
                            "lXHVDo": "Programme delivery funding - capital (2029-30)",
                            "yksYVj": "Programme delivery funding - capital (2030-31)",
                            "foBOGa": "Programme delivery funding - capital (2031-32)",
                            "BmNYxJ": "Programme delivery funding - capital (2032-33)",
                            "UYiAHd": "Programme delivery funding - capital (2033-34)",
                            "LzXJTJ": "Programme delivery funding - capital (2034-35)",
                            "LwEzPI": "Programme delivery funding - capital (2035-36)",
                        },
                    }
                },
                "ZaxlkA": {
                    "en": {
                        "title": "Tell us your indicative spend forecast for programme delivery funding (revenue) throughout the programme.",
                        "field_type": "MultiInputField",
                        "formatted_children": {
                            "YQGJbm": "Programme delivery funding - revenue (2026-27)",
                            "VmCcNW": "Programme delivery funding - revenue (2027-28)",
                            "pCCkfZ": "Programme delivery funding - revenue (2028-29)",
                            "aaOhAH": "Programme delivery funding - revenue (2029-30)",
                            "ehgQSG": "Programme delivery funding - revenue (2030-31)",
                            "mmMPXd": "Programme delivery funding - revenue (2031-32)",
                            "iLMwbk": "Programme delivery funding - revenue (2032-33)",
                            "ThaiNt": "Programme delivery funding - revenue (2033-34)",
                            "ROCfYU": "Programme delivery funding - revenue (2034-35)",
                            "qMNUxP": "Programme delivery funding - revenue (2035-36)",
                        },
                    }
                },
                "MEaRya": {
                    "en": {
                        "title": "Tell us your indicative spend forecast for pre-approved interventions in year 1.",
                        "field_type": "MultiInputField",
                        "formatted_children": {
                            "zsdDQk": "Cohesion (2026-27)",
                            "DBqPzO": "Education and opportunity (2026-27)",
                            "MNzARq": "Health and wellbeing (2026-27)",
                            "IVFTCQ": "Housing (2026-27)",
                            "nqmOwu": "Regeneration, high streets and heritage (2026-27)",
                            "UbTbvU": "Safety and security (2026-27)",
                            "qNiSsO": "Transport (2026-27)",
                            "hNACOp": "Work, productivity and skills (2026-27)",
                        },
                    }
                },
                "Grlvkx": {
                    "en": {
                        "title": "Tell us your indicative spend forecast for pre-approved interventions in year 2.",
                        "field_type": "MultiInputField",
                        "formatted_children": {
                            "wYgMdi": "Cohesion (2027-28)",
                            "YlgCLY": "Education and opportunity (2027-28)",
                            "ESRHVS": "Health and wellbeing (2027-28)",
                            "qUrvtI": "Housing (2027-28)",
                            "VsEWYE": "Regeneration, high streets and heritage (2027-28)",
                            "YIpOAe": "Safety and security (2027-28)",
                            "lSlyHK": "Transport (2027-28)",
                            "TaXzeh": "Work, productivity and skills (2027-28)",
                        },
                    }
                },
                "gEOHHl": {
                    "en": {
                        "title": "Tell us your indicative spend forecast for pre-approved interventions in year 3.",
                        "field_type": "MultiInputField",
                        "formatted_children": {
                            "FwurgE": "Cohesion (2028-29)",
                            "tmOkiG": "Education and opportunity (2028-29)",
                            "sSQLwH": "Health and wellbeing (2028-29)",
                            "uUTyWH": "Housing (2028-29)",
                            "ZsNcbA": "Regeneration, high streets and heritage (2028-29)",
                            "iuTXHe": "Safety and security (2028-29)",
                            "lXTtKN": "Transport (2028-29)",
                            "FfSahl": "Work, productivity and skills (2028-29)",
                        },
                    }
                },
                "yYqyaG": {
                    "en": {
                        "title": "Tell us your indicative spend forecast for pre-approved interventions in year 4.",
                        "field_type": "MultiInputField",
                        "formatted_children": {
                            "ygHERI": "Cohesion (2029-30)",
                            "QoEuWY": "Education and opportunity (2029-30)",
                            "QpOTwg": "Health and wellbeing (2029-30)",
                            "jCEizE": "Housing (2029-30)",
                            "zODcnS": "Regeneration, high streets and heritage (2029-30)",
                            "pAnzYr": "Safety and security (2029-30)",
                            "ZKFXMr": "Transport (2029-30)",
                            "flkyla": "Work, productivity and skills (2029-30)",
                        },
                    }
                },
                "QEywSA": {
                    "en": {
                        "title": "Tell us your indicative spend forecast for any off-menu interventions in the first investment period.",
                        "field_type": "MultiInputField",
                        "formatted_children": {
                            "NCgxYf": "Off-menu interventions (2026-27)",
                            "afjufs": "Off-menu interventions (2027-28)",
                            "EbZeKz": "Off-menu interventions (2028-29)",
                            "MRjEso": "Off-menu interventions (2029-30)",
                        },
                    }
                },
                "aUQnBP": {
                    "en": {
                        "title": "Tell us your indicative spend forecast for management costs in the first investment period.",
                        "field_type": "MultiInputField",
                        "formatted_children": {
                            "QVuIFv": "Management costs (2026-27)",
                            "GHFRTw": "Management costs (2027-28)",
                            "sAelLv": "Management costs (2028-29)",
                            "ZvlDXd": "Management costs (2029-30)",
                        },
                    }
                },
                "aLeDKy": {
                    "en": {
                        "title": "Tell us about any unknown uses of funding in the first investment period (financial years 2026 to 2030).",
                        "field_type": "MultiInputField",
                        "formatted_children": {
                            "wajlvP": "Unknown uses of funding (2026-27)",
                            "bPbTEe": "Unknown uses of funding (2027-28)",
                            "XGBxKK": "Unknown uses of funding (2028-29)",
                            "fqmDlx": "Unknown uses of funding (2029-30)",
                        },
                    }
                },
                # Question 2 - MP Consulted
                "cRASmW": {
                    "en": {
                        "title": "Has the MP for your place been consulted during development of this plan and reviewed it prior to submission?",
                        "field_type": "yesNoField",
                    }
                },
                "nfJFsF": {
                    "en": {
                        "title": "MP Full name",
                        "field_type": "textField",
                    }
                },
                "CCRPQy": {
                    "en": {
                        "title": "MP Constituency",
                        "field_type": "textField",
                    }
                },
                # Question 2 - MCA Consulted
                "IvRZON": {
                    "en": {
                        "title": "Have you consulted with the relevant Mayoral Combined Authority on the content of your Regeneration Plan?",
                        "field_type": "yesNoField",
                    }
                },
                # Question 3.3 - Individual Interventions
                "WFRgIa": {
                    "en": {
                        "title": "Which categories of pre-approved interventions do you plan to fund?",
                        "field_type": "checkboxesField",
                    }
                },
                "xFBFbU": {
                    "en": {
                        "title": "Which interventions relating to 'Cohesion' do you plan to fund in the first investment period?",
                        "field_type": "checkboxesField",
                    }
                },
                "AHJYFi": {
                    "en": {
                        "title": "Which interventions relating to 'Education and opportunity' do you plan to fund in the first investment period?",
                        "field_type": "checkboxesField",
                    }
                },
                "vUIIVo": {
                    "en": {
                        "title": "Which interventions relating to 'Health and wellbeing' do you plan to fund in the first investment period?",
                        "field_type": "checkboxesField",
                    }
                },
                "EqLMxj": {
                    "en": {
                        "title": "Which interventions relating to 'Housing' do you plan to fund in the first investment period?",
                        "field_type": "checkboxesField",
                    }
                },
                "GrBsow": {
                    "en": {
                        "title": "Which interventions relating to 'Regeneration, high streets and heritage' do you plan to fund in the first investment period?",
                        "field_type": "checkboxesField",
                    }
                },
                "NwlpeY": {
                    "en": {
                        "title": "Which interventions relating to 'Safety and security' do you plan to fund in the first investment period?",
                        "field_type": "checkboxesField",
                    }
                },
                "RsMYwj": {
                    "en": {
                        "title": "Which interventions relating to 'Transport' do you plan to fund in the first investment period?",
                        "field_type": "checkboxesField",
                    }
                },
                "RAcQRK": {
                    "en": {
                        "title": "Which interventions relating to 'Work, productivity and skills' do you plan to fund in the first investment period?",
                        "field_type": "checkboxesField",
                    }
                },
                # Question 3.3 - Off Menu Proposals
                "DgNaHl": {
                    "en": {
                        "title": "Does your Neighbourhood Board wish to deliver off-menu interventions?",
                        "field_type": "yesNoField",
                    }
                },
                "cpsPOw": {
                    "en": {
                        "title": "Describe the proposed intervention.",
                        "field_type": "MultiInputField",
                        "formatted_children": {
                            "iSuQcm": "Brief description",
                            "vhDdtP": "Estimated cost",
                            "Urvfex": "Why the proposed intervention cannot be delivered through pre-approved interventions",
                            "hjOHaG": "How the proposed intervention will support delivery of one or more of the strategic objectives",
                            "eyyfUI": "How the proposed intervention will be value for money and the outcomes and outputs that you aim to deliver through the investment",
                            "FiPgJD": "How you have consulted with relevant bodies, where relevant, when developing this proposal",
                        },
                    }
                },
                # Question 4.2 - Projects
                "wmpvjb": {
                    "en": {
                        "title": "Can you provide details of any projects you have identified for funding?",
                        "field_type": "yesNoField",
                    }
                },
                "dEyfRq": {
                    "en": {
                        "title": "Tell us about your project.",
                        "field_type": "MultiInputField",
                        "formatted_children": {
                            "AeuWAj": "Project name",
                            "tXQbHW": "Brief description of project",
                            "ojLAmd": "Primary intervention",
                            "YzhoTC": "Project status",
                            "qaHSDG": "Name of delivery organisation",
                            "GeundE": "Type of organisation",
                            "nYQcxZ": "Amount of funding allocated from the Plan for Neighbourhoods programme",
                            "EhzAeB": "Other sources of project funding",
                            "HbiXPn": "Total project budget",
                        },
                    }
                },
                # Question 5.4 - Areas of Support Interested In
                "NKLAZE": {
                    "en": {
                        "title": "Tell us which areas of support you may be interested in.",
                        "field_type": "checkboxesField",
                    }
                },
                # Question 5.1 - Milestone data
                "ZRERCV": {
                    "en": {
                        "title": "Which milestones are relevant for your place?",
                        "field_type": "checkboxesField",
                    }
                },
                "rrPXVD": {
                    "en": {
                        "title": "Consulting the community - key activities and dates",
                        "field_type": "MultiInputField",
                        "formatted_children": {
                            "wllxCG": "Summary of activities",
                            "WYTlBX": "Estimated start date",
                            "ljJuGk": "Estimated completion date",
                        },
                    }
                },
                "POAlfg": {
                    "en": {
                        "title": "Running a feasibility study - key activities and dates",
                        "field_type": "MultiInputField",
                        "formatted_children": {
                            "itoWXB": "Summary of activities",
                            "guCDSi": "Estimated start date",
                            "gJRNzf": "Estimated completion date",
                        },
                    }
                },
                "PHFgHg": {
                    "en": {
                        "title": "Call for projects and project selection round - key activities and dates",
                        "field_type": "MultiInputField",
                        "formatted_children": {
                            "AqETPA": "Summary of activities",
                            "ZLZXdp": "Estimated start date",
                            "RbGxAS": "Estimated completion date",
                        },
                    }
                },
                "mFpuWM": {
                    "en": {
                        "title": "Commissioning services - key activities and dates",
                        "field_type": "MultiInputField",
                        "formatted_children": {
                            "teTxKx": "Summary of activities",
                            "yzJgwQ": "Estimated start date",
                            "icvTMw": "Estimated completion date",
                        },
                    }
                },
                "wnHKSa": {
                    "en": {
                        "title": "Project procurement - key activities and dates",
                        "field_type": "MultiInputField",
                        "formatted_children": {
                            "fOrPxA": "Summary of activities",
                            "GbzGDA": "Estimated start date",
                            "DCINPC": "Estimated completion date",
                        },
                    }
                },
                "cfiJyU": {
                    "en": {
                        "title": "Additional milestones",
                        "field_type": "MultiInputField",
                        "formatted_children": {
                            "ZWYplj": "Brief description of milestone",
                            "HYGqTl": "Summary of activities",
                            "WBbwfO": "Estimated start date",
                            "HZuYud": "Estimated completion date",
                        },
                    }
                },
            }
        },
        "OUTPUT_TRACKER": {},
    },
    LAHF_FUND_ID: {
        "ASSESSOR_EXPORT": {
            "form_fields": {
                "svIchm": {"en": {"title": "Local authority name", "field_type": "textField"}},
                "vDsLGm": {"en": {"title": "Lead contact full name", "field_type": "textField"}},
                "gNJDlH": {"en": {"title": "Lead contact role", "field_type": "textField"}},
                "saBdpT": {"en": {"title": "Lead contact email address", "field_type": "emailAddressField"}},
                "qnaoFo": {"en": {"title": "Property address", "field_type": "ukAddressField"}},
                "DdMauS": {"en": {"title": "Total funding requested", "field_type": "numberField"}},
                "uvAgKD": {"en": {"title": "Adaptation requirements", "field_type": "textField"}},
            }
        },
        "OUTPUT_TRACKER": {
            "form_fields": {
                "DdMauS": {"en": {"title": "Total funding requested", "field_type": "numberField"}},
            }
        },
    },
    SHIF_FUND_ID: {
        "ASSESSOR_EXPORT": {
            "form_fields": {
                "oEoIjK": {"en": {"title": "Organisation name", "field_type": "textField"}},
                "WdapOj": {"en": {"title": "Lead contact full name", "field_type": "textField"}},
                "SAcHge": {"en": {"title": "Lead contact role", "field_type": "textField"}},
                "YaGHMI": {"en": {"title": "Lead contact email address", "field_type": "emailAddressField"}},
                "HZkwbv": {"en": {"title": "Lead contact contact number", "field_type": "telephoneNumberField"}},
                "wzawYs": {"en": {"title": "Organisation address", "field_type": "ukAddressField"}},
                "fidvDS": {"en": {"title": "Charity number", "field_type": "textField"}},
                "siMJHb": {"en": {"title": "Company registration number", "field_type": "textField"}},
                "RlFFTW": {"en": {"title": "Project name", "field_type": "textField"}},
                "OdMILX": {"en": {"title": "Funding requested (Full funding request)", "field_type": "numberField"}},
                "UoneMB": {"en": {"title": "Funding requested (Partial funding request)", "field_type": "numberField"}},
                "lTFJnY": {
                    "en": {"title": "What challenges are you trying to address?", "field_type": "freeTextField"}
                },
                "FFNuZw": {
                    "en": {
                        "title": "How will the proposal address the challenges specified in your problem statement?",
                        "field_type": "freeTextField",
                    }
                },
                "WJTBzi": {"en": {"title": "How is the proposed project innovative?", "field_type": "freeTextField"}},
                "czkAFo": {
                    "en": {
                        "title": "How does this project have the potential to be scaled up or replicated on a wider scale?",
                        "field_type": "freeTextField",
                    }
                },
                "PHcUVY": {
                    "en": {
                        "title": "Describe the positive impacts your project is expected to have",
                        "field_type": "freeTextField",
                    }
                },
            }
        },
        "OUTPUT_TRACKER": {
            "form_fields": {
                "UoneMB": {"en": {"title": "Total funding requested", "field_type": "numberField"}},
            }
        },
    },
    f"{NWP_FUND_ID}:{NWP_ROUND_PILL1_ID}": {
        "ASSESSOR_EXPORT": {
            "form_fields": {
                "GtoolQ": {"en": {"title": "Organisation name", "field_type": "textField"}},
                "GEyQSq": {"en": {"title": "Primary contact full name", "field_type": "textField"}},
                "Owsgne": {"en": {"title": "Primary contact role", "field_type": "textField"}},
                "WOWWfM": {"en": {"title": "Primary contact email address", "field_type": "emailAddressField"}},
                "oExeYu": {"en": {"title": "Primary contact contact number", "field_type": "telephoneNumberField"}},
                "fZBaXW": {"en": {"title": "Total Pillar 1 funding requested", "field_type": "numberField"}},
            }
        },
        "OUTPUT_TRACKER": {
            "form_fields": {
                "fZBaXW": {"en": {"title": "Total Pillar 1 funding requested", "field_type": "numberField"}},
            }
        },
    },
    f"{NWP_FUND_ID}:{NWP_ROUND_PILL2_ID}": {
        "ASSESSOR_EXPORT": {
            "form_fields": {
                "GtoolQ": {"en": {"title": "Organisation name", "field_type": "textField"}},
                "GEyQSq": {"en": {"title": "Primary contact full name", "field_type": "textField"}},
                "Owsgne": {"en": {"title": "Primary contact role", "field_type": "textField"}},
                "WOWWfM": {"en": {"title": "Primary contact email address", "field_type": "emailAddressField"}},
                "oExeYu": {"en": {"title": "Primary contact contact number", "field_type": "telephoneNumberField"}},
                "BmmObA": {"en": {"title": "Total Pillar 2 funding requested", "field_type": "numberField"}},
            }
        },
        "OUTPUT_TRACKER": {
            "form_fields": {
                "BmmObA": {"en": {"title": "Total Pillar 2 funding requested", "field_type": "numberField"}},
            }
        },
    },
    f"{NWP_FUND_ID}:{NWP_ROUND_PILL3_ID}": {
        "ASSESSOR_EXPORT": {
            "form_fields": {
                "GtoolQ": {"en": {"title": "Organisation name", "field_type": "textField"}},
                "GEyQSq": {"en": {"title": "Primary contact full name", "field_type": "textField"}},
                "Owsgne": {"en": {"title": "Primary contact role", "field_type": "textField"}},
                "WOWWfM": {"en": {"title": "Primary contact email address", "field_type": "emailAddressField"}},
                "oExeYu": {"en": {"title": "Primary contact contact number", "field_type": "telephoneNumberField"}},
                "tNAMxP": {"en": {"title": "Total Pillar 3 funding requested", "field_type": "numberField"}},
            }
        },
        "OUTPUT_TRACKER": {
            "form_fields": {
                "tNAMxP": {"en": {"title": "Total Pillar 3 funding requested", "field_type": "numberField"}},
            }
        },
    },
    f"{NWP_FUND_ID}:{NWP_ROUND_PILL4_ID}": {
        "ASSESSOR_EXPORT": {
            "form_fields": {
                "GtoolQ": {"en": {"title": "Organisation name", "field_type": "textField"}},
                "GEyQSq": {"en": {"title": "Primary contact full name", "field_type": "textField"}},
                "Owsgne": {"en": {"title": "Primary contact role", "field_type": "textField"}},
                "WOWWfM": {"en": {"title": "Primary contact email address", "field_type": "emailAddressField"}},
                "oExeYu": {"en": {"title": "Primary contact contact number", "field_type": "telephoneNumberField"}},
                "mhpCON": {"en": {"title": "Total Pillar 4 funding requested", "field_type": "numberField"}},
            }
        },
        "OUTPUT_TRACKER": {
            "form_fields": {
                "mhpCON": {"en": {"title": "Total Pillar 4 funding requested", "field_type": "numberField"}},
            }
        },
    },
    EHCF_FUND_ID: {
        "ASSESSOR_EXPORT": {
            "form_fields": {
                "WwxTJv": {"en": {"title": "Organisation name", "field_type": "textField"}},
                "iXAfvh": {"en": {"title": "Organisation address", "field_type": "ukAddressField"}},
                "elhXgA": {"en": {"title": "Primary contact full name", "field_type": "textField"}},
                "hduWVY": {"en": {"title": "Primary contact job title", "field_type": "textField"}},
                "sHxRrj": {"en": {"title": "Primary contact email address", "field_type": "emailAddressField"}},
                "sLHzMy": {"en": {"title": "Primary contact phone number", "field_type": "telephoneNumberField"}},
                "ddPcod": {"en": {"title": "Total funding requested", "field_type": "numberField"}},
            }
        },
        "OUTPUT_TRACKER": {
            "form_fields": {
                "ddPcod": {"en": {"title": "Total funding requested", "field_type": "numberField"}},
            }
        },
    },
    CTDF_FUND_ID: {
        "ASSESSOR_EXPORT": {
            "form_fields": {
                "orgName": {"en": {"title": "Organisation Name", "field_type": "textField"}},
                "projectName": {"en": {"title": "Project Name", "field_type": "textField"}},
                "projectDescription": {"en": {"title": "Project Description", "field_type": "freeTextField"}},
                "orgAddress": {"en": {"title": "Organisation Address", "field_type": "ukAddressField"}},
                "fundingRequested": {"en": {"title": "Funding Requested", "field_type": "numberField"}},
            }
        },
        "OUTPUT_TRACKER": {
            "form_fields": {
                "orgName": {"en": {"title": "Organisation Name", "field_type": "textField"}},
                "projectName": {"en": {"title": "Project Name", "field_type": "textField"}},
                "fundingRequested": {"en": {"title": "Funding Requested", "field_type": "numberField"}},
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
    "DPIFR4": {
        "fund_id": DPIF_FUND_ID,
        "round_id": DPIF_ROUND_4_ID,
        "type_of_application": "DPIF",
    },
    "CTDFCR1": {
        "fund_id": CTDF_FUND_ID,
        "round_id": CTDF_ROUND_1_ID,
        "type_of_application": "CTDF",
    },
    "CTDFCR2": {
        "fund_id": CTDF_FUND_ID,
        "round_id": CTDF_ROUND_2_ID,
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
    "CHAMREG": {
        "fund_id": CHAM_FUND_ID,
        "round_id": CHAM_ROUND_REG_ID,
        "type_of_application": "CHAM",
    },
    "CHAMAPPLY": {
        "fund_id": CHAM_FUND_ID,
        "round_id": CHAM_ROUND_APPLY_ID,
        "type_of_application": "CHAM",
    },
    "PFNRP": {
        "fund_id": PFN_FUND_ID,
        "round_id": PFN_ROUND_RP_ID,
        "type_of_application": "PFN",
    },
    "LAHFLAHFtu": {
        "fund_id": LAHF_FUND_ID,
        "round_id": LAHF_ROUND_LAHFTU_ID,
        "type_of_application": "LAHF",
    },
    "SHIFAPPLY": {
        "fund_id": SHIF_FUND_ID,
        "round_id": SHIF_ROUND_APPLY_ID,
        "type_of_application": "SHIF",
    },
    "NWPPILL1": {
        "fund_id": NWP_FUND_ID,
        "round_id": NWP_ROUND_PILL1_ID,
        "type_of_application": "NWP",
    },
    "NWPPILL2": {
        "fund_id": NWP_FUND_ID,
        "round_id": NWP_ROUND_PILL2_ID,
        "type_of_application": "NWP",
    },
    "NWPPILL3": {
        "fund_id": NWP_FUND_ID,
        "round_id": NWP_ROUND_PILL3_ID,
        "type_of_application": "NWP",
    },
    "NWPPILL4": {
        "fund_id": NWP_FUND_ID,
        "round_id": NWP_ROUND_PILL4_ID,
        "type_of_application": "NWP",
    },
    "EHCFAPPLY": {
        "fund_id": EHCF_FUND_ID,
        "round_id": EHCF_ROUND_APPLY_ID,
        "type_of_application": "EHCF",
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
