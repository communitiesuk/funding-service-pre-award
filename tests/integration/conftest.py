from multiprocessing import Process

import pytest
from flask_migrate import upgrade
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy_utils import create_database, database_exists


@pytest.fixture(scope="session")
def db(app, _db):
    with app.app_context():
        no_db = not database_exists(app.config["SQLALCHEMY_DATABASE_URI"])

        if no_db:
            create_database(app.config["SQLALCHEMY_DATABASE_URI"])

        # Run alembic migrations. We do this is a separate python process because it loads and executes a bunch
        # of code from db/migrations/env.py. This does things like set up loggers, which interferes with the
        # `caplog` fixture, and possibly has some other unexpected side effects.
        proc = Process(target=upgrade)
        proc.start()
        proc.join()

        yield _db


@pytest.fixture(scope="function", autouse=True)
def session(db):
    # Keep a reference to the original db session because the old-school pre_award tests instrument the test DB
    # using utils, which works differently (doesn't have transaction-based test isolation).
    old_session = db.session

    connection = db.engine.connect()
    transaction = connection.begin()

    db.session = session = scoped_session(
        session_factory=sessionmaker(bind=connection, join_transaction_mode="create_savepoint")
    )

    try:
        yield session
    finally:
        session.remove()
        transaction.rollback()
        connection.close()

    db.session = old_session
