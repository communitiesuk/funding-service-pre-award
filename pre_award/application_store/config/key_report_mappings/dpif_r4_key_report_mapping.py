from pre_award.application_store.config.key_report_mappings.model import (
    FormMappingItem,
    KeyReportMapping,
)

DPIF_R4_KEY_REPORT_MAPPING = KeyReportMapping(
    round_id="83d49d14-ced1-4610-a3f5-36b432364b43",
    mapping=[
        FormMappingItem(
            form_name="organisation-information-dpi",
            key="IRugBv",
            return_field="applicant_email",
        ),
        FormMappingItem(
            form_name="organisation-information-dpi",
            key="nYJiWy",
            return_field="organisation_name",
        ),
    ],
)
