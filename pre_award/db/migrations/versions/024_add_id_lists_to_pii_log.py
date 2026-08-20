import sqlalchemy as sa
from alembic import op

revision = "024_add_id_lists_to_pii_log"
down_revision = "023_add_submitted_value"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("pii_deletion_log", schema=None) as batch_op:
        batch_op.add_column(sa.Column("deleted_application_ids", sa.JSON(), nullable=False, server_default="[]"))
        batch_op.add_column(sa.Column("retained_application_ids", sa.JSON(), nullable=False, server_default="[]"))
        batch_op.add_column(sa.Column("failed_application_ids", sa.JSON(), nullable=False, server_default="[]"))


def downgrade():
    with op.batch_alter_table("pii_deletion_log", schema=None) as batch_op:
        batch_op.drop_column("failed_application_ids")
        batch_op.drop_column("retained_application_ids")
        batch_op.drop_column("deleted_application_ids")
