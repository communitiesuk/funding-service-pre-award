"""report tables

Revision ID: 020_report_tables
Revises: 019_generic_data_collection_tabl
Create Date: 2025-01-23 22:05:24.030157

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "020_report_tables"
down_revision = "019_generic_data_collection_tabl"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "proto_report",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("code", sa.String(), nullable=False),
        sa.Column("fake", sa.Boolean(), nullable=False),
        sa.Column("round_id", sa.UUID(), nullable=False),
        sa.Column("account_id", sa.UUID(), nullable=False),
        sa.Column("data_collection_id", sa.Integer(), nullable=False),
        sa.Column("updated_by_reporter_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["account_id"], ["account.id"], name=op.f("fk_proto_report_account_id_account")),
        sa.ForeignKeyConstraint(
            ["data_collection_id"],
            ["proto_data_collection.id"],
            name=op.f("fk_proto_report_data_collection_id_proto_data_collection"),
        ),
        sa.ForeignKeyConstraint(["round_id"], ["round.id"], name=op.f("fk_proto_report_round_id_round")),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_proto_report")),
    )


def downgrade():
    op.drop_table("proto_report")
