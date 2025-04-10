import time
from distutils.util import strtobool

from flask import current_app, jsonify, request, send_file
from flask.views import MethodView
from fsd_utils import evaluate_response
from sqlalchemy.orm.exc import NoResultFound

from pre_award.application_store._helpers import get_blank_forms, order_applications
from pre_award.application_store._helpers.application import send_change_received_notification, send_submit_notification
from pre_award.application_store.db.exceptions.submit import SubmitError
from pre_award.application_store.db.models.application.enums import Status
from pre_award.application_store.db.queries import (
    add_new_forms,
    create_application,
    export_json_to_csv,
    export_json_to_excel,
    get_application,
    get_feedback,
    get_fund_id,
    get_general_status_applications_report,
    get_key_report_field_headers,
    get_report_for_applications,
    search_applications,
    submit_application,
    update_form,
    upsert_feedback,
)
from pre_award.application_store.db.queries.application import create_qa_base64file
from pre_award.application_store.db.queries.feedback import (
    retrieve_all_feedbacks_and_surveys,
    retrieve_end_of_application_survey_data,
    upsert_end_of_application_survey_data,
)
from pre_award.application_store.db.queries.reporting.queries import (
    export_application_statuses_to_csv,
)
from pre_award.application_store.db.queries.research import (
    retrieve_research_survey_data,
    upsert_research_survey_data,
)
from pre_award.application_store.db.queries.statuses import (
    check_is_fund_round_open,
    update_statuses,
)
from pre_award.application_store.external_services import (
    get_account,
    get_fund,
    get_round,
    get_round_eoi_schema,
)
from pre_award.application_store.external_services.exceptions import (
    NotificationError,
)
from pre_award.common.blueprints import Blueprint

application_store_bp = Blueprint("application_store_bp", __name__)


class ApplicationsView(MethodView):
    def get(self):
        application_id = request.args.get("application_id")
        account_id = request.args.get("account_id")
        fund_id = request.args.get("fund_id")
        round_id = request.args.get("round_id")
        status_only = request.args.getlist("status_only")
        forms = strtobool(request.args.get("forms", "false"))
        response_headers = {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Credentials": True,
        }
        matching_applications = search_applications(
            application_id=application_id,
            account_id=account_id,
            fund_id=fund_id,
            round_id=round_id,
            status_only=status_only,
            forms=forms,
        )
        order_by = request.args.get("order_by")
        order_rev = request.args.get("order_rev")
        sorted_applications = order_applications(matching_applications, order_by, order_rev)
        return sorted_applications, 200, response_headers

    def post(self):
        args = request.get_json()
        account_id = args["account_id"]
        round_id = args["round_id"]
        fund_id = args["fund_id"]
        language = args["language"]
        fund = get_fund(fund_id=fund_id)
        if language == "cy" and not fund.welsh_available:
            language = "en"
        empty_forms = get_blank_forms(fund_id=fund_id, round_id=round_id, language=language)
        application = create_application(
            account_id=account_id,
            fund_id=fund_id,
            round_id=round_id,
            language=language,
        )
        add_new_forms(forms=empty_forms, application_id=application.id)
        return application.as_dict(), 201


class ApplicationByIdView(MethodView):
    def get(self, application_id):
        with_questions_file = strtobool(request.args.get("with_questions_file", "false"))
        try:
            return_dict = get_application(application_id, as_json=True, include_forms=True)
            return_dict = create_qa_base64file(return_dict, with_questions_file)
            return return_dict, 200
        except ValueError as e:
            current_app.logger.error(
                "Value error getting application ID: %(application_id)s", dict(application_id=application_id)
            )
            raise e
        except NoResultFound as e:
            return {"code": 404, "message": str(e)}, 404


class ApplicationsKeyApplicationMetricsView(MethodView):
    def get(self, application_id):
        try:
            return send_file(
                export_json_to_csv(get_report_for_applications(application_ids=[application_id])),
                "text/csv",
                as_attachment=True,
                download_name="required_data.csv",
            )
        except NoResultFound as e:
            return {"code": 404, "message": str(e)}, 404


class ApplicationsStatusesDataView(MethodView):
    def get(self):
        round_id = request.args.getlist("round_id")
        fund_id = request.args.getlist("fund_id")
        format = request.args.get("format", "csv")
        try:
            report_data = get_general_status_applications_report(
                round_id or None,
                fund_id or None,
            )
        except NoResultFound as e:
            return {"code": 404, "message": str(e)}, 404

        if format.lower() == "json":
            response = jsonify({"metrics": report_data})
            response.headers["Content-Type"] = "application/json"
            return response
        else:
            return send_file(
                export_application_statuses_to_csv(report_data),
                "text/csv",
                as_attachment=True,
                download_name="required_data.csv",
            )


class KeyApplicationMetricsDataView(MethodView):
    def get(self):
        status = request.args.get("status", Status.SUBMITTED.name)
        round_id = request.args.get("round_id")
        fund_id = request.args.get("fund_id")
        try:
            return send_file(
                export_json_to_csv(
                    get_report_for_applications(status=status, round_id=round_id, fund_id=fund_id),
                    get_key_report_field_headers(round_id),
                ),
                "text/csv",
                as_attachment=True,
                download_name="required_data.csv",
            )
        except NoResultFound as e:
            return {"code": 404, "message": str(e)}, 404


class ApplicationsFormView(MethodView):
    def put(self):
        request_json = request.get_json(force=True)
        form_dict = {
            "application_id": request_json["metadata"]["application_id"],
            "form_name": request_json["metadata"].get("form_name"),
            "question_json": request_json["questions"],
            "is_summary_page_submit": request_json["metadata"].get("isSummaryPageSubmit", False),
        }
        try:
            updated_form = update_form(**form_dict)
            is_round_open = check_is_fund_round_open(form_dict["application_id"])
            if not is_round_open:
                current_app.logger.info("Round is closed so user will be redirected")
                return {}, 301
            return updated_form, 201
        except NoResultFound as e:
            return {"code": 404, "message": str(e)}, 404


class SubmitApplicationView(MethodView):
    def get_application_eoi_response(self, application):
        eoi_schema = get_round_eoi_schema(application["fund_id"], application["round_id"], application["language"])
        result = evaluate_response(eoi_schema, application["forms"])
        return result

    def post(self, application_id):
        should_send_email = True
        send_email_to_assessor = False
        if request.args.get("dont_send_email") == "true":
            should_send_email = False

        check_application = get_application(application_id)
        if check_application.date_submitted is not None:
            send_email_to_assessor = True

        # Do the submission
        try:
            application = submit_application(application_id)
        except SubmitError as submit_error:
            return {"message": f"Unable to submit application {submit_error.application_id}"}, 500

        # Get EOI decision
        fund_id = get_fund_id(application_id)
        round_data = get_round(fund_id, application.round_id)
        application_with_form_json = get_application(application_id, as_json=True, include_forms=True)
        if round_data.is_expression_of_interest:
            eoi_results = self.get_application_eoi_response(application_with_form_json)
            eoi_decision = eoi_results["decision"]
        else:
            eoi_results = None
            eoi_decision = None

        # Send notification
        try:
            if should_send_email:
                fund_data = get_fund(fund_id)
                account = get_account(account_id=application.account_id)
                language = application_with_form_json["language"]
                application_with_form_json_and_fund_name = {
                    **application_with_form_json,
                    "fund_name": fund_data.name_json[language],
                    "fund_short_name": fund_data.short_name,
                    "round_name": round_data.title_json[language],
                    "prospectus_url": round_data.prospectus_url,
                }

                if send_email_to_assessor:
                    send_change_received_notification(
                        fund=fund_data,
                        round_data=round_data,
                    )

                send_submit_notification(
                    application_with_form_json=application_with_form_json,
                    eoi_results=eoi_results,
                    account=account,
                    application_with_form_json_and_fund_name=application_with_form_json_and_fund_name,
                    application=application,
                    round_data=round_data,
                )

        except NotificationError:
            current_app.logger.exception(
                "Notification error on sending SUBMIT notification for application %(application_id)s",
                dict(application_id=application_id),
            )

        return {
            "id": application_id,
            "reference": application_with_form_json["reference"],
            "email": account.email,
            "eoi_decision": eoi_decision,
        }, 201


class ApplicationFeedbackView(MethodView):
    def post(self):
        args = request.get_json()
        application_id = args["application_id"]
        fund_id = args["fund_id"]
        round_id = args["round_id"]
        section_id = args["section_id"]
        feedback_json = args["feedback_json"]
        status = args["status"]

        feedback = upsert_feedback(
            application_id=application_id,
            fund_id=fund_id,
            round_id=round_id,
            section_id=section_id,
            feedback_json=feedback_json,
            status=status,
        )

        update_statuses(application_id, form_name=None)

        return feedback.as_dict(), 201

    def get(self):
        application_id = request.args["application_id"]
        section_id = request.args["section_id"]
        feedback = get_feedback(application_id, section_id)
        if feedback:
            return feedback.as_dict(), 200

        return {
            "code": 404,
            "message": f"Feedback not fund for {application_id}, {section_id}",
        }, 404


class EndOfApplicationSurveyDataView(MethodView):
    def post(self):
        args = request.get_json()
        application_id = args["application_id"]
        fund_id = args["fund_id"]
        round_id = args["round_id"]
        page_number = args["page_number"]
        data = args["data"]

        survey_data = upsert_end_of_application_survey_data(
            application_id=application_id,
            fund_id=fund_id,
            round_id=round_id,
            page_number=page_number,
            data=data,
        )

        update_statuses(application_id, form_name=None)

        return survey_data.as_dict(), 201

    def get(self):
        application_id = request.args["application_id"]
        page_number = request.args["page_number"]
        survey_data = retrieve_end_of_application_survey_data(application_id, int(page_number))
        if survey_data:
            return survey_data.as_dict(), 200

        return {
            "code": 404,
            "message": f"End of application feedback survey data for {application_id}, {page_number} not found",
        }, 404


class GetAllFeedbacksAndSurveyReportView(MethodView):
    def get(self):
        fund_id = request.args["fund_id"]
        round_id = request.args["round_id"]
        status = request.args.get("status_only")

        try:
            return send_file(
                path_or_file=export_json_to_excel(retrieve_all_feedbacks_and_surveys(fund_id, round_id, status)),
                mimetype="application/vnd.ms-excel",
                as_attachment=True,
                download_name=f"fsd_feedback_{str(int(time.time()))}.xlsx",
            )
        except NoResultFound as e:
            return {"code": 404, "message": str(e)}, 404


class ApplicationResearchView(MethodView):
    def post(self):
        """
        Endpoint to post research survey data.

        This method retrieves application_id, fund_id, round_id, and (form) data and will either
        create or update the research survey associated with that application. Finally the
        application status is checked.

        Returns:
            Research survey data in dict form and HTTP status code 201 (Created).
        """
        args = request.get_json()
        application_id = args["application_id"]
        fund_id = args["fund_id"]
        round_id = args["round_id"]
        data = args["data"]

        survey_data = upsert_research_survey_data(
            application_id=application_id,
            fund_id=fund_id,
            round_id=round_id,
            data=data,
        )

        update_statuses(application_id, form_name=None)

        return survey_data.as_dict(), 201

        return {
            "code": 404,
            "message": f"Research survey data for {application_id} not found",
        }, 404

    def get(self):
        """
        Endpoint to retrieve research survey data for a given application_id.

        Args:
            application_id (str): The ID of the application for which survey data is requested.

        Returns:
            If found, survey data in dict form is returned with 200 HTTP code
            Else an error message with HTTP status code 404.
        """
        application_id = request.args["application_id"]
        survey_data = retrieve_research_survey_data(application_id)
        if survey_data:
            return survey_data.as_dict(), 200

        return {
            "code": 404,
            "message": f"Research survey data for {application_id} not found",
        }, 404


application_store_bp.add_url_rule(
    "/application/feedback", view_func=ApplicationFeedbackView.as_view("application_feedback")
)
application_store_bp.add_url_rule(
    "/application/research", view_func=ApplicationResearchView.as_view("application_research")
)
application_store_bp.add_url_rule("/applications/forms", view_func=ApplicationsFormView.as_view("application_forms"))

application_store_bp.add_url_rule("/applications", view_func=ApplicationsView.as_view("applications"))
application_store_bp.add_url_rule(
    "/applications/<application_id>", view_func=ApplicationByIdView.as_view("application_by_id")
)
application_store_bp.add_url_rule(
    "/applications/<application_id>/submit", view_func=SubmitApplicationView.as_view("submit_application")
)

application_store_bp.add_url_rule(
    "/applications/reporting/key_application_metrics",
    view_func=KeyApplicationMetricsDataView.as_view("key_application_metrics"),
)
application_store_bp.add_url_rule(
    "/applications/reporting/key_application_metrics/<application_id>",
    view_func=ApplicationsKeyApplicationMetricsView.as_view("key_application_metrics_for_application_id"),
)
application_store_bp.add_url_rule(
    "/applications/reporting/applications_statuses_data",
    view_func=ApplicationsStatusesDataView.as_view("applications_statuses_data"),
)

application_store_bp.add_url_rule(
    "/application/end_of_application_survey_data",
    view_func=EndOfApplicationSurveyDataView.as_view("end_of_application_survey_data"),
)
application_store_bp.add_url_rule(
    "/applications/get_all_feedbacks_and_survey_report",
    view_func=GetAllFeedbacksAndSurveyReportView.as_view("get_all_feedbacks_and_survey_report"),
)
