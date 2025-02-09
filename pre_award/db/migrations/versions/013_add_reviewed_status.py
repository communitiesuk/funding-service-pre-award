"""Add REVIEWED status to status enum

Revision ID: 013_add_reviewed_status
Revises: 012_change_short_codes_to_citext
Create Date: 2024-11-22 15:18:44.153089

"""

from alembic import op

# revision identifiers, used by Alembic.
revision = "013_add_reviewed_status"
down_revision = "012_change_short_codes_to_citext"
branch_labels = None
depends_on = None


def upgrade():
    # Add the 'REVIEWED' value to the 'status' enum type
    op.execute("alter type status add value 'REVIEWED' after 'CHANGE_RECEIVED'")


def downgrade():
    # Revert enum by removing the new statuses
    # Step 1: Rename the existing ENUM type
    op.execute("ALTER TYPE status RENAME TO status_old")
    # Step 2: Create a new ENUM type without the unwanted value
    op.execute("""
        CREATE TYPE status AS ENUM(
            'NOT_STARTED',
            'IN_PROGRESS',
            'SUBMITTED',
            'COMPLETED',
            'CHANGE_REQUESTED',
            'CHANGE_RECEIVED'
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
    op.execute("""
        ALTER TABLE assessment_records
        ALTER COLUMN workflow_status
        TYPE status
        USING workflow_status::TEXT::status
    """)
    # Step 4: Drop the old ENUM type
    op.execute("DROP TYPE status_old")
