"""add expression to conditions

Revision ID: 017_add_expression_to_conditions
Revises: 016_section_template_id
Create Date: 2025-02-21 10:21:58.208843

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "017_add_expression_to_conditions"
down_revision = "016_section_template_id"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("template_question_condition", schema=None) as batch_op:
        batch_op.add_column(sa.Column("expression", sa.String(), nullable=False))

    with op.batch_alter_table("proto_data_collection_question_condition", schema=None) as batch_op:
        batch_op.add_column(sa.Column("expression", sa.String(), nullable=False))


def downgrade():
    with op.batch_alter_table("template_question_condition", schema=None) as batch_op:
        batch_op.drop_column("expression")

    with op.batch_alter_table("proto_data_collection_question_condition", schema=None) as batch_op:
        batch_op.drop_column("expression")
