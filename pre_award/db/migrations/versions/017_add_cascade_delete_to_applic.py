"""Add CASCADE delete to Applications and AssessmentRecords

Revision ID: 017_add_cascade_delete_to_applic
Revises: 016_add_display_name_to_form_de
Create Date: 2025-11-17 12:45:00.000000

"""

from alembic import op

# revision identifiers, used by Alembic.
revision = "017_add_cascade_delete_to_applic"
down_revision = "016_add_display_name_to_form_de"
branch_labels = None
depends_on = None


def upgrade():
    # --- Applications related ---
    with op.batch_alter_table("end_of_application_survey_feedback", schema=None) as batch_op:
        batch_op.drop_constraint("fk_end_of_application_survey_feedback_application_id_ap_d5f0", type_="foreignkey")
        batch_op.create_foreign_key(
            batch_op.f("fk_end_of_application_survey_feedback_application_id_applications"),
            "applications",
            ["application_id"],
            ["id"],
            ondelete="CASCADE",
        )

    with op.batch_alter_table("feedback", schema=None) as batch_op:
        batch_op.drop_constraint("fk_feedback_application_id_applications", type_="foreignkey")
        batch_op.create_foreign_key(
            batch_op.f("fk_feedback_application_id_applications"),
            "applications",
            ["application_id"],
            ["id"],
            ondelete="CASCADE",
        )

    with op.batch_alter_table("forms", schema=None) as batch_op:
        batch_op.drop_constraint("fk_forms_application_id_applications", type_="foreignkey")
        batch_op.create_foreign_key(
            batch_op.f("fk_forms_application_id_applications"),
            "applications",
            ["application_id"],
            ["id"],
            ondelete="CASCADE",
        )

    with op.batch_alter_table("eligibility", schema=None) as batch_op:
        batch_op.drop_constraint("fk_eligibility_application_id_applications", type_="foreignkey")
        batch_op.create_foreign_key(
            batch_op.f("fk_eligibility_application_id_applications"),
            "applications",
            ["application_id"],
            ["id"],
            ondelete="CASCADE",
        )

    with op.batch_alter_table("research_survey", schema=None) as batch_op:
        batch_op.drop_constraint("fk_research_survey_application_id_applications", type_="foreignkey")
        batch_op.create_foreign_key(
            batch_op.f("fk_research_survey_application_id_applications"),
            "applications",
            ["application_id"],
            ["id"],
            ondelete="CASCADE",
        )

    # --- AssessmentRecords related ---
    with op.batch_alter_table("allocation_association", schema=None) as batch_op:
        batch_op.drop_constraint("fk_allocation_association_application_id_assessment_records", type_="foreignkey")
        batch_op.create_foreign_key(
            batch_op.f("fk_allocation_association_application_id_assessment_records"),
            "assessment_records",
            ["application_id"],
            ["application_id"],
            ondelete="CASCADE",
        )

    with op.batch_alter_table("assessment_flag", schema=None) as batch_op:
        batch_op.drop_constraint("fk_assessment_flag_application_id_assessment_records", type_="foreignkey")
        batch_op.create_foreign_key(
            batch_op.f("fk_assessment_flag_application_id_assessment_records"),
            "assessment_records",
            ["application_id"],
            ["application_id"],
            ondelete="CASCADE",
        )

    with op.batch_alter_table("comments", schema=None) as batch_op:
        batch_op.drop_constraint("fk_comments_application_id_assessment_records", type_="foreignkey")
        batch_op.create_foreign_key(
            batch_op.f("fk_comments_application_id_assessment_records"),
            "assessment_records",
            ["application_id"],
            ["application_id"],
            ondelete="CASCADE",
        )

    with op.batch_alter_table("comments_update", schema=None) as batch_op:
        batch_op.drop_constraint("fk_comments_update_comment_id_comments", type_="foreignkey")
        batch_op.create_foreign_key(
            batch_op.f("fk_comments_update_comment_id_comments"),
            "comments",
            ["comment_id"],
            ["comment_id"],
            ondelete="CASCADE",
        )

    with op.batch_alter_table("flag_update", schema=None) as batch_op:
        batch_op.drop_constraint("fk_flag_update_assessment_flag_id_assessment_flag", type_="foreignkey")
        batch_op.create_foreign_key(
            batch_op.f("fk_flag_update_assessment_flag_id_assessment_flag"),
            "assessment_flag",
            ["assessment_flag_id"],
            ["id"],
            ondelete="CASCADE",
        )

    with op.batch_alter_table("qa_complete", schema=None) as batch_op:
        batch_op.drop_constraint("fk_qa_complete_application_id_assessment_records", type_="foreignkey")
        batch_op.create_foreign_key(
            batch_op.f("fk_qa_complete_application_id_assessment_records"),
            "assessment_records",
            ["application_id"],
            ["application_id"],
            ondelete="CASCADE",
        )

    with op.batch_alter_table("scores", schema=None) as batch_op:
        batch_op.drop_constraint("fk_scores_application_id_assessment_records", type_="foreignkey")
        batch_op.create_foreign_key(
            batch_op.f("fk_scores_application_id_assessment_records"),
            "assessment_records",
            ["application_id"],
            ["application_id"],
            ondelete="CASCADE",
        )

    with op.batch_alter_table("tag_association", schema=None) as batch_op:
        batch_op.drop_constraint("fk_tag_association_application_id_assessment_records", type_="foreignkey")
        batch_op.create_foreign_key(
            batch_op.f("fk_tag_association_application_id_assessment_records"),
            "assessment_records",
            ["application_id"],
            ["application_id"],
            ondelete="CASCADE",
        )


def downgrade():
    # --- AssessmentRecords related ---
    with op.batch_alter_table("tag_association", schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f("fk_tag_association_application_id_assessment_records"), type_="foreignkey")
        batch_op.create_foreign_key(
            "fk_tag_association_application_id_assessment_records",
            "assessment_records",
            ["application_id"],
            ["application_id"],
        )

    with op.batch_alter_table("scores", schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f("fk_scores_application_id_assessment_records"), type_="foreignkey")
        batch_op.create_foreign_key(
            "fk_scores_application_id_assessment_records", "assessment_records", ["application_id"], ["application_id"]
        )

    with op.batch_alter_table("qa_complete", schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f("fk_qa_complete_application_id_assessment_records"), type_="foreignkey")
        batch_op.create_foreign_key(
            "fk_qa_complete_application_id_assessment_records",
            "assessment_records",
            ["application_id"],
            ["application_id"],
        )

    with op.batch_alter_table("flag_update", schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f("fk_flag_update_assessment_flag_id_assessment_flag"), type_="foreignkey")
        batch_op.create_foreign_key(
            "fk_flag_update_assessment_flag_id_assessment_flag", "assessment_flag", ["assessment_flag_id"], ["id"]
        )

    with op.batch_alter_table("comments_update", schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f("fk_comments_update_comment_id_comments"), type_="foreignkey")
        batch_op.create_foreign_key(
            "fk_comments_update_comment_id_comments", "comments", ["comment_id"], ["comment_id"]
        )

    with op.batch_alter_table("comments", schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f("fk_comments_application_id_assessment_records"), type_="foreignkey")
        batch_op.create_foreign_key(
            "fk_comments_application_id_assessment_records",
            "assessment_records",
            ["application_id"],
            ["application_id"],
        )

    with op.batch_alter_table("assessment_flag", schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f("fk_assessment_flag_application_id_assessment_records"), type_="foreignkey")
        batch_op.create_foreign_key(
            "fk_assessment_flag_application_id_assessment_records",
            "assessment_records",
            ["application_id"],
            ["application_id"],
        )

    with op.batch_alter_table("allocation_association", schema=None) as batch_op:
        batch_op.drop_constraint(
            batch_op.f("fk_allocation_association_application_id_assessment_records"), type_="foreignkey"
        )
        batch_op.create_foreign_key(
            "fk_allocation_association_application_id_assessment_records",
            "assessment_records",
            ["application_id"],
            ["application_id"],
        )

    # --- Applications related ---
    with op.batch_alter_table("research_survey", schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f("fk_research_survey_application_id_applications"), type_="foreignkey")
        batch_op.create_foreign_key(
            "fk_research_survey_application_id_applications", "applications", ["application_id"], ["id"]
        )

    with op.batch_alter_table("eligibility", schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f("fk_eligibility_application_id_applications"), type_="foreignkey")
        batch_op.create_foreign_key(
            "fk_eligibility_application_id_applications", "applications", ["application_id"], ["id"]
        )

    with op.batch_alter_table("forms", schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f("fk_forms_application_id_applications"), type_="foreignkey")
        batch_op.create_foreign_key("fk_forms_application_id_applications", "applications", ["application_id"], ["id"])

    with op.batch_alter_table("feedback", schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f("fk_feedback_application_id_applications"), type_="foreignkey")
        batch_op.create_foreign_key(
            "fk_feedback_application_id_applications", "applications", ["application_id"], ["id"]
        )

    with op.batch_alter_table("end_of_application_survey_feedback", schema=None) as batch_op:
        batch_op.drop_constraint(
            batch_op.f("fk_end_of_application_survey_feedback_application_id_applications"), type_="foreignkey"
        )
        batch_op.create_foreign_key(
            "fk_end_of_application_survey_feedback_application_id_ap_d5f0", "applications", ["application_id"], ["id"]
        )
