from flask import current_app
from invoke import Context, task  # type: ignore[attr-defined]
from openpyxl import Workbook

from app import create_app
from reporting.reporting import export_applicant_information, export_end_of_application_survey_data


def build_report_impl() -> None:
    current_app.logger.info("Building the report")

    workbook = Workbook()

    # Remove default sheet, always exists, but typed as Optional :shrug:
    default_sheet = workbook.active
    if default_sheet is not None:
        workbook.remove(default_sheet)

    # List of reports
    reports = [
        export_applicant_information,
        export_end_of_application_survey_data,
    ]

    for report_function in reports:
        report_function(workbook)

    workbook.save("reports.xlsx")

    current_app.logger.info("Building the report finished")


@task
def send_report(c: Context) -> None:
    app = create_app()
    with app.app_context():
        build_report_impl()
