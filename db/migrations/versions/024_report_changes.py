"""report changes

Revision ID: 024_report_changes
Revises: 023_account_id_organisation_id
Create Date: 2025-02-24 13:46:37.354978

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "024_report_changes"
down_revision = "023_account_id_organisation_id"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("proto_report", schema=None) as batch_op:
        batch_op.add_column(sa.Column("reporting_round_id", sa.Integer(), nullable=False))
        batch_op.add_column(sa.Column("data_collection_instance_id", sa.Integer(), nullable=False))
        batch_op.drop_constraint("fk_proto_report_round_id_round", type_="foreignkey")
        batch_op.drop_constraint("fk_proto_report_data_collection_id_proto_data_collectio_49b1", type_="foreignkey")
        batch_op.create_foreign_key(
            batch_op.f("fk_proto_report_data_collection_instance_id_proto_data_collection_instance"),
            "proto_data_collection_instance",
            ["data_collection_instance_id"],
            ["id"],
        )
        batch_op.create_foreign_key(
            batch_op.f("fk_proto_report_reporting_round_id_proto_reporting_round"),
            "proto_reporting_round",
            ["reporting_round_id"],
            ["id"],
        )
        batch_op.drop_column("data_collection_id")
        batch_op.drop_column("round_id")


def downgrade():
    with op.batch_alter_table("proto_report", schema=None) as batch_op:
        batch_op.add_column(sa.Column("round_id", sa.UUID(), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column("data_collection_id", sa.INTEGER(), autoincrement=False, nullable=False))
        batch_op.drop_constraint(
            batch_op.f("fk_proto_report_reporting_round_id_proto_reporting_round"), type_="foreignkey"
        )
        batch_op.drop_constraint(
            batch_op.f("fk_proto_report_data_collection_instance_id_proto_data_collection_instance"), type_="foreignkey"
        )
        batch_op.create_foreign_key(
            "fk_proto_report_data_collection_id_proto_data_collectio_49b1",
            "proto_data_collection_instance",
            ["data_collection_id"],
            ["id"],
        )
        batch_op.create_foreign_key("fk_proto_report_round_id_round", "round", ["round_id"], ["id"])
        batch_op.drop_column("data_collection_instance_id")
        batch_op.drop_column("reporting_round_id")
