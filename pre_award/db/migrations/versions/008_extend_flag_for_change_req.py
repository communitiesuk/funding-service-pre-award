"""Extends the assessment_flag table with two columns needed to allow change request functionality

Revision ID: "008_extend_flag_for_change_req"
Revises: "007_create_account_store"
Create Date: 2024-12-06 11:30:37.346479

"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "008_extend_flag_for_change_req"
down_revision = "007_create_account_store"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("assessment_flag", schema=None) as batch_op:
        batch_op.add_column(sa.Column("field_ids", postgresql.ARRAY(sa.String(length=256)), nullable=True))
        batch_op.add_column(sa.Column("is_change_request", sa.Boolean(), nullable=True))


def downgrade():
    with op.batch_alter_table("assessment_flag", schema=None) as batch_op:
        batch_op.drop_column("is_change_request")
        batch_op.drop_column("field_ids")
