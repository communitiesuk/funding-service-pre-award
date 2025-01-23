"""generic data collection tables

Revision ID: 019_generic_data_collection_tabl
Revises: 018_add_templatetype_to_template
Create Date: 2025-01-23 09:04:21.190696

"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql
from sqlalchemy.dialects.postgresql import ENUM

# revision identifiers, used by Alembic.
revision = "019_generic_data_collection_tabl"
down_revision = "018_add_templatetype_to_template"
branch_labels = None
depends_on = None

question_type_enum = ENUM("TEXT_INPUT", "TEXTAREA", "RADIOS", name="questiontype", create_type=False)


def upgrade():
    op.create_table(
        "proto_data_collection",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_proto_data_collection")),
    )
    op.create_table(
        "proto_data_collection_section",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("slug", sa.String(), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("order", sa.Integer(), nullable=False),
        sa.Column("round_id", sa.UUID(), nullable=False),
        sa.CheckConstraint("regexp_like(slug, '[a-z\\-]+')", name=op.f("ck_proto_data_collection_section_slug")),
        sa.ForeignKeyConstraint(
            ["round_id"], ["round.id"], name=op.f("fk_proto_data_collection_section_round_id_round")
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_proto_data_collection_section")),
        sa.UniqueConstraint("round_id", "slug", name="uq_as_slug_for_round2"),
    )
    op.create_table(
        "proto_data_collection_question",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("slug", sa.String(), nullable=False),
        sa.Column("type", question_type_enum, nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("hint", sa.String(), nullable=True),
        sa.Column("order", sa.Integer(), nullable=False),
        sa.Column("data_source", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("section_id", sa.Integer(), nullable=False),
        sa.Column("template_question_id", sa.Integer(), nullable=True),
        sa.Column("data_standard_id", sa.Integer(), nullable=True),
        sa.CheckConstraint("regexp_like(slug, '[a-z\\-]+')", name=op.f("ck_proto_data_collection_question_slug")),
        sa.ForeignKeyConstraint(
            ["data_standard_id"],
            ["data_standard.id"],
            name=op.f("fk_proto_data_collection_question_data_standard_id_data_standard"),
        ),
        sa.ForeignKeyConstraint(
            ["section_id"],
            ["proto_data_collection_section.id"],
            name=op.f("fk_proto_data_collection_question_section_id_proto_data_collection_section"),
        ),
        sa.ForeignKeyConstraint(
            ["template_question_id"],
            ["template_question.id"],
            name=op.f("fk_proto_data_collection_question_template_question_id_template_question"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_proto_data_collection_question")),
        sa.UniqueConstraint("section_id", "order", name="uq_aq_order_for_section2"),
        sa.UniqueConstraint("section_id", "slug", name="uq_aq_slug_for_section2"),
    )
    op.create_table(
        "proto_data_collection_section_data",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("data", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("completed", sa.Boolean(), nullable=False),
        sa.Column("data_collection_id", sa.Integer(), nullable=False),
        sa.Column("section_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["data_collection_id"],
            ["proto_data_collection.id"],
            name=op.f("fk_proto_data_collection_section_data_data_collection_id_proto_data_collection"),
        ),
        sa.ForeignKeyConstraint(
            ["section_id"],
            ["proto_data_collection_section.id"],
            name=op.f("fk_proto_data_collection_section_data_section_id_proto_data_collection_section"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_proto_data_collection_section_data")),
        sa.UniqueConstraint(
            "data_collection_id", "section_id", name=op.f("uq_proto_data_collection_section_data_data_collection_id")
        ),
    )
    op.drop_table("application_question")
    op.drop_table("proto_application_section_data")
    op.drop_table("application_section")
    with op.batch_alter_table("proto_application", schema=None) as batch_op:
        batch_op.add_column(sa.Column("data_collection_id", sa.Integer(), nullable=False))
        batch_op.create_foreign_key(
            batch_op.f("fk_proto_application_data_collection_id_proto_data_collection"),
            "proto_data_collection",
            ["data_collection_id"],
            ["id"],
        )


def downgrade():
    with op.batch_alter_table("proto_application", schema=None) as batch_op:
        batch_op.drop_constraint(
            batch_op.f("fk_proto_application_data_collection_id_proto_data_collection"), type_="foreignkey"
        )
        batch_op.drop_column("data_collection_id")

    op.create_table(
        "application_section",
        sa.Column(
            "id",
            sa.INTEGER(),
            server_default=sa.text("nextval('application_section_id_seq'::regclass)"),
            autoincrement=True,
            nullable=False,
        ),
        sa.Column("created_at", postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
        sa.Column("updated_at", postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
        sa.Column("slug", sa.VARCHAR(), autoincrement=False, nullable=False),
        sa.Column("title", sa.VARCHAR(), autoincrement=False, nullable=False),
        sa.Column("order", sa.INTEGER(), autoincrement=False, nullable=False),
        sa.Column("round_id", sa.UUID(), autoincrement=False, nullable=False),
        sa.CheckConstraint("regexp_like(slug::text, '[a-z\\-]+'::text)", name="ck_application_section_slug"),
        sa.ForeignKeyConstraint(["round_id"], ["round.id"], name="fk_application_section_round_id_round"),
        sa.PrimaryKeyConstraint("id", name="pk_application_section"),
        sa.UniqueConstraint("round_id", "slug", name="uq_as_slug_for_round2"),
        postgresql_ignore_search_path=False,
    )
    op.create_table(
        "proto_application_section_data",
        sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column("created_at", postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
        sa.Column("updated_at", postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
        sa.Column("data", postgresql.JSONB(astext_type=sa.Text()), autoincrement=False, nullable=False),
        sa.Column("proto_application_id", sa.INTEGER(), autoincrement=False, nullable=False),
        sa.Column("section_id", sa.INTEGER(), autoincrement=False, nullable=False),
        sa.Column("completed", sa.BOOLEAN(), autoincrement=False, nullable=False),
        sa.ForeignKeyConstraint(
            ["proto_application_id"],
            ["proto_application.id"],
            name="fk_proto_application_section_data_proto_application_id__21b3",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["section_id"],
            ["application_section.id"],
            name="fk_proto_application_section_data_section_id_applicatio_bbca",
        ),
        sa.PrimaryKeyConstraint("id", name="pk_proto_application_section_data"),
        sa.UniqueConstraint(
            "proto_application_id", "section_id", name="uq_proto_application_section_data_proto_application_id"
        ),
    )
    op.create_table(
        "application_question",
        sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column("created_at", postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
        sa.Column("updated_at", postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
        sa.Column("slug", sa.VARCHAR(), autoincrement=False, nullable=False),
        sa.Column(
            "type",
            question_type_enum,
            autoincrement=False,
            nullable=False,
        ),
        sa.Column("title", sa.VARCHAR(), autoincrement=False, nullable=False),
        sa.Column("hint", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.Column("order", sa.INTEGER(), autoincrement=False, nullable=False),
        sa.Column("data_source", postgresql.JSONB(astext_type=sa.Text()), autoincrement=False, nullable=True),
        sa.Column("section_id", sa.INTEGER(), autoincrement=False, nullable=False),
        sa.Column("template_question_id", sa.INTEGER(), autoincrement=False, nullable=True),
        sa.Column("data_standard_id", sa.INTEGER(), autoincrement=False, nullable=True),
        sa.CheckConstraint("regexp_like(slug::text, '[a-z\\-]+'::text)", name="ck_application_question_slug"),
        sa.ForeignKeyConstraint(
            ["data_standard_id"], ["data_standard.id"], name="fk_application_question_data_standard_id_data_standard"
        ),
        sa.ForeignKeyConstraint(
            ["section_id"], ["application_section.id"], name="fk_application_question_section_id_application_section"
        ),
        sa.ForeignKeyConstraint(
            ["template_question_id"],
            ["template_question.id"],
            name="fk_application_question_template_question_id_template_question",
        ),
        sa.PrimaryKeyConstraint("id", name="pk_application_question"),
        sa.UniqueConstraint("section_id", "order", name="uq_aq_order_for_section"),
        sa.UniqueConstraint("section_id", "slug", name="uq_aq_slug_for_section"),
    )
    op.drop_table("proto_data_collection_section_data")
    op.drop_table("proto_data_collection_question")
    op.drop_table("proto_data_collection_section")
    op.drop_table("proto_data_collection")
