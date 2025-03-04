"""re-run proto migration

Revision ID: 010_re_run_proto_migration
Revises: 009_relax_flag_json_constraints
Create Date: 2025-01-24 09:27:59.222550

"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy import text
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "010_re_run_proto_migration"
down_revision = "009_relax_flag_json_constraints"
branch_labels = None
depends_on = None

fundstatus_enum = postgresql.ENUM("DRAFT", "LIVE", "RETIRED", name="fundstatus", create_type=False)
templatetype_enum = postgresql.ENUM("APPLICATION", "REPORTING", name="templatetype", create_type=False)
questiontype_enum = postgresql.ENUM(
    "TEXT_INPUT",
    "TEXTAREA",
    "RADIOS",
    "NUMBER",
    "POUNDS_AND_PENCE",
    "LIST_AUTOCOMPLETE",
    name="questiontype",
    create_type=False,
)


def upgrade():
    fundstatus_enum.create(op.get_bind().engine, checkfirst=True)
    templatetype_enum.create(op.get_bind().engine, checkfirst=True)
    questiontype_enum.create(op.get_bind().engine, checkfirst=True)

    op.create_table(
        "data_standard",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("slug", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_data_standard")),
        sa.UniqueConstraint("slug", name=op.f("uq_data_standard_slug")),
    )
    op.create_table(
        "magic_link",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("path", sa.String(), nullable=False),
        sa.Column("token", sa.String(), nullable=False),
        sa.Column("used", sa.Boolean(), nullable=False),
        sa.Column(
            "expires_date", sa.DateTime(), server_default=sa.text("now() + make_interval(secs=>3600.0)"), nullable=False
        ),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_magic_link")),
    )
    with op.batch_alter_table("magic_link", schema=None) as batch_op:
        batch_op.create_index(batch_op.f("ix_magic_link_token"), ["token"], unique=True)

    op.create_table(
        "proto_data_collection_definition",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_proto_data_collection_definition")),
    )
    op.create_table(
        "proto_data_collection_instance",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_proto_data_collection_instance")),
    )
    op.create_table(
        "template_section",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("slug", sa.String(), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("order", sa.Integer(), nullable=False),
        sa.Column("type", templatetype_enum, nullable=False),
        sa.CheckConstraint("regexp_like(slug, '[a-z\\-]+')", name=op.f("ck_template_section_slug")),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_template_section")),
        sa.UniqueConstraint("slug", name=op.f("uq_template_section_slug")),
    )
    op.create_table(
        "proto_data_collection_definition_section",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("slug", sa.String(), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("order", sa.Integer(), nullable=False),
        sa.Column("definition_id", sa.Integer(), nullable=False),
        sa.CheckConstraint(
            "regexp_like(slug, '[a-z\\-]+')", name=op.f("ck_proto_data_collection_definition_section_slug")
        ),
        sa.ForeignKeyConstraint(
            ["definition_id"],
            ["proto_data_collection_definition.id"],
            name=op.f("fk_proto_data_collection_definition_section_definition_id_proto_data_collection_definition"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_proto_data_collection_definition_section")),
        sa.UniqueConstraint("definition_id", "slug", name="uq_as_slug_for_definition"),
    )
    op.create_table(
        "template_question",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("slug", sa.String(), nullable=False),
        sa.Column("type", questiontype_enum, nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("hint", sa.String(), nullable=True),
        sa.Column("order", sa.Integer(), nullable=False),
        sa.Column("data_source", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("template_section_id", sa.Integer(), nullable=False),
        sa.Column("data_standard_id", sa.Integer(), nullable=True),
        sa.CheckConstraint("regexp_like(slug, '[a-z\\-]+')", name=op.f("ck_template_question_slug")),
        sa.ForeignKeyConstraint(
            ["data_standard_id"], ["data_standard.id"], name=op.f("fk_template_question_data_standard_id_data_standard")
        ),
        sa.ForeignKeyConstraint(
            ["template_section_id"],
            ["template_section.id"],
            name=op.f("fk_template_question_template_section_id_template_section"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_template_question")),
        sa.UniqueConstraint("template_section_id", "order", name="uq_tq_order_for_section"),
        sa.UniqueConstraint("template_section_id", "slug", name="uq_tq_slug_for_section"),
    )
    op.create_table(
        "proto_application",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("external_id", sa.UUID(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("code", sa.String(), nullable=False),
        sa.Column("fake", sa.Boolean(), nullable=False),
        sa.Column("round_id", sa.UUID(), nullable=False),
        sa.Column("account_id", sa.UUID(), nullable=False),
        sa.Column("data_collection_instance_id", sa.Integer(), nullable=False),
        sa.Column("updated_by_applicant_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["account_id"], ["account.id"], name=op.f("fk_proto_application_account_id_account")),
        sa.ForeignKeyConstraint(
            ["data_collection_instance_id"],
            ["proto_data_collection_instance.id"],
            name=op.f("fk_proto_application_data_collection_id_proto_data_collection_instance"),
        ),
        sa.ForeignKeyConstraint(["round_id"], ["round.id"], name=op.f("fk_proto_application_round_id_round")),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_proto_application")),
    )
    op.create_table(
        "proto_data_collection_definition_question",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("slug", sa.String(), nullable=False),
        sa.Column("type", questiontype_enum, nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("hint", sa.String(), nullable=True),
        sa.Column("order", sa.Integer(), nullable=False),
        sa.Column("data_source", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("section_id", sa.Integer(), nullable=False),
        sa.Column("template_question_id", sa.Integer(), nullable=True),
        sa.Column("data_standard_id", sa.Integer(), nullable=True),
        sa.CheckConstraint(
            "regexp_like(slug, '[a-z\\-]+')", name=op.f("ck_proto_data_collection_definition_question_slug")
        ),
        sa.ForeignKeyConstraint(
            ["data_standard_id"],
            ["data_standard.id"],
            name=op.f("fk_proto_data_collection_definition_question_data_standard_id_data_standard"),
        ),
        sa.ForeignKeyConstraint(
            ["section_id"],
            ["proto_data_collection_definition_section.id"],
            name=op.f(
                "fk_proto_data_collection_definition_question_section_id_proto_data_collection_definition_section"
            ),
        ),
        sa.ForeignKeyConstraint(
            ["template_question_id"],
            ["template_question.id"],
            name=op.f("fk_proto_data_collection_definition_question_template_question_id_template_question"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_proto_data_collection_definition_question")),
        sa.UniqueConstraint("section_id", "order", name="uq_aq_order_for_section3"),
        sa.UniqueConstraint("section_id", "slug", name="uq_aq_slug_for_section3"),
    )
    op.create_table(
        "proto_data_collection_instance_section_data",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("data", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("completed", sa.Boolean(), nullable=False),
        sa.Column("instance_id", sa.Integer(), nullable=False),
        sa.Column("section_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["instance_id"],
            ["proto_data_collection_instance.id"],
            name=op.f("fk_proto_data_collection_instance_section_data_instance_id_proto_data_collection_instance"),
        ),
        sa.ForeignKeyConstraint(
            ["section_id"],
            ["proto_data_collection_definition_section.id"],
            name=op.f(
                "fk_proto_data_collection_instance_section_data_section_id_proto_data_collection_definition_section"
            ),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_proto_data_collection_instance_section_data")),
        sa.UniqueConstraint(
            "instance_id", "section_id", name=op.f("uq_proto_data_collection_instance_section_data_instance_id")
        ),
    )
    op.create_table(
        "proto_report",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("code", sa.String(), nullable=False),
        sa.Column("fake", sa.Boolean(), nullable=False),
        sa.Column("round_id", sa.UUID(), nullable=False),
        sa.Column("account_id", sa.UUID(), nullable=False),
        sa.Column("data_collection_id", sa.Integer(), nullable=False),
        sa.Column("updated_by_reporter_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["account_id"], ["account.id"], name=op.f("fk_proto_report_account_id_account")),
        sa.ForeignKeyConstraint(
            ["data_collection_id"],
            ["proto_data_collection_instance.id"],
            name=op.f("fk_proto_report_data_collection_id_proto_data_collection_instance"),
        ),
        sa.ForeignKeyConstraint(["round_id"], ["round.id"], name=op.f("fk_proto_report_round_id_round")),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_proto_report")),
    )
    with op.batch_alter_table("account", schema=None) as batch_op:
        batch_op.add_column(sa.Column("is_magic_link", sa.Boolean(), nullable=True))
        batch_op.add_column(
            sa.Column("proto_created_date", sa.DateTime(), server_default=sa.text("now()"), nullable=True)
        )
        batch_op.add_column(
            sa.Column("proto_updated_date", sa.DateTime(), server_default=sa.text("now()"), nullable=True)
        )

    with op.batch_alter_table("fund", schema=None) as batch_op:
        batch_op.add_column(sa.Column("proto_status", fundstatus_enum, nullable=True))
        batch_op.add_column(sa.Column("proto_name", sa.String(), nullable=True))
        batch_op.add_column(sa.Column("proto_name_cy", sa.String(), nullable=True))
        batch_op.add_column(
            sa.Column("proto_created_date", sa.DateTime(), server_default=sa.text("now()"), nullable=True)
        )
        batch_op.add_column(
            sa.Column("proto_updated_date", sa.DateTime(), server_default=sa.text("now()"), nullable=True)
        )
        batch_op.add_column(sa.Column("proto_prospectus_link", sa.String(), nullable=True))
        batch_op.add_column(sa.Column("proto_apply_action_description", sa.String(), nullable=True))

    op.execute(text("update fund set proto_status = 'DRAFT' where proto_status is null"))

    with op.batch_alter_table("fund", schema=None) as batch_op:
        batch_op.alter_column("proto_status", existing_type=fundstatus_enum, nullable=False)

    with op.batch_alter_table("round", schema=None) as batch_op:
        batch_op.add_column(sa.Column("proto_draft", sa.Boolean(), nullable=True))
        batch_op.add_column(sa.Column("proto_start_date", sa.Date(), nullable=True))
        batch_op.add_column(sa.Column("proto_end_date", sa.Date(), nullable=True))
        batch_op.add_column(
            sa.Column("proto_created_date", sa.DateTime(), server_default=sa.text("now()"), nullable=True)
        )
        batch_op.add_column(
            sa.Column("proto_updated_date", sa.DateTime(), server_default=sa.text("now()"), nullable=True)
        )
        batch_op.add_column(sa.Column("data_collection_definition_id", sa.Integer(), nullable=True))
        batch_op.create_foreign_key(
            batch_op.f("fk_round_data_collection_definition_id_proto_data_collection_definition"),
            "proto_data_collection_definition",
            ["data_collection_definition_id"],
            ["id"],
        )

    op.execute(text("update fund set proto_name = name_json->>'en', proto_name_cy = name_json->>'cy'"))
    op.execute(text("update fund set proto_apply_action_description = title_json->>'en'"))

    op.execute(text("update round set proto_start_date = '2025-01-01', proto_end_date = '2025-02-28'"))
    op.execute(text("update round set proto_draft = true where proto_draft is null"))

    with op.batch_alter_table("round", schema=None) as batch_op:
        batch_op.alter_column("proto_start_date", existing_type=sa.Date(), nullable=False)
        batch_op.alter_column("proto_end_date", existing_type=sa.Date(), nullable=False)
        batch_op.alter_column("proto_draft", existing_type=sa.Boolean(), nullable=False)


def downgrade():
    with op.batch_alter_table("round", schema=None) as batch_op:
        batch_op.drop_constraint(
            batch_op.f("fk_round_data_collection_definition_id_proto_data_collection_definition"), type_="foreignkey"
        )
        batch_op.drop_column("data_collection_definition_id")
        batch_op.drop_column("proto_updated_date")
        batch_op.drop_column("proto_created_date")
        batch_op.drop_column("proto_end_date")
        batch_op.drop_column("proto_start_date")
        batch_op.drop_column("proto_draft")

    with op.batch_alter_table("fund", schema=None) as batch_op:
        batch_op.drop_column("proto_apply_action_description")
        batch_op.drop_column("proto_prospectus_link")
        batch_op.drop_column("proto_updated_date")
        batch_op.drop_column("proto_created_date")
        batch_op.drop_column("proto_name_cy")
        batch_op.drop_column("proto_name")
        batch_op.drop_column("proto_status")

    with op.batch_alter_table("account", schema=None) as batch_op:
        batch_op.drop_column("proto_updated_date")
        batch_op.drop_column("proto_created_date")
        batch_op.drop_column("is_magic_link")

    op.drop_table("proto_report")
    op.drop_table("proto_data_collection_instance_section_data")
    op.drop_table("proto_data_collection_definition_question")
    op.drop_table("proto_application")
    op.drop_table("template_question")
    op.drop_table("proto_data_collection_definition_section")
    op.drop_table("template_section")
    op.drop_table("proto_data_collection_instance")
    op.drop_table("proto_data_collection_definition")
    with op.batch_alter_table("magic_link", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_magic_link_token"))

    op.drop_table("magic_link")
    op.drop_table("data_standard")
