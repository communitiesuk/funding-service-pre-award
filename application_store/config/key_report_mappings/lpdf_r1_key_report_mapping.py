from application_store.config.key_report_mappings.model import (
    FormMappingItem,
    KeyReportMapping,
)

LPDF_R1_KEY_REPORT_MAPPING = KeyReportMapping(
    round_id="f1d514da-0282-4a96-82c4-25c09645d0b0",
    mapping=[
        FormMappingItem(
            form_name="local-plans-local-authority-details",
            key="RoLhhf",
            return_field="organisation_name",
        ),
        FormMappingItem(
            form_name="local-plans-local-authority-details",
            key="BkuACU",
            return_field="applicant_email",
        ),
    ],
)
