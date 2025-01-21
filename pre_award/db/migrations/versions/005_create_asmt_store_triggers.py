"""create_asmt_store_triggers

Revision ID: 005_create_asmt_store_triggers
Revises: 004_create_assessment_store
Create Date: 2024-12-02 13:47:41.220406

"""

from alembic import op
from alembic_utils.pg_function import PGFunction
from alembic_utils.pg_trigger import PGTrigger

# revision identifiers, used by Alembic.
revision = "005_create_asmt_store_triggers"
down_revision = "004_create_assessment_store"
branch_labels = None
depends_on = None


def upgrade():
    public_block_blob_mutate = PGFunction(
        schema="public",
        signature="block_blob_mutate()",
        definition="RETURNS TRIGGER\n    LANGUAGE PLPGSQL\n    AS\n    $$\n    BEGIN\n        IF NEW.jsonb_blob <> OLD.jsonb_blob THEN\n        RAISE EXCEPTION 'Cannot mutate application json.';\n        END IF;\n        RETURN NEW;\n    END;\n    $$",  # noqa: E501
    )
    op.create_entity(public_block_blob_mutate)

    public_assessment_records_block_updates_on_app_blob = PGTrigger(
        schema="public",
        signature="block_updates_on_app_blob",
        on_entity="public.assessment_records",
        is_constraint=False,
        definition="BEFORE UPDATE\n    ON assessment_records\n    FOR EACH ROW\n    EXECUTE PROCEDURE block_blob_mutate()",  # noqa: E501
    )
    op.create_entity(public_assessment_records_block_updates_on_app_blob)


def downgrade():
    public_assessment_records_block_updates_on_app_blob = PGTrigger(
        schema="public",
        signature="block_updates_on_app_blob",
        on_entity="public.assessment_records",
        is_constraint=False,
        definition="BEFORE UPDATE\n    ON assessment_records\n    FOR EACH ROW\n    EXECUTE PROCEDURE block_blob_mutate()",  # noqa: E501
    )
    op.drop_entity(public_assessment_records_block_updates_on_app_blob)

    public_block_blob_mutate = PGFunction(
        schema="public",
        signature="block_blob_mutate()",
        definition="RETURNS TRIGGER\n    LANGUAGE PLPGSQL\n    AS\n    $$\n    BEGIN\n        IF NEW.jsonb_blob <> OLD.jsonb_blob THEN\n        RAISE EXCEPTION 'Cannot mutate application json.';\n        END IF;\n        RETURN NEW;\n    END;\n    $$",  # noqa: E501
    )
    op.drop_entity(public_block_blob_mutate)
