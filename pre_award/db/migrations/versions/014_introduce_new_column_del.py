"""Introduse newcolumn for soft delete applications but hard delete user inputs

Revision ID: 014_introduse_newcolumn_for_soft
Revises: 013_add_zerotofour_scoringsystem
Create Date: 2025-08-11 10:36:09.020749

"""

import sqlalchemy as sa
from alembic import op

revision = "014_introduce_new_column_del"
down_revision = "013_add_zerotofour_scoringsystem"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("applications", schema=None) as batch_op:
        batch_op.add_column(sa.Column("is_deleted", sa.Boolean(), nullable=False, server_default=sa.text("false")))

    with op.batch_alter_table("assessment_records", schema=None) as batch_op:
        batch_op.add_column(sa.Column("is_deleted", sa.Boolean(), nullable=False, server_default=sa.text("false")))


def downgrade():
    with op.batch_alter_table("assessment_records", schema=None) as batch_op:
        batch_op.drop_column("is_deleted")

    with op.batch_alter_table("applications", schema=None) as batch_op:
        batch_op.drop_column("is_deleted")
