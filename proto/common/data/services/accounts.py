from db import db
from proto.common.data.models.account import Account


def get_account(id):
    account = db.session.get(Account, id)
    return account
