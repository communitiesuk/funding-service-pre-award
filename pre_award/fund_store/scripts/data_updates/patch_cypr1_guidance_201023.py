from flask import current_app
from sqlalchemy import update

import fund_store.config.fund_loader_config.cyp.cyp_r1 as cyp_r1
from db import db
from fund_store.db.models.round import Round


def update_round_guidance(round_config):
    current_app.logger.info(
        "Round: %(round_short_name)s, id: %(round_id)s",
        dict(
            round_short_name=round_config["short_name"],
            round_id=str(round_config["id"]),
        ),
    )
    current_app.logger.info("\t\tUpdating round guidance")
    stmt = update(Round).where(Round.id == round_config["id"]).values(guidance_url=round_config["guidance_url"])

    db.session.execute(stmt)
    db.session.commit()


def main() -> None:
    current_app.logger.info("Updating guidance url for CYP R1")
    update_round_guidance(cyp_r1.round_config[0])
    current_app.logger.info("Updates complete")


if __name__ == "__main__":
    from app import create_app

    app = create_app()

    with app.app_context():
        main()
