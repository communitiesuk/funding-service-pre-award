"""grant recipients

Revision ID: 014_grant_recipients
Revises: 013_scores_and_comments
Create Date: 2025-01-27 21:22:14.168730

"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "014_grant_recipients"
down_revision = "013_scores_and_comments"
branch_labels = None
depends_on = None


grant_recipient_status_enum = postgresql.ENUM("ACTIVE", "COMPLETED", name="grantrecipientstatus", create_type=False)


def upgrade():
    grant_recipient_status_enum.create(op.get_bind().engine, checkfirst=True)

    op.create_table(
        "proto_grant_recipient",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("status", grant_recipient_status_enum, nullable=False),
        sa.Column("application_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["application_id"],
            ["proto_application.id"],
            name=op.f("fk_proto_grant_recipient_application_id_proto_application"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_proto_grant_recipient")),
        sa.UniqueConstraint("application_id", name=op.f("uq_proto_grant_recipient_application_id")),
    )
    with op.batch_alter_table("proto_grant_recipient", schema=None) as batch_op:
        batch_op.create_index(batch_op.f("ix_proto_grant_recipient_status"), ["status"], unique=False)

    with op.batch_alter_table("proto_application", schema=None) as batch_op:
        batch_op.alter_column("submitted", existing_type=sa.BOOLEAN(), nullable=False)
        batch_op.create_index(batch_op.f("ix_proto_application_external_id"), ["external_id"], unique=False)

    with op.batch_alter_table("round", schema=None) as batch_op:
        batch_op.alter_column("proto_start_date", existing_type=sa.DATE(), nullable=True)
        batch_op.alter_column("proto_end_date", existing_type=sa.DATE(), nullable=True)


def downgrade():
    with op.batch_alter_table("round", schema=None) as batch_op:
        batch_op.alter_column("proto_end_date", existing_type=sa.DATE(), nullable=False)
        batch_op.alter_column("proto_start_date", existing_type=sa.DATE(), nullable=False)

    with op.batch_alter_table("proto_application", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_proto_application_external_id"))
        batch_op.alter_column("submitted", existing_type=sa.BOOLEAN(), nullable=True)

    with op.batch_alter_table("proto_grant_recipient", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_proto_grant_recipient_status"))

    op.drop_table("proto_grant_recipient")
