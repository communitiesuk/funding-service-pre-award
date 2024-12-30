"""Create feedback_message column

Revision ID: 008_add_feedback_message
Revises: 007_create_account_store
Create Date: 2024-11-30 19:33:00.710210

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "008_add_feedback_message"
down_revision = "007_create_account_store"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("forms", schema=None) as batch_op:
        batch_op.add_column(sa.Column("feedback_message", sa.String(), nullable=True))

    op.execute("ALTER TYPE status ADD VALUE 'CHANGES_REQUESTED'")


def downgrade():
    with op.batch_alter_table("forms", schema=None) as batch_op:
        batch_op.drop_column("feedback_message")

    # Step 1: Rename the existing ENUM type
    op.execute("ALTER TYPE status RENAME TO status_old")

    # Step 2: Create a new ENUM type without the unwanted value
    op.execute("""
        CREATE TYPE status AS ENUM(
            'NOT_STARTED',
            'IN_PROGRESS',
            'SUBMITTED',
            'COMPLETED'
        )
    """)

    # Step 3: Update all columns using the old ENUM type to use the new ENUM type
    op.execute("""
        ALTER TABLE forms
        ALTER COLUMN status
        TYPE status
        USING status::TEXT::status
    """)

    op.execute("""
        ALTER TABLE applications
        ALTER COLUMN status
        TYPE status
        USING status::TEXT::status
    """)

    op.execute("""
        ALTER TABLE feedback
        ALTER COLUMN status
        TYPE status
        USING status::TEXT::status
    """)

    # Step 4: Drop the old ENUM type
    op.execute("DROP TYPE status_old")
