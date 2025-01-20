from flask import current_app
from sqlalchemy import update

import fund_store.config.fund_loader_config.digital_planning.dpi_r2 as dpi_r2
from db import db
from fund_store.db.models.round import Round


def update_rounds_with_links(rounds):
    for round in rounds:
        current_app.logger.warning(
            "\tRound: %(round_short_name)s (%(round_id)s)",
            dict(round_short_name=round["short_name"], round_id=str(round["id"])),
        )
        if round.get("guidance_url"):
            current_app.logger.warning("\t\tUpdating guidance_url")
            stmt = (
                update(Round)
                .where(Round.id == round["id"])
                .values(
                    guidance_url=round["guidance_url"],
                )
            )

            db.session.execute(stmt)
        else:
            current_app.logger.warning("\t\tNo guidance_url defined")
    db.session.commit()


def main() -> None:
    current_app.logger.warning("Updating guidance_url for DPIF R2")
    update_rounds_with_links(dpi_r2.round_config)
    current_app.logger.warning("Updates complete")


if __name__ == "__main__":
    from app import create_app

    app = create_app()

    with app.app_context():
        main()
