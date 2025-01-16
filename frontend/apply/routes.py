from flask import render_template

from pre_award.common.blueprints import Blueprint

apply_bp = Blueprint("apply_routes", __name__, template_folder="templates")


@apply_bp.route("/monolith")
def landing_page():
    return render_template("apply/landing-mono.html.jinja")
