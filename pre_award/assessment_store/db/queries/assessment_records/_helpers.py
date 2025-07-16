from collections import defaultdict
from datetime import datetime

import jsonpath_rw_ext
import requests
from flask import current_app

from pre_award.assessment_store.config.mappings.assessment_mapping_fund_round import (
    fund_round_data_key_mappings,
)
from pre_award.assessment_store.db.models.assessment_record import TagAssociation

FIELD_DEFAULT_VALUE = "Not Available"


def get_answer_value(application_json, answer_key):
    try:
        return (
            jsonpath_rw_ext.parse(f"$.forms[*].questions[*].fields[?(@.key == '{answer_key}')]")
            .find(application_json)[0]
            .value["answer"]
        )
    except Exception as e:
        current_app.logger.warning(
            "Could not extract answer from question %(answer_key)s in application: %(application_id)s.",
            dict(application_id=application_json["id"], answer_key=answer_key),
            exc_info=e,
        )
        return None


def extract_multiinput_fields(application_json):
    """Yield all multiInput fields with answers from the application JSON."""
    for form in application_json.get("forms", []):
        for question in form.get("questions", []):
            for field in question.get("fields", []):
                if field.get("type") == "multiInput" and field.get("answer"):
                    if isinstance(field["answer"], list):
                        yield field["answer"]


def sum_keys_in_answer_dict(answer_dict, keys, application_id):
    """Sum the values for the given keys in a single answer_dict."""
    total = 0
    for key in keys:
        if key in answer_dict and answer_dict[key] is not None:
            try:
                total += int(float(answer_dict[key]))
            except Exception as e:
                current_app.logger.warning(
                    "Could not calculate total for %(answer_key)s in application: %(application_id)s.",
                    dict(
                        application_id=application_id,
                        answer_key=", ".join(keys) if isinstance(keys, list) else keys,
                    ),
                    exc_info=e,
                )
    return total


def sum_total_for_pfn(application_json, keys):
    """Sum values for a list of keys for PFN applications."""
    total = 0
    application_id = application_json.get("id")
    answers_list = extract_multiinput_fields(application_json)
    for answers in answers_list:
        for answer_dict in answers:
            if isinstance(answer_dict, dict):
                total += sum_keys_in_answer_dict(answer_dict, keys, application_id)
    return total


def get_answer_value_for_multi_input(application_json, answer_key, value_key):
    try:
        reference = application_json.get("reference", "")
        if reference.startswith(("PFN-RP",)) and isinstance(answer_key, list):
            # PFN logic. (answer_key is a list of keys to sum)
            return sum_total_for_pfn(application_json, answer_key)

        answers = (
            jsonpath_rw_ext.parse(f"$.forms[*].questions[*].fields[?(@.key == '{answer_key}')]")
            .find(application_json)[0]
            .value["answer"]
        )

        funding_one = 0
        for answer in answers:
            funding_one = funding_one + int(float(answer[value_key]))
        return funding_one
    except Exception as e:
        current_app.logger.warning(
            "Could not extract answer from question %(answer_key)s in application: %(application_id)s.",
            dict(application_id=application_json["id"], answer_key=answer_key),
            exc_info=e,
        )
        return None


def get_location_json_from_postcode(raw_postcode):
    """Make a POST request to the postcodes.io API with the provided postcode and
    extract the location data of postcode."""
    try:
        response = requests.post(
            url="http://api.postcodes.io/postcodes",
            json={"postcodes": [raw_postcode]},
            headers={"Content-Type": "application/json"},
        )
        if response.status_code != 200:
            current_app.logger.error(
                "Failed requesting location data for postcode %(postcode)s. Received error response %(response)s",
                dict(postcode=raw_postcode, response=response),
            )
            return None

        result = response.json()
        postcode_data = result["result"][0]["result"]
        location_data = (
            {
                "error": False,
                "postcode": raw_postcode,
                "county": postcode_data["admin_county"]
                if postcode_data["admin_county"]
                else postcode_data["admin_district"],
                "region": postcode_data["region"]
                if postcode_data["region"]
                else postcode_data["european_electoral_region"],
                "country": postcode_data["country"],
                "constituency": postcode_data["parliamentary_constituency"],
            }
            if postcode_data
            else None
        )
        return location_data

    except Exception as e:
        current_app.logger.error(
            "Failed requesting location data for postcode %(postcode)s", dict(postcode=raw_postcode), exc_info=e
        )
        return None


def derive_application_values(application_json):  # noqa: C901 - historical sadness
    # TODO: implement mapping function to match
    #  fund+round fields to derived values
    application_id = application_json["id"]
    fund_round_shortname = "".join(application_json["reference"].split("-")[:2])
    derived_values = {
        "application_id": application_id,
        "project_name": ""
        if application_json["project_name"] is None and fund_round_shortname == "COFEOI"
        else application_json["project_name"],
        "short_id": application_json["reference"],
        "fund_id": application_json["fund_id"],
        "round_id": application_json["round_id"],
        "funding_amount_requested": 0,
        "asset_type": "No asset type specified.",
        "language": application_json["language"],
        "location_json_blob": {
            "error": False,
            "postcode": FIELD_DEFAULT_VALUE,
            "county": FIELD_DEFAULT_VALUE,
            "region": FIELD_DEFAULT_VALUE,
            "country": FIELD_DEFAULT_VALUE,
            "constituency": FIELD_DEFAULT_VALUE,
        },
    }

    field_mappings = fund_round_data_key_mappings.get(fund_round_shortname, None)
    if not field_mappings:
        # Don't throw an exception here as we want to soft-fail - ie the submission process still works, but devs are
        # alerted to the lack of mappings
        current_app.logger.error(
            "No assessment data mappings for fund round {fund_round_shortname}. "
            "Cannot derive values for application {application_id}",
            extra=dict(fund_round_shortname=fund_round_shortname, application_id=application_id),
        )
        return derived_values

    # Some funds don't map any fields, so don't bother with the rest of this function if that's the case
    if all(field is None for field in field_mappings.values()):
        return derived_values

    current_app.logger.info(
        "Deriving values for application id: %(application_id)s.", dict(application_id=application_id)
    )

    try:
        # search for asset_type
        asset_type = "No asset type specified."
        if asset_key := field_mappings["asset_type"]:
            asset_type = get_answer_value(application_json, asset_key) or FIELD_DEFAULT_VALUE

        reference = application_json.get("reference", "")
        # Get the mapping for PFN-RP
        if reference.startswith("PFN-RP"):
            mapping = fund_round_data_key_mappings["PFNRP"]
            funding_one_keys = mapping["funding_one"]
            funding_two_keys = mapping["funding_two"]

        # search for capital funding
        funding_field_type = fund_round_data_key_mappings.get(fund_round_shortname, {}).get("funding_field_type")
        funding_one = 0
        if funding_one_keys := field_mappings["funding_one"]:
            funding_one_keys = [funding_one_keys] if isinstance(funding_one_keys, str) else funding_one_keys

            if funding_field_type == "multiInputField" and len(funding_one_keys) > 1:
                if reference.startswith(("PFN-RP",)):
                    funding_one = get_answer_value_for_multi_input(application_json, funding_one_keys, None)
                else:
                    funding_one = (
                        get_answer_value_for_multi_input(application_json, funding_one_keys[0], funding_one_keys[1])
                        or 0
                    )
            else:
                for key in funding_one_keys:
                    funding_one = funding_one + int(float(get_answer_value(application_json, key) or 0))

        # search for revenue funding
        funding_two = 0
        if funding_two_keys := field_mappings["funding_two"]:
            funding_two_keys = [funding_two_keys] if isinstance(funding_two_keys, str) else funding_two_keys
            if funding_field_type == "multiInputField" and len(funding_two_keys) > 1:
                if reference.startswith(("PFN-RP",)):
                    funding_two = get_answer_value_for_multi_input(application_json, funding_two_keys, None)
                else:
                    funding_two = (
                        get_answer_value_for_multi_input(application_json, funding_two_keys[0], funding_two_keys[1])
                        or 0
                    )
            else:
                for key in funding_two_keys:
                    funding_two = funding_two + int(float(get_answer_value(application_json, key) or 0))

        # search for location postcode
        location_data = None
        if address_key := field_mappings["location"]:
            address = get_answer_value(application_json, address_key)
            if address:
                raw_postcode = address.split(",")[-1].strip().replace(" ", "").upper()
                location_data = get_location_json_from_postcode(raw_postcode)

        derived_values["funding_amount_requested"] = funding_one + funding_two
        derived_values["asset_type"] = asset_type
        if location_data:
            derived_values["location_json_blob"] = location_data
        else:
            derived_values["location_json_blob"]["error"] = (
                True if address_key else False
            )  # if location is not mandatory for a fund, then treat error as `False`
    except Exception as e:
        current_app.logger.error(
            # Shouldn't ever get here, but quick catch all for the interim removal of the queue
            # and not breaking the submit process
            "Unexpected error when deriving values for application %(application_id)s",
            dict(application_id=application_id),
            exc_info=e,
        )

    return derived_values


def get_most_recent_tags(tag_associations):
    # Create a dictionary to group tag_associations by tag_id
    tag_id_dict = {}
    for tag_assoc in tag_associations:
        tag_id = tag_assoc["tag"]["id"]
        tag_id_dict.setdefault(tag_id, []).append(tag_assoc)

    updated_tag_associations = []
    for assoc_list in tag_id_dict.values():
        # Sort each group by created_at timestamp to find the most recent entry
        sorted_tags = sorted(
            assoc_list,
            key=lambda x: datetime.strptime(x["created_at"], "%Y-%m-%dT%H:%M:%S.%f%z"),
            reverse=True,
        )
        # Append the most recent tag association to the updated list
        updated_tag_associations.append(sorted_tags[0])

    return updated_tag_associations


def update_tag_associations(assessment_metadatas):
    for metadata in assessment_metadatas:
        # Retrieve tag associations for the current metadata
        tag_associations = metadata.get("tag_associations", [])
        if tag_associations:
            # Update tag_associations for the current metadata with the most recent entries
            metadata["tag_associations"] = get_most_recent_tags(tag_associations)
    return assessment_metadatas


def get_existing_tags(application_id):
    """Queries the database for existing tags associated with a specific
    application, organises them by tag ID, and returns a defaultdict where each
    tag ID is associated with a list containing tuples of creation timestamps and
    their corresponding tag instances.

    Example:
        {'0000000-00000-00000-000001':
        [(datetime.datetime(2023, 11, 17, 18, 48, 25, tzinfo=datetime.timezone.utc),
          <TagAssociation db91a66b->), .......
          ]}

    """
    existing_tags = TagAssociation.query.filter(
        TagAssociation.application_id == application_id,
    ).all()
    list_existing_tags = defaultdict(list)
    for existing_tag in existing_tags:
        tag_id = str(existing_tag.tag_id)
        list_existing_tags[tag_id].append((existing_tag.created_at, existing_tag))
    return list_existing_tags


def filter_tags(incoming_tags, existing_tags):
    """If an incoming tag ID matches an existing tag ID, it skips that tag;
    otherwise, it appends the tag list from the existing tags to the filtered tags
    list."""
    filtered_tags = []
    for (
        existing_tag_id,
        existing_tag_list,
    ) in existing_tags.items():
        _incoming_tag = next(
            (incoming_tag for incoming_tag in incoming_tags if incoming_tag.get("id") == existing_tag_id),
            None,
        )
        if _incoming_tag:
            current_app.logger.info(
                "Tag id is already associated: %(existing_tag_id)s", dict(existing_tag_id=existing_tag_id)
            )
        else:
            filtered_tags.append(existing_tag_list)
    return filtered_tags
