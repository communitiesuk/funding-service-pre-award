# move this when cherry picking commit to bring account model in
from account_store.db.models.account import Account
from db import db


def get_account(id):
    account = db.session.get(Account, id)
    return account
