"""add applications_retained_count to pii_deletion_log

Records how many applications were intentionally retained (excluded) during a PII deletion run, so
the audit trail is honest about partial-retention deletions (e.g. keeping a successful applicant).

Revision ID: 024_add_retained_count_to_pii_log
Revises: 023_add_submitted_value
Create Date: 2026-06-29 00:00:00.000000
"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "024_add_retained_count_to_pii_log"
down_revision = "023_add_submitted_value"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("pii_deletion_log", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                "applications_retained_count",
                sa.Integer(),
                nullable=False,
                server_default="0",
            )
        )


def downgrade():
    with op.batch_alter_table("pii_deletion_log", schema=None) as batch_op:
        batch_op.drop_column("applications_retained_count")
