"""reporting rounds

Revision ID: 011_reporting_rounds
Revises: 010_re_run_proto_migration
Create Date: 2025-01-24 20:40:46.271536

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "011_reporting_rounds"
down_revision = "010_re_run_proto_migration"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "proto_reporting_round",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("external_id", sa.Uuid(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("preview", sa.Boolean(), nullable=False),
        sa.Column("reporting_period_starts", sa.DateTime(), nullable=False),
        sa.Column("reporting_period_ends", sa.DateTime(), nullable=False),
        sa.Column("submission_period_starts", sa.DateTime(), nullable=False),
        sa.Column("submission_period_ends", sa.DateTime(), nullable=False),
        sa.Column("grant_id", sa.UUID(), nullable=False),
        sa.Column("data_collection_definition_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["data_collection_definition_id"],
            ["proto_data_collection_definition.id"],
            name=op.f("fk_proto_reporting_round_data_collection_definition_id_proto_data_collection_definition"),
        ),
        sa.ForeignKeyConstraint(["grant_id"], ["fund.id"], name=op.f("fk_proto_reporting_round_grant_id_fund")),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_proto_reporting_round")),
    )
    with op.batch_alter_table("proto_reporting_round", schema=None) as batch_op:
        batch_op.create_index(batch_op.f("ix_proto_reporting_round_external_id"), ["external_id"], unique=False)
        batch_op.create_index(
            "only_one_preview_round", ["preview"], unique=True, postgresql_where=sa.text("preview IS true")
        )


def downgrade():
    with op.batch_alter_table("proto_reporting_round", schema=None) as batch_op:
        batch_op.drop_index("only_one_preview_round", postgresql_where=sa.text("preview IS true"))
        batch_op.drop_index(batch_op.f("ix_proto_reporting_round_external_id"))

    op.drop_table("proto_reporting_round")
