"""Add ZeroToFour to ScoringSystem ENUM

Revision ID: 013_add_zerotofour_scoringsystem
Revises: 012_change_short_codes_to_citext
Create Date: 2025-03-13 21:26:46.315063

"""

from alembic import op

# revision identifiers, used by Alembic.
revision = "013_add_zerotofour_scoringsystem"
down_revision = "012_change_short_codes_to_citext"
branch_labels = None
depends_on = None


def upgrade():
    op.execute("alter type scoringsystem add value 'ZeroToFour' after 'ZeroToOne'")


def downgrade():
    # Revert enum by removing the new scoringsystem
    # Step 1: Rename the existing ENUM type
    op.execute("ALTER TYPE scoringsystem RENAME TO scoringsystem_old")
    # Step 2: Create a new ENUM type without the unwanted value
    op.execute("""
        CREATE TYPE scoringsystem AS ENUM(
            'OneToFive',
            'ZeroToThree',
            'ZeroToOne'
        )
    """)
    # Step 3: Update all columns using the old ENUM type to use the new ENUM type
    op.execute("""
        ALTER TABLE scoring_system
        ALTER COLUMN scoring_system_name
        TYPE scoringsystem
        USING scoring_system_name::TEXT::scoringsystem
    """)
    # Step 4: Drop the old ENUM type
    op.execute("DROP TYPE scoringsystem_old")
