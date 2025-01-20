from flask import current_app
from sqlalchemy import update

import fund_store.config.fund_loader_config.night_shelter.ns_r2 as ns_r2
from db import db
from fund_store.db.models.round import Round


def update_rounds_with_links(rounds):
    for round in rounds:
        current_app.logger.warning(
            "\tRound: %(round_short_name)s (%(round_id)s)",
            dict(round_short_name=round["short_name"], round_id=str(round["id"])),
        )
        if round.get("application_guidance"):
            current_app.logger.warning("\t\tUpdating application_guidance")
            stmt = (
                update(Round)
                .where(Round.id == round["id"])
                .values(
                    application_guidance=round["application_guidance"],
                )
            )

            db.session.execute(stmt)
        else:
            current_app.logger.warning("\t\tNo application_guidance defined")
    db.session.commit()


def main() -> None:
    current_app.logger.warning("Updating application_guidance for NSTF R2")
    update_rounds_with_links(ns_r2.round_config)
    current_app.logger.warning("Updates complete")


if __name__ == "__main__":
    from app import create_app

    app = create_app()

    with app.app_context():
        main()
