"""Adds COF R3W3 scoring system to the assesssment_rounds table.

Revision ID: 5c03105a204c
Revises: af78512b644f
Create Date: 2024-01-05 14:34:23.729866

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "5c03105a204c"
down_revision = "af78512b644f"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    connection = op.get_bind()
    insert_query = sa.text(
        "INSERT INTO assessment_round(round_id, scoring_system)VALUES (:uuid, :scoring_system) RETURNING round_id;"
    )

    params = {
        "uuid": "4efc3263-aefe-4071-b5f4-0910abec12d2",
        "scoring_system": "OneToFive",
    }
    connection.execute(insert_query, params)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    connection = op.get_bind()
    delete_query = sa.text("DELETE FROM assessment_round WHERE round_id = :uuid;")
    params = {
        "uuid": "4efc3263-aefe-4071-b5f4-0910abec12d2",
    }
    connection.execute(delete_query, params)
    # ### end Alembic commands ###