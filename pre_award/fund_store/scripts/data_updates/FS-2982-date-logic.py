from flask import current_app
from sqlalchemy import update

import pre_award.fund_store.config.fund_loader_config.cof.cof_r2 as cof_r2
import pre_award.fund_store.config.fund_loader_config.cof.cof_r3 as cof_r3
import pre_award.fund_store.config.fund_loader_config.night_shelter.ns_r2 as ns_r2
from pre_award.db import db
from pre_award.fund_store.db.models.round import Round


def update_date_format(round_config):
    current_app.logger.warning("\t\tUpdating date format/ logic for rounds")
    stmt = (
        update(Round)
        .where(Round.id == round_config[0].get("id"))
        .values(
            opens=round_config[0].get("opens"),
            deadline=round_config[0].get("deadline"),
            assessment_deadline=round_config[0].get("assessment_deadline"),
        )
    )
    db.session.execute(stmt)
    db.session.commit()


def main() -> None:
    current_app.logger.warning("Updating date format for NSTF R2, COF R3, COF R2")
    update_date_format(ns_r2.round_config)
    update_date_format(cof_r3.round_config)
    update_date_format(cof_r2.rounds_config)
    current_app.logger.warning("Updates complete")


if __name__ == "__main__":
    from app import create_app

    app = create_app()

    with app.app_context():
        main()
