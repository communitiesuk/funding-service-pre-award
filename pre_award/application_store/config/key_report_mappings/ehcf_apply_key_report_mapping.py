from pre_award.application_store.config.key_report_mappings.model import (
    FormMappingItem,
    KeyReportMapping,
)

EHCF_APPLY_KEY_REPORT_MAPPING = KeyReportMapping(
    round_id="e3a99e8c-e5ef-4d40-844d-38e27bf4042f",
    mapping=[
        FormMappingItem(
            form_name="ehcf-apply-your-organisation",
            key="WwxTJv",
            return_field="organisation_name",
        ),
        FormMappingItem(
            form_name="ehcf-apply-your-organisation",
            key="byicLn",
            return_field="email",
        ),
    ],
)
