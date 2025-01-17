import os

from invoke import Context

from assessment_store.tasks.db_tasks import seed_assessment_store_db


def main():
    """
    Script to seed the assessment store database.
    Detects the environment and seeds accordingly.
    """
    environment = os.getenv("FLASK_ENV", "local")
    print(f"Running seeding script for environment: {environment}")

    ctx = Context()
    seed_assessment_store_db(ctx, environment=environment)


if __name__ == "__main__":
    main()
