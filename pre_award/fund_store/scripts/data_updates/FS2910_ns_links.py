from flask import current_app
from sqlalchemy import update

import pre_award.fund_store.config.fund_loader_config.night_shelter.ns_r2 as ns_r2
from data.models import Round
from pre_award.db import db


def update_rounds_with_links(rounds):
    for round in rounds:
        current_app.logger.warning(
            "\tRound: %(round_short_name)s (%(round_id)s)",
            dict(round_short_name=round["short_name"], round_id=str(round["id"])),
        )
        if round.get("prospectus") and round.get("privacy_notice"):
            current_app.logger.warning("\t\tUpdating prospectus and privacy notice")
            stmt = (
                update(Round)
                .where(Round.id == round["id"])
                .values(
                    prospectus=round["prospectus"],
                    privacy_notice=round["privacy_notice"],
                )
            )

            db.session.execute(stmt)
        else:
            current_app.logger.warning("\t\tNo links defined")
    db.session.commit()


def main() -> None:
    current_app.logger.warning("Updating prospectus and privacy links for NSTF R2")
    update_rounds_with_links(ns_r2.round_config)
    current_app.logger.warning("Updates complete")


if __name__ == "__main__":
    from app import create_app

    app = create_app()

    with app.app_context():
        main()
