from collections import namedtuple

ALL_VALUE = "ALL"
ON_VALUE = "ON"
OFF_VALUE = "OFF"

asset_types = {
    ALL_VALUE: "All",
    "community-centre": "Community centre",
    "cinema": "Cinema",
    "gallery": "Gallery",
    "museum": "Museum",
    "music-venue": "Music venue",
    "park": "Park",
    "post-office": "Post office",
    "pub": "Pub",
    "shop": "Shop",
    "sporting": "Sporting leisure facility",
    "theatre": "Theatre",
    "other": "Other",
}

assessment_statuses = {
    ALL_VALUE: "All",
    "NOT_STARTED": "Ready to review",
    "IN_PROGRESS": "Review in progress",
    "COMPLETED": "Assessment complete",
    "QA_COMPLETED": "QA complete",
    "FLAGGED": "Flagged",
    "STOPPED": "Stopped",
    "MULTIPLE_FLAGS": "Multiple flags to resolve",
    "CHANGE_REQUESTED": "Change requested",
    "CHANGE_RECEIVED": "Review changes",
}

funding_types = {
    ALL_VALUE: "All",
    "both-revenue-and-capital": "Capital and revenue",
    "capital": "Capital",
    "revenue": "Revenue",
}

cohort = {
    ALL_VALUE: "All",
    "ukrainian-schemes": "Ukraine",
    "hong-kong-british-nationals": "Hong Kong",
    "afghan-citizens-resettlement-scheme": "Afghanistan",
}

search_params_default = {
    "search_term": "",
    "search_in": "project_name,short_id",
    "asset_type": ALL_VALUE,
    "status": ALL_VALUE,
    "filter_by_tag": ALL_VALUE,
    "assigned_to": ALL_VALUE,
}
search_params_cof = {
    "search_term": "",
    "search_in": "project_name,short_id",
    "asset_type": ALL_VALUE,
    "status": ALL_VALUE,
    "filter_by_tag": ALL_VALUE,
    "country": ALL_VALUE,
    "region": ALL_VALUE,
    "local_authority": ALL_VALUE,
}
search_params_nstf = {
    "search_term": "",
    "search_in": "organisation_name,short_id",
    "funding_type": ALL_VALUE,
    "status": ALL_VALUE,
    "filter_by_tag": ALL_VALUE,
    "country": ALL_VALUE,
    "region": ALL_VALUE,
    "local_authority": ALL_VALUE,
}
search_params_cyp = {
    "search_term": "",
    "search_in": "organisation_name,short_id",
    "cohort": ALL_VALUE,
    "status": ALL_VALUE,
    "filter_by_tag": ALL_VALUE,
    "country": ALL_VALUE,
    "region": ALL_VALUE,
}

search_params_dpif = {
    "search_term": "",
    "search_in": "organisation_name,short_id",
    "status": ALL_VALUE,
    "filter_by_tag": ALL_VALUE,
    "publish_datasets": ALL_VALUE,
    "datasets": ALL_VALUE,
    "team_in_place": ALL_VALUE,
}

# TODO Add HSRA filtering options
search_params_hsra = {
    "search_term": "",
    "search_in": "organisation_name,short_id",
    "status": ALL_VALUE,
    "filter_by_tag": ALL_VALUE,
    "local_authority": ALL_VALUE,
    "joint_application": ALL_VALUE,
}

joint_application_options = {
    ALL_VALUE: "All",
    "true": "Yes",
    "false": "No",
}

dpi_filters = [
    {
        "name": "team_in_place",
        "values": ["ALL", "Yes", "No"],
    },
    {
        "name": "datasets",
        "values": ["ALL", "Yes", "No"],
    },
    {
        "name": "publish_datasets",
        "values": [
            "ALL",
            "None",
            "0-to-3-months",
            "4-to-7-months",
            "8-to-11-months",
            "longer-than-11-months",
        ],
    },
]

search_params_tag = {
    "search_term": "",
    "search_in": "value",
    "tag_purpose": ALL_VALUE,
    "tag_status": True,
}

search_params_cof_eoi = {
    "search_term": "",
    "search_in": "short_id",
    "filter_by_tag": ALL_VALUE,
}
LandingFilters = namedtuple("LandingFilters", ["filter_status", "filter_fund_type", "filter_fund_name"])
landing_filters = LandingFilters(filter_status=ALL_VALUE, filter_fund_type=ALL_VALUE, filter_fund_name="")
