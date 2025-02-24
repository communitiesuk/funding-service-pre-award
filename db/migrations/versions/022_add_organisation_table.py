"""add organisation table

Revision ID: 022_add_organisation_table
Revises: 021_add_fund_relationship_on_gra
Create Date: 2025-02-24 11:41:55.937992

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "022_add_organisation_table"
down_revision = "021_add_fund_relationship_on_gra"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "organisation",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("domain", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_organisation")),
    )


def downgrade():
    op.drop_table("organisation")
