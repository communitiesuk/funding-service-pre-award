import datetime
from uuid import uuid4

from pre_award.assessment_store.db.models.flags.flag_update import FlagStatus

now = datetime.datetime.now()
earlier = now - datetime.timedelta(days=1)

user_id = uuid4()
flag_config = [
    {
        "status": FlagStatus.RAISED,
        "justification": "Test justification 1",
        "sections_to_flag": ["Test section 1"],
        "date_created": earlier,
        "user_id": user_id,
        "allocation": "TEAM_1",
    },
    {
        "status": FlagStatus.RAISED,
        "justification": "Test justification 2",
        "sections_to_flag": ["Test section 2"],
        "date_created": earlier,
        "user_id": user_id,
        "allocation": "TEAM_2",
    },
    {
        "status": FlagStatus.RAISED,
        "justification": "Test justification 3",
        "sections_to_flag": ["Test section 3"],
        "date_created": earlier,
        "user_id": user_id,
        "allocation": "TEAM_3",
    },
]

add_flag_update_request_json = {
    "user_id": str(user_id),
    "status": FlagStatus.STOPPED,
    "allocation": "TEAM_2",
    "justification": "stopping assessment",
}

create_flag_request_json = {
    "justification": "some text",
    "status": FlagStatus.RAISED,
    "allocation": "TEAM_1",
    "sections_to_flag": ["section_1"],
    "user_id": str(user_id),
}
