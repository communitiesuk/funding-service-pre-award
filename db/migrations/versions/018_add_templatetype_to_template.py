"""add templatetype to template sections

Revision ID: 018_add_templatetype_to_template
Revises: 017_apply_auth
Create Date: 2025-01-23 08:17:46.759604

"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import ENUM

# revision identifiers, used by Alembic.
revision = "018_add_templatetype_to_template"
down_revision = "017_apply_auth"
branch_labels = None
depends_on = None

templatetype_enum = ENUM("APPLICATION", "REPORTING", name="templatetype", create_type=False)


def upgrade():
    templatetype_enum.create(op.get_bind(), checkfirst=True)

    with op.batch_alter_table("template_section", schema=None) as batch_op:
        batch_op.add_column(sa.Column("type", templatetype_enum, nullable=False))


def downgrade():
    with op.batch_alter_table("template_section", schema=None) as batch_op:
        batch_op.drop_column("type")

    templatetype_enum.drop(op.get_bind(), checkfirst=True)
