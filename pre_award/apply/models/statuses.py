from flask_babel import gettext


def get_formatted(value: str):
    statuses = {
        "NOT_STARTED": gettext("Not Started"),
        "IN_PROGRESS": gettext("In Progress"),
        "COMPLETED": gettext("Completed"),
        "SUBMITTED": gettext("Submitted"),
        "NOT_SUBMITTED": gettext("Not Submitted"),
        "READY_TO_SUBMIT": gettext("Ready to Submit"),
        "CHANGE_REQUESTED": "Change Requested",
    }
    return statuses.get(value, value.replace("_", " ").strip().title())
