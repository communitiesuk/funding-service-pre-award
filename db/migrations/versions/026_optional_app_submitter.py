"""optional app submitter

Revision ID: 026_optional_app_submitter
Revises: 025_application_record_submitter
Create Date: 2025-02-24 17:17:43.675070

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "026_optional_app_submitter"
down_revision = "025_application_record_submitter"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("proto_application", schema=None) as batch_op:
        batch_op.alter_column("submitted_by_id", existing_type=sa.UUID(), nullable=True)


def downgrade():
    with op.batch_alter_table("proto_application", schema=None) as batch_op:
        batch_op.alter_column("submitted_by_id", existing_type=sa.UUID(), nullable=False)
