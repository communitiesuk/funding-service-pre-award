from pre_award.application_store.config.key_report_mappings.model import (
    FormMappingItem,
    KeyReportMapping,
)

NWP_PILL4_KEY_REPORT_MAPPING = KeyReportMapping(
    round_id="7f7fb87b-7336-4c2a-b83c-98c7830e835c",
    mapping=[
        FormMappingItem(
            form_name="nwp-pill4-organisation-information",
            key="GtoolQ",
            return_field="organisation_name",
        ),
        FormMappingItem(
            form_name="nwp-pill4-applicant-information",
            key="cKnBaI",
            return_field="email",
        ),
    ],
)
