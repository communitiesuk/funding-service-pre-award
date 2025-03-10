from datetime import datetime

from openpyxl import Workbook

from data.crud.applications import get_applications_for_round_by_status
from data.crud.assessment_records import get_assessments_by_round
from data.crud.fund_round_queries import get_funds_with_rounds
from pre_award.application_store.db.models.application.enums import Status


def export_applicant_information(workbook: Workbook) -> None:
    sheet = workbook.create_sheet(title="Applicant information")

    sheet.append(["Fund", "Fund Round", "FundID", "ID", "Submission date", "Product"])

    funds = get_funds_with_rounds()
    for fund in funds:
        for round in fund.rounds:
            assessments = get_assessments_by_round(round.id)
            for assessment in assessments:
                date_submitted = datetime.fromisoformat(str(assessment.jsonb_blob["date_submitted"]))

                row = [
                    fund.name_json["en"],
                    fund.name_json["en"] + " " + round.title_json["en"],
                    fund.short_name + "-" + round.short_name,
                    str(assessment.application_id),
                    date_submitted.strftime("%Y-%m-%d %H:%M:%S"),
                    "Apply",
                ]

                sheet.append(row)


def export_end_of_application_survey_data(workbook: Workbook) -> None:
    sheet = workbook.create_sheet(title="End of application survey data")

    sheet.append(["Fund", "application_id", "section", "comment", "rating", "date_submitted"])

    funds = get_funds_with_rounds()
    for fund in funds:
        for round in fund.rounds:
            applications = get_applications_for_round_by_status(round.id, [Status.SUBMITTED])
            for application in applications:
                feedback = application.end_of_application_survey
                for item in feedback:
                    date_submitted = datetime.fromisoformat(str(item.date_submitted))
                    section, comment, rating = item.get_section_comment_rating

                    row = [
                        fund.short_name + "-" + round.short_name,
                        str(application.id),
                        section,
                        comment,
                        rating,
                        date_submitted.strftime("%Y-%m-%d %H:%M:%S"),
                    ]

                    sheet.append(row)
