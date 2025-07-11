import requests
from flask import current_app

from pre_award.assessment_store.db.models.assessment_record.enums import Status
from pre_award.config import Config


def get_status(questions):
    """_summary_: GIVEN function return a dictionary
    of statuses.

    Args:
        questions: Takes get_questions() function

    Returns:
        Returns dictionary of statuses
    """
    status = {}
    if questions:
        status["NOT STARTED"] = sum(value == "NOT STARTED" for value in questions.values())
        status["IN PROGRESS"] = sum(value == "IN PROGRESS" for value in questions.values())
        status["COMPLETED"] = sum(value == "COMPLETED" for value in questions.values())
        status["TOTAL"] = sum(
            ((value == "NOT STARTED") + (value == "IN PROGRESS") + (value == "COMPLETED"))
            for value in questions.values()
        )
    return status


def all_status_completed(criteria_list):
    """Function checks if all statuses are completed then returns True
    otherwise returns False"""
    return all(
        sub_criteria.status == "COMPLETED"
        for criteria in criteria_list.criterias
        for sub_criteria in criteria.sub_criterias
    )


def update_ar_status_to_completed(application_id):
    """Function makes a call to assessment store to update the
    status of given application_id to COMPLETED"""
    response = requests.post(Config.ASSESSMENT_UPDATE_STATUS.format(application_id=application_id))
    if response.status_code == 204:
        current_app.logger.info("The application status has been updated to COMPLETE")
        return response
    else:
        current_app.logger.error("Not Found: application_id not found")


def update_ar_status_to_qa_completed(application_id, user_id):
    """Function makes a call to assessment store to update the
    status of given application_id to COMPLETED"""
    response = requests.post(Config.ASSESSMENT_UPDATE_QA_STATUS.format(application_id=application_id, user_id=user_id))
    if response.status_code == 200:
        current_app.logger.info("The application status has been updated to QA_COMPLETE")
        return response
    else:
        current_app.logger.error(
            "Could not create qa_complete record for application %(application_id)s",
            dict(application_id=application_id),
        )


def is_score_or_change_request_allowed_uncompeted(state, sub_criteria_id):
    """
    Return True if 'Approve and score' or change request is allowed.

    Approve (Score) / change request is allowed only if:
    - The application has NOT been marked as QA complete (Moderation complete for uncompeted funds)
    - The sub-criteria is NOT already in 'CHANGE_REQUESTED' status
    """
    if state.is_qa_complete:
        return False

    for criteria in state.criterias:
        for sub in criteria.sub_criterias:
            if sub.id == sub_criteria_id and sub.status == Status.CHANGE_REQUESTED.name:
                return False

    return True
