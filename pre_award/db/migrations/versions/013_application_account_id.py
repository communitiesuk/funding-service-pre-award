"""application account id

Revision ID: 013_application_account_id
Revises: 012_change_short_codes_to_citext
Create Date: 2025-02-11 12:07:25.374462

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "013_application_account_id"
down_revision = "012_change_short_codes_to_citext"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("applications", schema=None) as batch_op:
        batch_op.alter_column(
            "account_id",
            existing_type=sa.VARCHAR(),
            type_=sa.UUID(),
            postgresql_using="account_id::uuid",
            existing_nullable=False,
        )
        batch_op.create_foreign_key(batch_op.f("fk_applications_account_id_account"), "account", ["account_id"], ["id"])


def downgrade():
    with op.batch_alter_table("applications", schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f("fk_applications_account_id_account"), type_="foreignkey")
        batch_op.alter_column("account_id", existing_type=sa.UUID(), type_=sa.VARCHAR(), existing_nullable=False)
