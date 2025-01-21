from sqlalchemy import select

from db import db
from proto.common.data.models.applications import Applications
from proto.common.data.models.fund import Fund
from proto.common.data.models.round import Round


# for apply we'll limit by the account accessing (or their email domain or their guest lists depending on how far we go with that)
# for assess we'll limit by the fund the user has permissions for
# tbd if those are the same overloaded method or multiple
def get_applications(account_id):
    applications = db.session.scalars(select(Applications).filter(Applications.account_id == account_id)).all()
    return applications


# should the page to list applications filter to a specific round or should it just show all applications
# across that fund?
# it's likely there's a need to give some assessors permissions for speicific rounds of funding so making it default
# to the whole grant by default might be problematic for that (although likely only COF or DPIF thats ever gotten near that many rounds)
def search_applications(short_code):
    # could prove the concept that competitive funds should only get applications from SUBMITTED onwards
    # vs. uncompeted funds which could just show all applications
    # comes back to the question of it there are meaningful assessment and application statuses outside of in progress and success/ failure
    applications = db.session.scalars(
        select(Applications).join(Round).join(Fund).filter(Fund.short_name == short_code)
    ).all()
    return applications
