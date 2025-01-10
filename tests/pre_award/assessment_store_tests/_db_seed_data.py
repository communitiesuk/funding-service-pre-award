from tests.pre_award.assessment_store_tests._application_store_json import (
    application_store_json_template,
    cof25_eoi_application_store_json_template,
    cof25r1_application_store_json_template,
    cof_eoi_application_store_json_template,
    cofr3w1_application_store_json_template,
    cofr3w2_application_store_json_template,
    cofr3w3_application_store_json_template,
    cofr4w1_application_store_json_template,
    cofr4w2_application_store_json_template,
    cypr1_application_store_json_template,
    dpifr2_application_store_json_template,
    hsra_rp_application_store_json_template,
    hsra_vr_application_store_json_template,
    nstfr2_application_store_json_template,
)

# Put a sample of output data (from application store) for a fund-round here
mappings_application_store_json = {
    "COFR2W2": application_store_json_template,
    "COFR2W3": application_store_json_template,
    "COFR3W1": cofr3w1_application_store_json_template,
    "COFR3W2": cofr3w2_application_store_json_template,
    "COFR3W3": cofr3w3_application_store_json_template,
    "COFR4W1": cofr4w1_application_store_json_template,
    "COFR4W2": cofr4w2_application_store_json_template,
    "COF25R1": cof25r1_application_store_json_template,
    "COF25EOI": cof25_eoi_application_store_json_template,
    "COFEOI": cof_eoi_application_store_json_template,
    "NSTFR2": nstfr2_application_store_json_template,
    "CYPR1": cypr1_application_store_json_template,
    "DPIFR2": dpifr2_application_store_json_template,
    "HSRAVR": hsra_vr_application_store_json_template,
    "HSRARP": hsra_rp_application_store_json_template,
    "RANDOM_FUND_ROUND": application_store_json_template,
}

mappings_short_name_to_reference_prepend = {
    "COFR2W2": "COF-R2W2",
    "COFR2W3": "COF-R2W3",
    "COFR3W1": "COF-R3W1",
    "COFR3W2": "COF-R3W2",
    "COFR3W3": "COF-R3W3",
    "COFR4W1": "COF-R4W1",
    "COFR4W2": "COF-R4W2",
    "COF25R1": "COF25-R1",
    "COFEOI": "COF-EOI-R1",
    "COF25EOI": "COF25-EOI-R1",
    "NSTFR2": "NSTF-R2",
    "CYPR1": "CYP-R1",
    "DPIFR2": "DPIF-R2",
    "HSRAVR": "HSRA-VR",
    "HSRARP": "HSRA-RP",
    "RANDOM_FUND_ROUND": "RFR",
}


def get_dynamic_rows(
    number_of_apps_per_round,
    number_of_funds,
    number_of_rounds,
    fund_round_config_dict,
):
    from random import choice, sample
    from string import ascii_uppercase
    from uuid import uuid4

    fund_round_short_name = list(fund_round_config_dict.keys())[0]
    fund_round_config = fund_round_config_dict[fund_round_short_name]
    application_store_json = mappings_application_store_json[fund_round_short_name]
    application_short_ref_prefix = mappings_short_name_to_reference_prepend[fund_round_short_name]

    funds = [fund_round_config["fund_id"]] if fund_round_config else [uuid4() for _ in range(number_of_funds)]

    verbs = ["Save", "Restore", "Refurbish", "Rebuild", "Remodel"]

    adjects = ["old", "humble", "derelict", "vintage", "loved", "beautiful"]

    local_authorities = [
        "Gravesham Borough Council",
        "Great Yarmouth Borough Council",
        "Guildford Borough Council",
        "Gwynedd County Council",
        "Halton Borough Council",
        "Hambleton District Council",
        "Hampshire County Council",
        "Uttlesford District Council",
        "Vale of Glamorgan Council",
        "Vale of White Horse District Council",
        "Wakefield Metropolitan District Council",
    ]
    org_names = [
        "Friendly housing foundation",
        "Night shelters ltd",
        "Local shelter org",
        "Action for Homelessness",
    ]
    funding_types = ["revenue", "capital", "both-revenue-and-capital"]
    places = [
        ("skatepark", "sporting"),
        ("pub", "pub"),
        ("cinema", "cinema"),
        ("community centre", "community-centre"),
        ("gallery", "gallery"),
        ("museum", "museum"),
    ]
    cities = [
        ("Exeter", "England", "EX44NT"),
        ("Hasland", "England", "S41 0HX"),
        ("Aberdeen", "Scotland", "AB11 6LX"),
        ("Cardiff", "Wales", "CF10 1EP"),
        ("Newport", "Wales", "NP10 8QQ"),
        ("Solihull", "England", "B90 3AQ"),
    ]

    funding = [
        ("2300", "2300"),
        ("3000", "1500"),
        ("5000", "4000"),
        ("1000", "1000"),
        ("2345", "450"),
        ("1230", "4020"),
        ("3050", "850"),
    ]

    for _count, fund_id in enumerate(funds):
        print("fund id:", fund_id)

        rounds = [fund_round_config["round_id"]] if fund_round_config else [uuid4() for _ in range(number_of_rounds)]

        for round_id in rounds:
            print("round id:", round_id)

            app_ids = [uuid4() for _ in range(number_of_apps_per_round)]

            for app_id in app_ids:
                print("application id:", app_id)
                picked_place = choice(places)
                picked_city = choice(cities)
                picked_funding = choice(funding)
                picked_la = choice(local_authorities)
                funding_type = choice(funding_types)
                org_name = choice(org_names)

                project_name = f"{choice(verbs)} the {choice(adjects)} {picked_place[0]} in {picked_city[0]}"

                short_ref = application_short_ref_prefix + "-" + "".join(sample(ascii_uppercase, 6))

                print("Seeding db inc location info")
                location_json_blob = {
                    "location_error": "false",
                    "location_county": "test-county",
                    "location_region": picked_city[1],
                    "location_country": picked_city[1],
                    "location_postcode": picked_city[2] if len(picked_city) > 2 else "QQ12QQ",
                    "location_constituency": "test-constituency",
                }
                yield application_store_json.substitute(
                    app_id=app_id,
                    project_name=project_name,
                    short_ref=short_ref,
                    round_id=round_id,
                    fund_id=fund_id,
                    capital_funding=picked_funding[0],
                    revenue_funding=picked_funding[1],
                    asset_type=picked_place[1],
                    local_authority=picked_la,
                    org_name=org_name,
                    funding_type=funding_type,
                    **location_json_blob,
                )
