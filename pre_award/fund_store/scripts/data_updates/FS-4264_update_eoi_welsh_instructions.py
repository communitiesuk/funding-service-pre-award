from flask import current_app
from sqlalchemy import update

import pre_award.fund_store.config.fund_loader_config.cof.eoi as eoi
from pre_award.db import db
from services.data.models.round import Round


def update_rounds_with_links(round_config):
    current_app.logger.warning(
        "\tRound: %(round_short_name)s (%(round_id)s)",
        dict(
            round_short_name=round_config[0]["short_name"],
            round_id=str(round_config[0]["id"]),
        ),
    )
    current_app.logger.warning("\t\tUpdating instructions & application_guidance")
    stmt = (
        update(Round)
        .where(Round.id == round_config[0]["id"])
        .values(
            instructions_json=round_config[0]["instructions_json"],
            application_guidance_json=round_config[0]["application_guidance_json"],
        )
    )

    db.session.execute(stmt)
    db.session.commit()


def main() -> None:
    current_app.logger.warning("Updating instructions & application_guidance for EOI")
    update_rounds_with_links(eoi.round_config_eoi)
    current_app.logger.warning("Updates complete")


if __name__ == "__main__":
    from app import create_app

    app = create_app()

    with app.app_context():
        main()
