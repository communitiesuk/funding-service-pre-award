import pytest
from sqlalchemy.orm import scoped_session, sessionmaker


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


def mock_get_data(endpoint, *args, **kwargs):
    if "/rounds/" in endpoint:
        return {
            "id": "test-round-id",
            "title_json": {"en": "Test Round Name"},
            "fund_id": "test-fund-id",
        }
    else:
        return {
            "name": "Test Fund Name",
            "id": "test-fund-id",
            "short_name": "TEST",
            "description": "Test fund description",
            "welsh_available": False,
            "name_json": {"en": "Test Fund Name"},
            "funding_type": "TEST_TYPE",
        }
