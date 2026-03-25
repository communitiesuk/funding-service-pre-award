from alembic import op

# revision identifiers, used by Alembic.
revision = "023_add_submitted_value"
down_revision = "022_change_pii_deletion_complete"
branch_labels = None
depends_on = None


def upgrade():
    """Add SUBMITTED value to applicationswithpiideleted enum."""
    op.execute("ALTER TYPE applicationswithpiideleted ADD VALUE IF NOT EXISTS 'SUBMITTED'")


def downgrade():
    """Downgrade is not easily supported for enum value removal.

    Postgres cannot easily drop individual enum values, so this
    migration is effectively irreversible.
    """
    pass
