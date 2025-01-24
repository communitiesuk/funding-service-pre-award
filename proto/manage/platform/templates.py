from common.blueprints import Blueprint

templates_blueprint = Blueprint("templates", __name__)


@templates_blueprint.context_processor
def _templates_service_nav():
    return dict(active_navigation_tab="templates")
