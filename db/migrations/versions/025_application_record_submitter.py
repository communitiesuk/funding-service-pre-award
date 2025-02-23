"""application record submitter

Revision ID: 025_application_record_submitter
Revises: 024_report_changes
Create Date: 2025-02-24 16:11:44.087846

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "025_application_record_submitter"
down_revision = "024_report_changes"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("proto_application", schema=None) as batch_op:
        batch_op.add_column(sa.Column("submitted_by_id", sa.UUID(), nullable=False))
        batch_op.create_foreign_key(
            batch_op.f("fk_proto_application_submitted_by_id_account"), "account", ["submitted_by_id"], ["id"]
        )


def downgrade():
    with op.batch_alter_table("proto_application", schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f("fk_proto_application_submitted_by_id_account"), type_="foreignkey")
        batch_op.drop_column("submitted_by_id")
