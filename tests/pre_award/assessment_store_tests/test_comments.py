import io
from collections import Counter
from datetime import timedelta
from uuid import uuid4

import pandas as pd

from pre_award.application_store.db.models import Applications
from pre_award.assessment_store.db.models.assessment_record.assessment_records import AssessmentRecord
from pre_award.assessment_store.db.models.comment.enums import CommentType
from pre_award.assessment_store.db.queries.comments.queries import export_comments_to_excel, get_comments_for_export
from tests.pre_award.assessment_store_tests.conftest import create_comment_with_updates


def test_export_comments_to_excel(
    db,
    app,
    mock_comments_sub_criteria,
    comments_test_account,
    comments_base_time,
    comments_data,
):
    application_id = str(uuid4())
    test_fund_id = str(uuid4())
    test_round_id = str(uuid4())
    user_id = comments_test_account.id

    test_application = Applications(
        id=application_id,
        account_id=user_id,
        fund_id=test_fund_id,
        round_id=test_round_id,
        key="test-key",
        language="en",
        reference="TEST-REF",
        project_name="Test Project",
    )
    db.session.add(test_application)

    test_assessment_record = AssessmentRecord(
        application_id=application_id,
        short_id="TEST-SHORT-ID",
        type_of_application="Test",
        project_name="Test Project",
        funding_amount_requested=10000,
        round_id=test_round_id,
        fund_id=test_fund_id,
        language="en",
        workflow_status="SUBMITTED",
        asset_type="Test",
        jsonb_blob={},
    )
    db.session.add(test_assessment_record)
    db.session.commit()

    # Create comments with updates for the test application
    for idx, cdata in enumerate(comments_data):
        create_comment_with_updates(
            db=db,
            application_id=application_id,
            user_id=user_id,
            sub_criteria_id=cdata["sub_criteria_id"],
            comment_type=cdata["comment_type"],
            update_texts=cdata["updates"],
            comments_base_time=comments_base_time + timedelta(hours=idx),
            account=comments_test_account,
        )

    # Create a different application to later check for filtering
    other_app = Applications(
        id="00000000-0000-0000-0000-000000000000",
        account_id="other-user",
        fund_id=str(uuid4()),
        round_id=str(uuid4()),
        key="other-key",
        language="en",
        reference="OTHER-REF",
        project_name="Other Project",
    )
    db.session.add(other_app)
    db.session.commit()

    # Create an assessment record for the other application
    assessment_record = AssessmentRecord(
        application_id=other_app.id,
        short_id="OTHER-SHORT-ID",
        type_of_application="Test",
        project_name="Other Project",
        funding_amount_requested=0,
        round_id=other_app.round_id,
        fund_id=other_app.fund_id,
        language="en",
        workflow_status="NOT_STARTED",
        asset_type="Test",
        jsonb_blob={},
    )
    db.session.add(assessment_record)
    db.session.commit()

    # Create a comment for the other application
    create_comment_with_updates(
        db=db,
        application_id=other_app.id,
        user_id="other-user",
        sub_criteria_id=None,
        comment_type=CommentType.WHOLE_APPLICATION,
        update_texts=["Other app comment"],
        comments_base_time=comments_base_time,
        account=comments_test_account,
    )

    # Retrieve comments for the test application
    comments_list = get_comments_for_export(
        fund_id=test_fund_id,
        round_id=test_round_id,
        application_id=application_id,
    )

    # Export to Excel (in-memory)
    fund_short_name = "TEST"
    round_short_name = "ROUND"
    with app.test_request_context():
        response = export_comments_to_excel(
            comments_list, fund_short_name, round_short_name, application_id=application_id
        )
        response.direct_passthrough = False
        output = response.get_data()

    # Read the Excel file
    output_io = io.BytesIO(output)
    df = pd.read_excel(output_io)

    # Check that all comments for the test application are present
    expected_comments = []
    for cdata in comments_data:
        expected_comments.extend(cdata["updates"])
    assert Counter(df["Comment"]) == Counter(expected_comments)

    # Check that no comments from the other applications are present
    assert "Other app comment" not in df["Comment"].values

    # Check ordering: Application-level comments (sub_criteria_id=None) first,
    # then by sub_criteria_id, then by date_created
    sub_criteria_col = df["Sub-criteria name"].fillna("None").values
    app_level_end = 0
    for val in sub_criteria_col:
        if val == "None":
            app_level_end += 1
        else:
            break

    # All application-level comments should be at the top
    assert all(val == "None" for val in sub_criteria_col[:app_level_end])
    # The rest should be grouped by sub_criteria_id (SC1, then SC2)
    sc1_start = app_level_end
    sc1_end = sc1_start + sum(1 for c in comments_data if c["sub_criteria_id"] == "SC1" for _ in c["updates"])
    assert all(val == "Sub Criteria 1" for val in sub_criteria_col[sc1_start:sc1_end])
    assert all(val == "Sub Criteria 2" for val in sub_criteria_col[sc1_end:])
