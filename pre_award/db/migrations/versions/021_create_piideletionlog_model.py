import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "021_create_piideletionlog_model"
down_revision = "020_adding_pii_deletion_complete"
branch_labels = None
depends_on = None


applications_with_pii_deleted_enum = postgresql.ENUM(
    "UN_SUBMITTED",
    "ALL",
    name="applicationswithpiideleted",
    create_type=False,
)


def upgrade():
    bind = op.get_bind()

    # create type only if it doesn't already exist
    applications_with_pii_deleted_enum.create(bind, checkfirst=True)

    op.create_table(
        "pii_deletion_log",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("round_id", sa.Uuid(), nullable=False),
        sa.Column("deletion_timestamp", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.Column("deleted_by", sa.String(), nullable=False),
        sa.Column(
            "applications_with_pii_deleted",
            applications_with_pii_deleted_enum,
            nullable=False,
        ),
        sa.Column("applications_with_pii_deleted_count", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["round_id"], ["round.id"], name=op.f("fk_pii_deletion_log_round_id_round")),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_pii_deletion_log")),
    )
    with op.batch_alter_table("pii_deletion_log", schema=None) as batch_op:
        batch_op.create_index(batch_op.f("ix_pii_deletion_log_round_id"), ["round_id"], unique=False)


def downgrade():
    with op.batch_alter_table("pii_deletion_log", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_pii_deletion_log_round_id"))

    op.drop_table("pii_deletion_log")
