from sqlalchemy import select

from db import db
from proto.common.data.models.applications import Applications


# for apply we'll limit by the account accessing (or their email domain or their guest lists depending on how far we go with that)
# for assess we'll limit by the fund the user has permissions for
# tbd if those are the same overloaded method or multiple
def get_applications(account_id):
    applications = db.session.scalars(select(Applications).filter(Applications.account_id == account_id)).all()
    return applications
