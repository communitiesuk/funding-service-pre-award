import pytest

from pre_award.assessment_store.db.queries.qa_complete.queries import (
    create_qa_complete_record,
    get_qa_complete_record_for_application,
)
from tests.pre_award.assessment_store_tests._helpers import get_assessment_record
from tests.pre_award.assessment_store_tests.conftest import test_input_data


@pytest.mark.apps_to_insert([test_input_data[0]])
def test_create_qa_complete_record_for_application(db, seed_application_records):
    """test_create_qa_complete_record Tests we can create qa_complete records in
    the qa_complete table in the appropriate format."""
    picked_row = get_assessment_record(seed_application_records[0]["application_id"])
    application_id = picked_row.application_id
    user_id = "test_user"
    qa_complete_record_metadata = create_qa_complete_record(application_id, user_id)
    assert len(qa_complete_record_metadata) == 5
    assert qa_complete_record_metadata["date_created"]
    assert qa_complete_record_metadata["user_id"] == "test_user"


@pytest.mark.apps_to_insert([test_input_data[0]])
def test_get_qa_complete_record_for_application(db, seed_application_records):
    """test_get_qa_complete_record Tests we can get qa_complete records in the
    qa_complete table in the appropriate format."""
    picked_row = get_assessment_record(seed_application_records[0]["application_id"])
    application_id = picked_row.application_id
    user_id = "test_user"
    create_qa_complete_record(application_id, user_id)
    qa_complete_record_metadata = get_qa_complete_record_for_application(application_id)
    assert len(qa_complete_record_metadata) == 5
    assert qa_complete_record_metadata["date_created"]
    assert qa_complete_record_metadata["user_id"] == "test_user"
