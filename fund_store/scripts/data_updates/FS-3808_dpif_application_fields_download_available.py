from flask import current_app
from sqlalchemy import update

import fund_store.config.fund_loader_config.digital_planning.dpi_r2 as dpi_r2
from db import db
from fund_store.db.models.round import Round


def update_application_fields_download_available(rounds):
    for round in rounds:
        current_app.logger.warning(
            "\tRound: %(round_short_name)s (%(round_id)s)",
            dict(round_short_name=round["short_name"], round_id=str(round["id"])),
        )
        if round.get("application_fields_download_available"):
            current_app.logger.warning("\t\tUpdating application_fields_download_available")
            stmt = (
                update(Round)
                .where(Round.id == round["id"])
                .values(
                    application_fields_download_available=round["application_fields_download_available"],
                )
            )

            db.session.execute(stmt)
        else:
            current_app.logger.warning("\t\tNo application_fields_download_available defined")
    db.session.commit()


def main() -> None:
    current_app.logger.warning("Updating application_fields_download_available for DPIF R2")
    update_application_fields_download_available(dpi_r2.round_config)
    current_app.logger.warning("Updates complete")


if __name__ == "__main__":
    from app import create_app

    app = create_app()

    with app.app_context():
        main()
