from flask_admin.menu import MenuLink

from proto.manage.admin.entities import (
    DataCollectionQuestionAdmin,
    DataCollectionSectionAdmin,
    DataStandardAdmin,
    FundAdmin,
    ProtoReportingRoundAdmin,
    RoundAdmin,
    TemplateQuestionAdmin,
    TemplateSectionAdmin,
)


def register_admin_views(flask_admin, db):
    flask_admin.add_view(FundAdmin(db.session))
    flask_admin.add_view(RoundAdmin(db.session))
    flask_admin.add_view(ProtoReportingRoundAdmin(db.session))
    flask_admin.add_view(DataStandardAdmin(db.session, category="Templates"))
    flask_admin.add_view(TemplateSectionAdmin(db.session, category="Templates"))
    flask_admin.add_view(TemplateQuestionAdmin(db.session, category="Templates"))
    flask_admin.add_view(DataCollectionSectionAdmin(db.session, category="Applications"))
    flask_admin.add_view(DataCollectionQuestionAdmin(db.session, category="Applications"))

    # fixme: boo hardcoding - but need an app context/request context/extra stuff to use url_for.
    flask_admin.add_link(MenuLink(name="← Back to Grant management", url="/grant-management"))
