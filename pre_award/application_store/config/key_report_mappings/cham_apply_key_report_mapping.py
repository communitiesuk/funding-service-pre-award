from pre_award.application_store.config.key_report_mappings.model import (
    FormMappingItem,
    KeyReportMapping,
)

CHAM_APPLY_KEY_REPORT_MAPPING = KeyReportMapping(
    round_id="0ea715b0-8736-4621-9914-51410f9ccafb",
    mapping=[
        FormMappingItem(
            form_name="cham-apply-registration-details",
            key="trYDMJ",
            return_field="organisation_name",
        ),
        FormMappingItem(
            form_name="cham-apply-registration-details",
            key="bzFqFj",
            return_field="applicant_email",
        ),
    ],
)
