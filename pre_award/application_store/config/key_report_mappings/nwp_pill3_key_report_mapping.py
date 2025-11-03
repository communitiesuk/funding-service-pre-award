from pre_award.application_store.config.key_report_mappings.model import (
    FormMappingItem,
    KeyReportMapping,
)

NWP_PILL3_KEY_REPORT_MAPPING = KeyReportMapping(
    round_id="1cdc93fb-1133-4cb9-b791-ca277715fe54",
    mapping=[
        FormMappingItem(
            form_name="nwp-pill3-organisation-information",
            key="GtoolQ",
            return_field="organisation_name",
        ),
        FormMappingItem(
            form_name="nwp-pill3-applicant-information",
            key="cKnBaI",
            return_field="email",
        ),
    ],
)
