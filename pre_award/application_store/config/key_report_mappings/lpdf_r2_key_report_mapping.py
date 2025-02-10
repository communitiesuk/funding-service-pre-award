from pre_award.application_store.config.key_report_mappings.model import (
    FormMappingItem,
    KeyReportMapping,
)

LPDF_R2_KEY_REPORT_MAPPING = KeyReportMapping(
    round_id="4b519371-aa10-4d9d-ae28-1ff1739af5d3",
    mapping=[
        FormMappingItem(
            form_name="local-authority-details",
            key="RoLhhf",
            return_field="organisation_name",
        ),
        FormMappingItem(
            form_name="local-authority-details",
            key="BkuACU",
            return_field="applicant_email",
        ),
    ],
)
