from pre_award.application_store.config.key_report_mappings.model import (
    FormMappingItem,
    KeyReportMapping,
)

UF1_R1_KEY_REPORT_MAPPING = KeyReportMapping(
    round_id="a2993c27-eef8-431c-b5ac-c2ce9f2c90fc",  # UF1 R1 round ID
    mapping=[
        FormMappingItem(
            form_name="uf1-organisation-information",
            key="yptqZX",
            return_field="organisation_name",
        ),
        # FormMappingItem(
        #     form_name="uf1-organisation-information",
        #     key="bzFqFj",
        #     return_field="applicant_email",
        # ),
    ],
)
