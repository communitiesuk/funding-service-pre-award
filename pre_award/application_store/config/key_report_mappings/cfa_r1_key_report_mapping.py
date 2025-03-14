from pre_award.application_store.config.key_report_mappings.model import (
    FormMappingItem,
    KeyReportMapping,
)

CFA_R1_KEY_REPORT_MAPPING = KeyReportMapping(
    round_id="25cca4ba-9dbe-45c7-ae2d-d14cadcd8bc6",
    mapping=[
        FormMappingItem(
            form_name="cfa-r1-about-your-organisation",
            key="Astkjl",
            return_field="organisation_name",
        ),
        FormMappingItem(
            form_name="cfa-r1-about-your-organisation",
            key="nvLzWR",
            return_field="email",
        ),
    ],
)
