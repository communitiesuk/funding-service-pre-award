"""The module containing all code related to the `assessment_records` table within
the Postgres db.

Tangential structures such as triggers and ENUMS are kept in other
files.

"""

from flask_sqlalchemy.model import DefaultMeta
from sqlalchemy import Boolean, Column, Computed, Index, cast, func
from sqlalchemy.dialects.postgresql import ENUM, JSONB, TEXT, UUID
from sqlalchemy.orm import column_property, relationship

from pre_award.assessment_store.db.models.assessment_record.enums import Language, Status
from pre_award.db import db

BaseModel: DefaultMeta = db.Model


class AssessmentRecord(BaseModel):
    """AssessmentRecord The sqlalchemy-flask model class used to define the
    `assessment_records` table in the Postgres database."""

    __tablename__ = "assessment_records"

    application_id = Column("application_id", UUID, primary_key=True)

    short_id = Column("short_id", db.String(255), nullable=False)

    type_of_application = Column("type_of_application", db.String(255), index=True, nullable=False)

    project_name = Column("project_name", db.String(255), index=True, nullable=False)

    funding_amount_requested = Column("funding_amount_requested", db.Float(), index=True, nullable=False)

    round_id = Column("round_id", UUID, index=True, nullable=False)

    fund_id = Column("fund_id", UUID, index=True, nullable=False)

    language = Column("language", ENUM(Language), default="en")

    workflow_status = Column("workflow_status", ENUM(Status), index=True, default="NOT_STARTED")

    asset_type = Column("asset_type", db.String(255), index=True, nullable=False)

    jsonb_blob = Column("jsonb_blob", JSONB, nullable=False)

    application_json_md5 = Column(
        "application_json_md5",
        TEXT,
        Computed(func.md5(cast(jsonb_blob, TEXT)), persisted=True),
    )

    is_deleted = Column(Boolean, nullable=False, default=False)

    scores = relationship("Score")

    comments = relationship("Comment")

    flags = relationship("AssessmentFlag")

    tag_associations = relationship("TagAssociation")

    qa_complete = relationship("QaComplete")

    user_associations = relationship("AllocationAssociation")

    location_json_blob = Column("location_json_blob", JSONB, nullable=True)

    is_withdrawn = Column("is_withdrawn", Boolean, default=False, nullable=False)

    change_requests = relationship(
        "AssessmentFlag",
        primaryjoin="and_(AssessmentFlag.application_id == AssessmentRecord.application_id, "
        "AssessmentFlag.is_change_request == True)",
        viewonly=True,  # this is a subset relationship; the unfiltered `flags` should be used for writes/deletes
    )
    # These are defined as column_properties not as hybrid_property due to performance
    # Using column_property below forces the json parsing to be done on the DB side which is quicker than in python
    organisation_name = column_property(
        func.coalesce(
            func.jsonb_path_query_first(
                jsonb_blob,
                '$.forms[*].questions[*].fields[*] ? (@.key == "opFJRm").answer',
            ),
            func.jsonb_path_query_first(
                jsonb_blob,
                '$.forms[*].questions[*].fields[*] ? (@.key == "JbmcJE").answer',
            ),
            func.jsonb_path_query_first(
                jsonb_blob,
                '$.forms[*].questions[*].fields[*] ? (@.key == "nYJiWy").answer',
            ),
            func.jsonb_path_query_first(
                jsonb_blob,
                '$.forms[*].questions[*].fields[*] ? (@.key == "SMRWjl").answer',
            ),
        )
    )
    local_authority = column_property(
        func.jsonb_path_query_first(
            jsonb_blob,
            '$.forms[*].questions[*].fields[*] ? (@.key == "nURkuc" || @.key == "WLddBt").answer',
        )
    )
    funding_type = column_property(
        func.jsonb_path_query_first(
            jsonb_blob,
            '$.forms[*].questions[*].fields[*] ? (@.key == "NxVqXd").answer',
        )
    )
    cohort = column_property(
        func.jsonb_path_query_first(
            jsonb_blob,
            '$.forms[*].questions[*].fields[*] ? (@.key == "vYYoAC").answer',
        )
    )
    is_project_regional = column_property(
        func.jsonb_path_query_first(
            jsonb_blob,
            '$.forms[*].questions[*].fields[*] ? (@.key == "iqqqTk").answer',
        )
    )
    lead_contact_email = column_property(
        func.jsonb_path_query_first(
            jsonb_blob,
            '$.forms[*].questions[*].fields[*] ? (@.key == "IRugBv").answer',
        )
    )
    team_in_place = column_property(
        func.jsonb_path_query_first(
            jsonb_blob,
            '$.forms[*].questions[*].fields[*] ? (@.key == "vuZiab").answer',
        )
    )
    datasets = column_property(
        func.jsonb_path_query_first(
            jsonb_blob,
            '$.forms[*].questions[*].fields[*] ? (@.key == "BQKLZz").answer',
        )
    )
    publish_datasets = column_property(
        func.jsonb_path_query_first(
            jsonb_blob,
            '$.forms[*].questions[*].fields[*] ? (@.key == "WSaPbE").answer',
        )
    )
    lead_contact_email = column_property(
        func.jsonb_path_query_first(
            jsonb_blob,
            '$.forms[*].questions[*].fields[*] ? (@.key == "NQoGIm").answer',
        )
    )
    application_name = column_property(
        func.jsonb_path_query_first(
            jsonb_blob,
            '$.forms[*].questions[*].fields[*] ? (@.key == "qbBtUh").answer',
        )
    )
    joint_application = column_property(
        func.jsonb_path_query_first(
            jsonb_blob,
            '$.forms[*].questions[*].fields[*] ? (@.key == "luWnQp").answer',
        )
    )
    total_expected_cost = column_property(
        func.jsonb_path_query_first(
            jsonb_blob,
            '$.forms[*].questions[*].fields[*] ? (@.key == "lfXuaP").answer',
        )
    )
    date_submitted = column_property(func.jsonb_path_query_first(jsonb_blob, "$.date_submitted"))


Index(
    "ix_application_jsonb",
    AssessmentRecord.jsonb_blob,
    postgresql_ops={
        "jsonb_blob": "jsonb_path_ops",
    },
    postgresql_using="gin",
)

# This is very fast for "=" in WHERE clauses.
Index(
    "ix_application_id_hash",
    AssessmentRecord.application_id,
    postgresql_using="hash",
)

# Links the round_id and fund_id columns by an index.
Index(
    "ix_application_round_fund_id",
    AssessmentRecord.round_id,
    AssessmentRecord.fund_id,
)

Index(
    "ix_project_name",
    AssessmentRecord.project_name,
    postgresql_ops={
        "project_name": "gin_trgm_ops",
    },
    postgresql_using="gin",
)

Index(
    "ix_jsonb_blob_nURkuc",
    AssessmentRecord.jsonb_blob["nURkuc"],
    postgresql_using="gin",
)
