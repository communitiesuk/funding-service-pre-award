"""add fund relationship on grant recipient

Revision ID: 021_add_fund_relationship_on_gra
Revises: 020_add_some_grant_recipient_inf
Create Date: 2025-02-21 17:34:02.812899

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "021_add_fund_relationship_on_gra"
down_revision = "020_add_some_grant_recipient_inf"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("proto_grant_recipient", schema=None) as batch_op:
        batch_op.add_column(sa.Column("grant_id", sa.UUID(), nullable=False))
        batch_op.create_foreign_key(batch_op.f("fk_proto_grant_recipient_grant_id_fund"), "fund", ["grant_id"], ["id"])


def downgrade():
    with op.batch_alter_table("proto_grant_recipient", schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f("fk_proto_grant_recipient_grant_id_fund"), type_="foreignkey")
        batch_op.drop_column("grant_id")
