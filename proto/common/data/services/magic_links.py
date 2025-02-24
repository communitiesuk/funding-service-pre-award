from datetime import datetime
from secrets import token_urlsafe

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert as postgres_insert

# move this to proto when cherry picking the commit that did that on the other branch
from account_store.db.models.account import Account
from db import db
from proto.common.data.models import Organisation
from proto.common.data.models.magic_link import MagicLink


def get_magic_link(token):
    magic_link = db.session.scalars(
        select(MagicLink).filter(
            MagicLink.expires_date >= datetime.now(),
            MagicLink.token == token,
            MagicLink.used == False,  # noqa
        )
    ).one()
    return magic_link


def get_magic_link_by_id(id):
    magic_link = db.session.get(MagicLink, id)
    return magic_link


def claim_magic_link(magic_link: MagicLink):
    magic_link.used = True

    domain = magic_link.email.split("@")[1]  # shortcut
    org = db.session.scalar(select(Organisation).where(Organisation.domain == domain))
    if not org:
        org_name = domain.split(".")[0].title() + " Council"
        org = Organisation(name=org_name, domain=domain)
        db.session.add(org)
        db.session.flush()

    # postgres specific statement - there is as of quite recently an ORM way of doing this but it looked
    # like work and probably needs a newer lib
    stmt = (
        postgres_insert(Account)
        .values(email=magic_link.email, is_magic_link=True, organisation_id=org.id)
        .on_conflict_do_nothing()
        .returning(Account.id, Account.email)
    )
    db.session.execute(stmt)
    db.session.commit()

    # this is a wasted extra statement but I can't be bothered to look into why returning through id, email
    # tuple above isn't working as I'd expect
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
