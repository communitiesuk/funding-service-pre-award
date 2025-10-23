from pre_award.application_store.config.key_report_mappings.model import (
    FormMappingItem,
    KeyReportMapping,
)

NWP_R1_KEY_REPORT_MAPPING = KeyReportMapping(
    round_id="e87283ae-e514-4a5e-bcaa-b32526fad721",
    mapping=[
        FormMappingItem(
            form_name="nwp-r1-organisation-details",
            key="GtoolQ",
            return_field="organisation_name",
        ),
        FormMappingItem(
            form_name="nwp-r1-organisation-details",
            key="WOWWfM",
            return_field="email",
        ),
    ],
)
