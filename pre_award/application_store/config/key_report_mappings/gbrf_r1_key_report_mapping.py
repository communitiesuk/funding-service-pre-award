from application_store.config.key_report_mappings.model import (
    FormMappingItem,
    KeyReportMapping,
)

GBRF_R1_KEY_REPORT_MAPPING = KeyReportMapping(
    round_id="e480f03f-e3e0-4bd0-9026-dfed52cc3982",
    mapping=[
        FormMappingItem(
            form_name="local-plans-local-authority-details-signed-off",
            key="RoLhhf",
            return_field="organisation_name",
        ),
        FormMappingItem(
            form_name="local-plans-local-authority-details-signed-off",
            key="BkuACU",
            return_field="applicant_email",
        ),
    ],
)
