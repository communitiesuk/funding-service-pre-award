"""add some grant recipient info

Revision ID: 020_add_some_grant_recipient_inf
Revises: 019_validations_from_template
Create Date: 2025-02-21 15:08:35.589367

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "020_add_some_grant_recipient_inf"
down_revision = "019_validations_from_template"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("proto_grant_recipient", schema=None) as batch_op:
        batch_op.add_column(sa.Column("funding_allocated", sa.Integer(), nullable=False))
        batch_op.add_column(sa.Column("funding_paid", sa.Integer(), nullable=False))


def downgrade():
    with op.batch_alter_table("proto_grant_recipient", schema=None) as batch_op:
        batch_op.drop_column("funding_paid")
        batch_op.drop_column("funding_allocated")
