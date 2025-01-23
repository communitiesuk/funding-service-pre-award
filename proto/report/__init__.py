from flask import render_template

from common.blueprints import Blueprint
from proto.common.auth import is_authenticated

report_blueprint = Blueprint("proto_report", __name__)


@report_blueprint.get("/report")
@report_blueprint.get("/report/")
@is_authenticated
def report_index():
    return render_template("report/index.html")
