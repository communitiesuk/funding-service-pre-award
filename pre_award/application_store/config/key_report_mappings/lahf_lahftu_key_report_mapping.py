from pre_award.application_store.config.key_report_mappings.model import (
    FormMappingItem,
    KeyReportMapping,
)

LAHF_LAHFTU_KEY_REPORT_MAPPING = KeyReportMapping(
    round_id="6bb128c7-3ae9-4192-bee4-99b6b5b3b98f",
    mapping=[
        FormMappingItem(
            form_name="lahf-lahftu-local-authority-details",
            key="vDsLGm",
            return_field="organisation_name",
        ),
        FormMappingItem(
            form_name="lahf-lahftu-local-authority-details",
            key="saBdpT",
            return_field="email",
        ),
    ],
)
