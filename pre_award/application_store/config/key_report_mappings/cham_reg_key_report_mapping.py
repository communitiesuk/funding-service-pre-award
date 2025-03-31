from pre_award.application_store.config.key_report_mappings.model import (
    FormMappingItem,
    KeyReportMapping,
)

CHAM_REG_KEY_REPORT_MAPPING = KeyReportMapping(
    round_id="b92044ee-17f0-4ed5-b4bb-d2ac04eaab54",
    mapping=[
        FormMappingItem(
            form_name="cham-reg-organisation-information",
            key="trYDMJ",
            return_field="organisation_name",
        ),
        FormMappingItem(
            form_name="cham-reg-lead-contact-information",
            key="OPgJWR",
            return_field="applicant_email",
        ),
    ],
)
