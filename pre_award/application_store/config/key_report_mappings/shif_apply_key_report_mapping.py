from pre_award.application_store.config.key_report_mappings.model import (
    FormMappingItem,
    KeyReportMapping,
)

SHIF_APPLY_KEY_REPORT_MAPPING = KeyReportMapping(
    round_id="798ec042-1f64-4714-bde9-98bef1cb067c",
    mapping=[
        FormMappingItem(
            form_name="shif-apply-organisation-information",
            key="oEoIjK",
            return_field="organisation_name",
        ),
        FormMappingItem(
            form_name="shif-apply-organisation-information",
            key="YaGHMI",
            return_field="email",
        ),
    ],
)
