import click
from sqlalchemy.orm.attributes import flag_modified

from app import create_app
from pre_award.application_store.db.models import Applications
from pre_award.application_store.db.queries.application import (
    get_applications_by_references,
)
from pre_award.assess.services.aws import delete_file_from_aws, list_files_in_folder
from pre_award.assessment_store.db.models import AssessmentRecord
from pre_award.assessment_store.db.queries.assessment_records.queries import (
    get_assessment_record,
)
from pre_award.db import db

app = create_app()


def _parse_refs(_ctx, _param, values) -> list[str]:
    items = []
    if values is None:
        raise click.BadParameter("No application reference to delete")
    for item in values.split(","):
        items.append(item.strip())
    return items


@click.command()
@click.option(
    "-r",
    "--application-reference",
    "application_references",
    callback=_parse_refs,
    help="Application reference to delete applications for",
)
def delete_grant_application_data(application_references: list[str]) -> None:
    print(f"Initialise application data deletion for application reference of {application_references}")
    if not application_references:
        print("Initialise application data deletion for reference(s): NONE PROVIDED")
        return

    applications: dict[str, Applications] = get_applications_by_references(application_references)
    if not applications:
        print("No application found with reference")
        return

    for application in applications.values():
        try:
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
