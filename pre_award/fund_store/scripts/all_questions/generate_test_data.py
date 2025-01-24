import json
import os

START_TO_MAIN_ACTIVITIES = {
    "file_name": "start_to_main_activites.json",
    "start_page": "/intro-about-your-organisation",
    "end_page": "/tell-us-about-your-organisations-main-activities",
    "pages": [
        "/intro-about-your-organisation",
        "/alternative-organisation-name",
        "/organisation-details",
        "/tell-us-about-your-organisations-main-activities",
    ],
}

HOW_IS_ORG_CLASSIFIED = {
    "file_name": "how_is_org_classified.json",
    "start_page": "/how-is-your-organisation-classified",
    "end_page": "/organisation-address",
    "pages": [
        "/how-is-your-organisation-classified",
        "/how-is-your-organisation-classified-other",
        "/charity-number",
        "/company-registration-number",
        "/organisation-address",
    ],
}
JOINT_BID = {
    "file_name": "joint_bid_out_and_back.json",
    "start_page": "/joint-bid",
    "end_page": "/website-and-social-media",
    "pages": [
        "/partner-organisation-details",
        "/work-with-partner-organisations",
        "/agreement-exists",
        "/website-and-social-media",
        "/joint-bid",
    ],
}


def generate_test_data(target_test_files: [], in_path: str, out_folder: str):
    with open(in_path, "r") as f:
        all_data = json.load(f)

    for file in target_test_files:
        cutdown_data = {"start_page": file["start_page"], "all_pages": []}
        for p in file["pages"]:
            cutdown_data["all_pages"].append(next(page for page in all_data["all_pages"] if page["path"] == p))

        last_page = next(p for p in cutdown_data["all_pages"] if p["path"] == file["end_page"])
        last_page["next_paths"] = []
        last_page["all_possible_after"] = []

        with open(os.path.join(out_folder, file["file_name"]), "w") as f_out:
            json.dump(cutdown_data, f_out)
