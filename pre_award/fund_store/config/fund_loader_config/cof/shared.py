from fund_store.config.fund_loader_config.logo import DLUHC_LOGO_PNG
from fund_store.db.models.fund import FundingType

fund_config = {
    "id": "47aef2f5-3fcb-4d45-acb5-f0152b5f03c4",
    "name_json": {
        "en": "Community Ownership Fund",
        "cy": "Y Cronfa Perchnogaeth Gymunedol",
    },
    "title_json": {
        "en": "funding to save an asset in your community",
        "cy": "gyllid i achub ased yn eich cymuned",
    },
    "short_name": "COF",
    "funding_type": FundingType.COMPETITIVE,
    "description_json": {
        "en": (
            "The Community Ownership Fund is a £150 million fund over 4 years"
            " to support community groups across England, Wales, Scotland and"
            " Northern Ireland to take ownership of assets which are at risk"
            " of being lost to the community."
        ),
        "cy": (  # TODO: Provide welsh translation
            "The Community Ownership Fund is a £150 million fund over 4 years"
            " to support community groups across England, Wales, Scotland and"
            " Northern Ireland to take ownership of assets which are at risk"
            " of being lost to the community."
        ),
    },
    "welsh_available": True,
    "owner_organisation_name": "Department for Levelling Up, Housing and Communities",
    "owner_organisation_shortname": "DLUHC",
    "owner_organisation_logo_uri": DLUHC_LOGO_PNG,
    "ggis_scheme_reference_number": "",
}

COF_APPLICATION_GUIDANCE = {
    "en": (
        "<h2 class='govuk-heading govuk-heading-s'>What we'll ask you for</h2><p"
        " class='govuk-body'>You can preview the <a href='{all_questions_url}'>full list of"
        " application questions</a>.</p><p class='govuk-body'>We'll also ask you to upload"
        " a business plan to support the answers you've given us in the management case"
        " section.</p>"
    ),
    "cy": (
        "<h2 class='govuk-heading govuk-heading-s'>Beth fyddwn ni'n gofyn i chi amdano</h2><p"
        " class='govuk-body'>Gallwch gael cip ymlaen llaw <a href='{all_questions_url}'>o restr lawn"
        " cwestiynau'r cais</a>.</p><p class='govuk-body'>Byddwn hefyd yn gofyn i chi "
        "lanlwytho cynllun busnes i ategu'r atebion rydych wedi'u rhoi i ni yn"
        " yr adran achos rheoli.</p>"
    ),
}

EOI_APPLICATION_GUIDANCE = {
    "en": (
        "<h2 class='govuk-heading govuk-heading-s'>What we'll ask you for</h2><p"
        " class='govuk-body'>You can preview the <a class='govuk-link' href='{all_questions_url}'>full list of"
        " application questions</a>.</p>"
    ),
    "cy": (
        "<h2 class='govuk-heading govuk-heading-s'>Beth y byddwn yn gofyn i chi amdano</h2><p"
        " class='govuk-body'>Gallwch gael rhagolwg o'r <a class='govuk-link' href='{all_questions_url}'>rhestr lawn o"
        " gwestiynau yn y cais</a>.</p>"
    ),
}
