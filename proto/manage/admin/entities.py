from abc import abstractmethod

from flask_admin.contrib import sqla
from flask_wtf import FlaskForm

from proto.common.data.models import (
    ProtoDataCollectionDefinitionQuestion,
    ProtoDataCollectionDefinitionSection,
    ProtoReportingRound,
    TemplateSection,
)
from proto.common.data.models.fund import Fund
from proto.common.data.models.question_bank import (
    DataStandard,
    TemplateQuestion,
)
from proto.common.data.models.round import Round


class BaseAdmin(sqla.ModelView):
    form_base_class = FlaskForm

    page_size = 50
    can_set_page_size = True

    can_create = False
    can_view_details = True
    can_edit = False
    can_delete = False
    can_export = False

    form_excluded_columns = ["created_at", "updated_at"]

    def __init__(
        self,
        session,
        name=None,
        category=None,
        endpoint=None,
        url=None,
        static_folder=None,
        menu_class_name=None,
        menu_icon_type=None,
        menu_icon_value=None,
    ):
        super().__init__(
            self._model,
            session,
            name=name,
            category=category,
            endpoint=endpoint,
            url=url,
            static_folder=static_folder,
            menu_class_name=menu_class_name,
            menu_icon_type=menu_icon_type,
            menu_icon_value=menu_icon_value,
        )

    @property
    @abstractmethod
    def _model(self):
        pass


class FundAdmin(BaseAdmin):
    _model = Fund

    can_create = True
    can_edit = True

    column_list = [
        Fund.short_name,
        Fund.name_json,
        Fund.title_json,
        Fund.welsh_available,
        Fund.owner_organisation_shortname,
    ]

    column_labels = dict(short_name="code", name_json="Name", title_json="Title")

    column_formatters = dict(
        name_json=lambda v, c, m, p: m.name_json["en"], title_json=lambda v, c, m, p: m.title_json["en"]
    )


class RoundAdmin(BaseAdmin):
    _model = Round

    can_create = True
    can_edit = True

    column_list = [
        "proto_grant.short_name",
        Round.short_name,
        Round.title_json,
        Round.proto_start_date,
        Round.proto_end_date,
        Round.assessment_start,
        Round.assessment_deadline,
    ]

    column_labels = {"proto_grant.short_name": "Fund", "name_json": "Name", "title_json": "Title"}
    column_filters = ["proto_grant.short_name"]

    column_formatters = {
        "fund_id": lambda v, c, m, p: m.proto_grant.short_name,
        "title_json": lambda v, c, m, p: m.title_json["en"],
    }


class ProtoReportingRoundAdmin(BaseAdmin):
    _model = ProtoReportingRound

    can_create = True
    can_edit = True

    column_list = [
        "grant",
        "reporting_period_starts",
        "reporting_period_ends",
        "submission_period_starts",
        "submission_period_ends",
    ]

    column_formatters = {
        "grant": lambda v, c, m, p: m.grant.short_name,
    }


class DataStandardAdmin(BaseAdmin):
    _model = DataStandard
    can_create = True
    can_edit = True


class TemplateSectionAdmin(BaseAdmin):
    _model = TemplateSection
    can_create = True
    can_edit = True

    column_list = ["type", "slug", "title", "order"]


class TemplateQuestionAdmin(BaseAdmin):
    _model = TemplateQuestion
    can_create = True
    can_edit = True


class DataCollectionSectionAdmin(BaseAdmin):
    _model = ProtoDataCollectionDefinitionSection
    can_create = True
    can_edit = True

    form_excluded_columns = ["created_at", "updated_at", "questions"]

    column_labels = {
        "round": "Round (warning: check value is correct if creating new instance from Design System side)"
    }


class DataCollectionQuestionAdmin(BaseAdmin):
    _model = ProtoDataCollectionDefinitionQuestion
    can_create = True
    can_edit = True

    form_excluded_columns = ["created_at", "updated_at", "template_question"]

    column_labels = {
        "section": "Section (warning: check value is correct if creating new instance from Design System side)"
    }
