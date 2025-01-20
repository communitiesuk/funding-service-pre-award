from datetime import datetime
from secrets import token_urlsafe

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert as postgres_insert

from db import db
from proto.common.data.models.account import Account
from proto.common.data.models.magic_link import MagicLink


def get_magic_link(token):
    # ideally this should return one_or_none() and have the problem handled upstream but just setting to
    # meaningfully error during the proto
    magic_link = db.session.scalars(
        select(MagicLink).filter(
            MagicLink.expires_date >= datetime.now(), MagicLink.token == token, MagicLink.used == False
        )
    ).one()
    return magic_link


# could have the original method overloaded to allow id or token and conditionally filtering but separating it out for now as you
# wouldn't want to return one up accidentally
def get_magic_link_by_id(id):
    magic_link = db.session.get(MagicLink, id)
    return magic_link


# don't really like the idea of passing in fully formed db models just to be acted no but happy to work out how this interface feels nice
# and easy to test
def claim_magic_link(magic_link: MagicLink):
    magic_link.used = True
    # account = Account(email=magic_link.email, is_magic_link=True)
    # if this doesn't let us do upsert then it would have to be a prepared `insert` statement with on conflict described, which hopefully could be added to the session
    # look at https://github.com/sqlalchemy/sqlalchemy/discussions/9675#discussioncomment-5673326 for being able to do this in the ORM style class objects - would much prefer to do that but
    # it doesn't look like its been around for very long
    # for now just prepare the statement in postgres specific statements (the reason for it not being long-supported)
    stmt = (
        postgres_insert(Account)
        .values(email=magic_link.email, is_magic_link=True)
        .on_conflict_do_nothing()
        .returning(Account.id, Account.email)
    )
    # account_result = db.session.execute(stmt)
    db.session.execute(stmt)

    # db.session.add(account)
    db.session.commit()

    # this is a wasted extra statement but I can't be bothered to look into why going through the id, email tuple above isn't working as I'd expect
    account = db.session.scalars(select(Account).filter(Account.email == magic_link.email)).one()
    return account


def create_magic_link(email, path):
    # don't have the beans to think through all the guarantees/ potential salts/ hashses you might want to use
    # for now if the email has the token which is in the db thats good enough
    token = token_urlsafe(24)
    magic_link = MagicLink(email=email, token=token, path=path)
    db.session.add(magic_link)
    db.session.commit()
    return magic_link
