from collections import defaultdict

from pre_award.application_store.config.key_report_mappings.cfa_r1_key_report_mapping import CFA_R1_KEY_REPORT_MAPPING
from pre_award.application_store.config.key_report_mappings.cham_apply_key_report_mapping import (
    CHAM_APPLY_KEY_REPORT_MAPPING,
)
from pre_award.application_store.config.key_report_mappings.cham_reg_key_report_mapping import (
    CHAM_REG_KEY_REPORT_MAPPING,
)
from pre_award.application_store.config.key_report_mappings.cof25_eoi_key_report_mapping import (
    COF25_EOI_KEY_REPORT_MAPPING,
)
from pre_award.application_store.config.key_report_mappings.cof_eoi_key_report_mapping import COF_EOI_KEY_REPORT_MAPPING
from pre_award.application_store.config.key_report_mappings.cof_key_report_mapping import COF_KEY_REPORT_MAPPING
from pre_award.application_store.config.key_report_mappings.cof_r2_key_report_mapping import COF_R2_KEY_REPORT_MAPPING
from pre_award.application_store.config.key_report_mappings.cof_r3w2_key_report_mapping import (
    COF_R3W2_KEY_REPORT_MAPPING,
)
from pre_award.application_store.config.key_report_mappings.cyp_r1_key_report_mapping import CYP_R1_KEY_REPORT_MAPPING
from pre_award.application_store.config.key_report_mappings.dpif_r2_key_report_mapping import DPIF_R2_KEY_REPORT_MAPPING
from pre_award.application_store.config.key_report_mappings.dpif_r4_key_report_mapping import DPIF_R4_KEY_REPORT_MAPPING
from pre_award.application_store.config.key_report_mappings.ehcf_apply_key_report_mapping import (
    EHCF_APPLY_KEY_REPORT_MAPPING,
)
from pre_award.application_store.config.key_report_mappings.gbrf_r1_key_report_mapping import GBRF_R1_KEY_REPORT_MAPPING
from pre_award.application_store.config.key_report_mappings.lahf_lahftu_key_report_mapping import (
    LAHF_LAHFTU_KEY_REPORT_MAPPING,
)
from pre_award.application_store.config.key_report_mappings.lpdf_r1_key_report_mapping import LPDF_R1_KEY_REPORT_MAPPING
from pre_award.application_store.config.key_report_mappings.lpdf_r2_key_report_mapping import LPDF_R2_KEY_REPORT_MAPPING
from pre_award.application_store.config.key_report_mappings.nwp_pill1_key_report_mapping import (
    NWP_PILL1_KEY_REPORT_MAPPING,
)
from pre_award.application_store.config.key_report_mappings.nwp_pill2_key_report_mapping import (
    NWP_PILL2_KEY_REPORT_MAPPING,
)
from pre_award.application_store.config.key_report_mappings.nwp_pill3_key_report_mapping import (
    NWP_PILL3_KEY_REPORT_MAPPING,
)
from pre_award.application_store.config.key_report_mappings.nwp_pill4_key_report_mapping import (
    NWP_PILL4_KEY_REPORT_MAPPING,
)
from pre_award.application_store.config.key_report_mappings.pfn_rp_key_report_mapping import PFN_RP_KEY_REPORT_MAPPING
from pre_award.application_store.config.key_report_mappings.shif_apply_key_report_mapping import (
    SHIF_APPLY_KEY_REPORT_MAPPING,
)

ROUND_ID_TO_KEY_REPORT_MAPPING = defaultdict(
    lambda: COF_R2_KEY_REPORT_MAPPING.mapping,
    {
        CYP_R1_KEY_REPORT_MAPPING.round_id: CYP_R1_KEY_REPORT_MAPPING.mapping,
        DPIF_R2_KEY_REPORT_MAPPING.round_id: DPIF_R2_KEY_REPORT_MAPPING.mapping,
        DPIF_R4_KEY_REPORT_MAPPING.round_id: DPIF_R4_KEY_REPORT_MAPPING.mapping,
        COF_EOI_KEY_REPORT_MAPPING.round_id: COF_EOI_KEY_REPORT_MAPPING.mapping,
        COF25_EOI_KEY_REPORT_MAPPING.round_id: COF25_EOI_KEY_REPORT_MAPPING.mapping,
        COF_R2_KEY_REPORT_MAPPING.round_id: COF_R2_KEY_REPORT_MAPPING.mapping,
        COF_R3W2_KEY_REPORT_MAPPING.round_id: COF_R3W2_KEY_REPORT_MAPPING.mapping,
        GBRF_R1_KEY_REPORT_MAPPING.round_id: GBRF_R1_KEY_REPORT_MAPPING.mapping,
        LPDF_R1_KEY_REPORT_MAPPING.round_id: LPDF_R1_KEY_REPORT_MAPPING.mapping,
        LPDF_R2_KEY_REPORT_MAPPING.round_id: LPDF_R2_KEY_REPORT_MAPPING.mapping,
        CFA_R1_KEY_REPORT_MAPPING.round_id: CFA_R1_KEY_REPORT_MAPPING.mapping,
        CHAM_REG_KEY_REPORT_MAPPING.round_id: CHAM_REG_KEY_REPORT_MAPPING.mapping,
        CHAM_APPLY_KEY_REPORT_MAPPING.round_id: CHAM_APPLY_KEY_REPORT_MAPPING.mapping,
        PFN_RP_KEY_REPORT_MAPPING.round_id: PFN_RP_KEY_REPORT_MAPPING.mapping,
        LAHF_LAHFTU_KEY_REPORT_MAPPING.round_id: LAHF_LAHFTU_KEY_REPORT_MAPPING.mapping,
        SHIF_APPLY_KEY_REPORT_MAPPING.round_id: SHIF_APPLY_KEY_REPORT_MAPPING.mapping,
        NWP_PILL1_KEY_REPORT_MAPPING.round_id: NWP_PILL1_KEY_REPORT_MAPPING.mapping,
        NWP_PILL2_KEY_REPORT_MAPPING.round_id: NWP_PILL2_KEY_REPORT_MAPPING.mapping,
        NWP_PILL3_KEY_REPORT_MAPPING.round_id: NWP_PILL3_KEY_REPORT_MAPPING.mapping,
        NWP_PILL4_KEY_REPORT_MAPPING.round_id: NWP_PILL4_KEY_REPORT_MAPPING.mapping,
        EHCF_APPLY_KEY_REPORT_MAPPING.round_id: EHCF_APPLY_KEY_REPORT_MAPPING.mapping,
        **({key: COF_KEY_REPORT_MAPPING.mapping for key in COF_KEY_REPORT_MAPPING.round_id}),
    },
)


def get_report_mapping_for_round(round_id):
    return ROUND_ID_TO_KEY_REPORT_MAPPING[round_id]
