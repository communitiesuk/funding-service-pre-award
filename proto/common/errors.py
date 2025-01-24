from flask import render_template


def errorhandler_403(error):
    return render_template("common/403.html"), 403
