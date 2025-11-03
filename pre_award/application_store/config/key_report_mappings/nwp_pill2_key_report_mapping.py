from pre_award.application_store.config.key_report_mappings.model import (
    FormMappingItem,
    KeyReportMapping,
)

NWP_PILL2_KEY_REPORT_MAPPING = KeyReportMapping(
    round_id="8b48609f-8f2f-4646-95b9-735175b90fc5",
    mapping=[
        FormMappingItem(
            form_name="nwp-pill2-organisation-information",
            key="GtoolQ",
            return_field="organisation_name",
        ),
        FormMappingItem(
            form_name="nwp-pill2-applicant-information",
            key="cKnBaI",
            return_field="email",
        ),
    ],
)
