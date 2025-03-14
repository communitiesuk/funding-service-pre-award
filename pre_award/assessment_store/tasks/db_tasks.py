import inspect
import sys
from typing import Literal

sys.path.insert(1, ".")

from invoke import task  # noqa:E402

from app import create_app  # noqa:E402
from pre_award.assessment_store.tasks.helper_tasks import (  # noqa:E402
    _echo_input,  # noqa:E402
    _echo_print,  # noqa:E402
    _env_var,  # noqa:E402
)

# Needed for invoke to work on python3.11
# Remove once invoke has been updated.
if not hasattr(inspect, "getargspec"):
    inspect.getargspec = inspect.getfullargspec


@task
def bootstrap_dev_db(c):
    """Create a clean database for development.

    Unit testing makes a seperate db.

    """

    from sqlalchemy_utils.functions import create_database, database_exists

    with _env_var("FLASK_ENV", "development"):
        app = create_app()
        with app.app_context():
            from pre_award.config import Config

            if database_exists(Config.SQLALCHEMY_DATABASE_URI):
                _echo_print("Existing database found!\n")

            else:
                _echo_print(
                    f"{Config.SQLALCHEMY_DATABASE_URI} not found...",
                )
                create_database(Config.SQLALCHEMY_DATABASE_URI)
                _echo_print(
                    f"{Config.SQLALCHEMY_DATABASE_URI} db created...",
                )


@task
def generate_test_data(c):
    import json

    from tests.pre_award.assessment_store_tests._db_seed_data import get_dynamic_rows

    _echo_print("Generating data.")
    rows = [json.loads(row) for row in get_dynamic_rows(3, 3, 10)]

    _echo_print("Writing data to apps.json")
    with open("apps.json", "w") as f:
        json.dump(rows, f, indent=4)


@task(
    help={
        "fundround": "The round and fund to seed applications for assessment.",
        "appcount": "The amount of applications to seed.",
    }
)
def seed_dev_db(c, fundround=None, appcount=None):
    """Uses the `tests.conftest.seed_database` function to insert test data into
    your dev database."""
    from flask_migrate import upgrade

    with _env_var("FLASK_ENV", "development"):
        app = create_app()
        with app.app_context():
            from pre_award.assessment_store.config.mappings.assessment_mapping_fund_round import (
                fund_round_mapping_config,
            )
            from pre_award.config import Config
            from tests.pre_award.assessment_store_tests._helpers import seed_database_for_fund_round

            choosing = not bool(fundround and appcount)
            if not choosing:
                fund_round = fund_round_mapping_config[fundround]
                apps = int(appcount)
                print(f"Seeding {apps} applications for fund_round: '{fundround}'")

            while choosing:
                new_line = "\n"
                fundround = str(
                    _echo_input(
                        "Please type the fund-round to seed:"
                        f"\nfund-rounds available to seed: "
                        f"{new_line} - {f' {new_line} - '.join(fund_round_mapping_config.keys())}"
                        f"{new_line} > "
                    ),
                )
                fund_round = fund_round_mapping_config[fundround]
                apps = int(_echo_input("How many applications?{new_line} > "))
                choosing = (
                    not _echo_input(f"Would you like to insert {apps} applications for {fundround}? y/n \n").lower()
                    == "y"
                )

            _echo_print(
                f"Running migrations on db {Config.SQLALCHEMY_DATABASE_URI}.",
            )

            upgrade()

            _echo_print(f"Seeding db {Config.SQLALCHEMY_DATABASE_URI} with {apps} test rows.")
            seed_database_for_fund_round(apps, {fundround: fund_round})

            _echo_print(f"Seeding db {Config.SQLALCHEMY_DATABASE_URI} complete.")


@task
def create_seeded_db(c):
    """Creates and seeds a database for local development."""

    bootstrap_dev_db(c)
    seed_dev_db(c)


def seed_assessment_store_db_impl(environment: Literal["local", "cloud"]):
    import uuid

    from data.models import Round
    from pre_award.assessment_store.db.models.score import AssessmentRound, ScoringSystem
    from pre_award.assessment_store.db.models.tag import TagType
    from pre_award.db import db

    # Define scoring systems
    scoring_system_data = [
        {
            "id": str(uuid.uuid4()),
            "scoring_system_name": "OneToFive",
            "minimum_score": 1,
            "maximum_score": 5,
        },
        {
            "id": str(uuid.uuid4()),
            "scoring_system_name": "ZeroToThree",
            "minimum_score": 0,
            "maximum_score": 3,
        },
        {
            "id": str(uuid.uuid4()),
            "scoring_system_name": "ZeroToFour",
            "minimum_score": 0,
            "maximum_score": 4,
        },
        {
            "id": str(uuid.uuid4()),
            "scoring_system_name": "ZeroToOne",
            "minimum_score": 0,
            "maximum_score": 1,
        },
    ]

    # Fetch existing scoring systems
    existing_systems = {system.scoring_system_name.name: system.id for system in db.session.query(ScoringSystem).all()}

    # Add missing scoring systems
    new_systems_added = False
    for scoring_system in scoring_system_data:
        name = scoring_system["scoring_system_name"]
        if name not in existing_systems:
            db.session.add(ScoringSystem(**scoring_system))
            _echo_print(f"Added new scoring system: {name}")
            new_systems_added = True
        else:
            scoring_system["id"] = existing_systems[name]  # Reuse existing ID

    if new_systems_added:
        db.session.commit()
    else:
        _echo_print("No new scoring systems were added.")

    # Associate scoring systems with all rounds
    round_ids = db.session.query(Round).with_entities(Round.id).all()
    for (round_id,) in round_ids:
        db.session.merge(AssessmentRound(round_id=round_id, scoring_system_id=scoring_system_data[0]["id"]))
        _echo_print(f"Associated scoring system ID {scoring_system_data[0]['id']} with round ID {round_id}")

    print(f"Seeded DB with scoring system and assessment round data in {environment} environment.")

    # Define tag types
    tag_types_data = [
        TagType(
            id=str(uuid.uuid4()),
            purpose="GENERAL",
            description="Use to categorise projects, such as by organisation or location",
        ),
        TagType(
            id=str(uuid.uuid4()),
            purpose="PEOPLE",
            description="Use these tags to assign assessments to team members. "
            "Note you cannot send notifications using tags",
        ),
        TagType(
            id=str(uuid.uuid4()),
            purpose="POSITIVE",
            description="Use to indicate that a project has passed an assessment stage or is recommended",
        ),
        TagType(
            id=str(uuid.uuid4()),
            purpose="NEGATIVE",
            description="Use to indicate that a project has failed an assessment stage or is not recommended",
        ),
        TagType(
            id=str(uuid.uuid4()),
            purpose="ACTION",
            description="Use to recommend an action, such as further discussion",
        ),
    ]

    for tag_type in tag_types_data:
        existing_tag_type = db.session.query(TagType).where(TagType.purpose == tag_type.purpose).one_or_none()
        if not existing_tag_type:
            db.session.add(tag_type)
    db.session.commit()
    _echo_print("Seeded DB with tag type data")


@task
def seed_assessment_store_db(c, environment="local"):
    """
    Seeds the assessment store database with required data.

    Parameters:
    - environment: Specify the environment ("local" or "cloud").
    """
    flask_env = "development" if environment == "local" else "production"
    with _env_var("FLASK_ENV", flask_env):
        app = create_app()
        with app.app_context():
            seed_assessment_store_db_impl(environment=environment)
