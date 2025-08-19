import click
from sqlalchemy.orm.attributes import flag_modified

from app import create_app
from pre_award.application_store.db.models import Applications
from pre_award.application_store.db.queries.application import get_application_by_reference
from pre_award.assess.services.aws import delete_file_from_aws, list_files_in_folder
from pre_award.assessment_store.db.models import AssessmentRecord
from pre_award.assessment_store.db.queries.assessment_records.queries import (
    get_assessment_record,
)
from pre_award.db import db

app = create_app()


@click.command()
@click.option(
    "--application_reference",
    help="Application reference to delete applications for",
    prompt=True,
)
def delete_grant_application_data(application_reference) -> None:
    print(f"Initialise application data deletion for application reference of {application_reference}")
    try:
        application: Applications = get_application_by_reference(application_reference)
        if not application:
            print(f"No application found with reference {application_reference}")
            return
        for form in application.forms:
            db.session.delete(form)
        application.is_deleted = True
        application.project_name = ""
        s3_files_list = list_files_in_folder(f"{application.id}/")
        print(f"Found {len(s3_files_list)} files in {application.id}")
        for file_key in s3_files_list:
            delete_file_from_aws(file_key)
        db.session.add(application)
        db.session.commit()
        print(f"Application marked as deleted and application id is {application.id}")
        assessment_record: AssessmentRecord = get_assessment_record(application.id)
        if assessment_record:
            assessment_record.is_deleted = True
            assessment_record.project_name = ""
            assessment_record.jsonb_blob["forms"] = []
            assessment_record.jsonb_blob["is_deleted"] = True
            flag_modified(assessment_record, "jsonb_blob")
            db.session.add(assessment_record)
            db.session.commit()
            print(f"Assessment marked as deleted and application id is {application.id}")
    except Exception as e:
        db.session.rollback()
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    with app.app_context():
        delete_grant_application_data()
