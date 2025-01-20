from datetime import datetime
from secrets import token_urlsafe

from sqlalchemy import select

from db import db
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
def set_used(magic_link: MagicLink):
    magic_link.used = True
    db.session.commit()
    return magic_link


def create_magic_link(email, path):
    # don't have the beans to think through all the guarantees/ potential salts/ hashses you might want to use
    # for now if the email has the token which is in the db thats good enough
    token = token_urlsafe(24)
    magic_link = MagicLink(email=email, token=token, path=path)
    db.session.add(magic_link)
    db.session.commit()
    return magic_link
