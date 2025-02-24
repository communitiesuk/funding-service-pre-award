"""account_id->organisation_id

Revision ID: 023_account_id_organisation_id
Revises: 022_add_organisation_table
Create Date: 2025-02-24 11:49:21.486733

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "023_account_id_organisation_id"
down_revision = "022_add_organisation_table"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("account", schema=None) as batch_op:
        batch_op.add_column(sa.Column("organisation_id", sa.Uuid(), nullable=False))
        batch_op.create_foreign_key(
            batch_op.f("fk_account_organisation_id_organisation"), "organisation", ["organisation_id"], ["id"]
        )

    with op.batch_alter_table("proto_application", schema=None) as batch_op:
        batch_op.add_column(sa.Column("organisation_id", sa.Uuid(), nullable=False))
        batch_op.drop_constraint("fk_proto_application_account_id_account", type_="foreignkey")
        batch_op.create_foreign_key(
            batch_op.f("fk_proto_application_organisation_id_organisation"), "organisation", ["organisation_id"], ["id"]
        )
        batch_op.drop_column("account_id")

    with op.batch_alter_table("proto_grant_recipient", schema=None) as batch_op:
        batch_op.add_column(sa.Column("organisation_id", sa.Uuid(), nullable=False))
        batch_op.create_foreign_key(
            batch_op.f("fk_proto_grant_recipient_organisation_id_organisation"),
            "organisation",
            ["organisation_id"],
            ["id"],
        )

    with op.batch_alter_table("proto_report", schema=None) as batch_op:
        batch_op.add_column(sa.Column("organisation_id", sa.Uuid(), nullable=False))
        batch_op.drop_constraint("fk_proto_report_account_id_account", type_="foreignkey")
        batch_op.create_foreign_key(
            batch_op.f("fk_proto_report_organisation_id_organisation"), "organisation", ["organisation_id"], ["id"]
        )
        batch_op.drop_column("account_id")


def downgrade():
    with op.batch_alter_table("proto_report", schema=None) as batch_op:
        batch_op.add_column(sa.Column("account_id", sa.UUID(), autoincrement=False, nullable=False))
        batch_op.drop_constraint(batch_op.f("fk_proto_report_organisation_id_organisation"), type_="foreignkey")
        batch_op.create_foreign_key("fk_proto_report_account_id_account", "account", ["account_id"], ["id"])
        batch_op.drop_column("organisation_id")

    with op.batch_alter_table("proto_grant_recipient", schema=None) as batch_op:
        batch_op.drop_constraint(
            batch_op.f("fk_proto_grant_recipient_organisation_id_organisation"), type_="foreignkey"
        )
        batch_op.drop_column("organisation_id")

    with op.batch_alter_table("proto_application", schema=None) as batch_op:
        batch_op.add_column(sa.Column("account_id", sa.UUID(), autoincrement=False, nullable=False))
        batch_op.drop_constraint(batch_op.f("fk_proto_application_organisation_id_organisation"), type_="foreignkey")
        batch_op.create_foreign_key("fk_proto_application_account_id_account", "account", ["account_id"], ["id"])
        batch_op.drop_column("organisation_id")

    with op.batch_alter_table("account", schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f("fk_account_organisation_id_organisation"), type_="foreignkey")
        batch_op.drop_column("organisation_id")
