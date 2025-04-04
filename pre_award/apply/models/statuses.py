from flask_babel import gettext


def get_formatted(value: str):
    statuses = {
        "NOT_STARTED": gettext("Not started"),
        "IN_PROGRESS": gettext("In progress"),
        "COMPLETED": gettext("Completed"),
        "SUBMITTED": gettext("Submitted"),
        "NOT_SUBMITTED": gettext("Not submitted"),
        "READY_TO_SUBMIT": gettext("Ready to submit"),
        "CHANGE_REQUESTED": "Change requested",
    }
    return statuses.get(value, value.replace("_", " ").strip().title())
