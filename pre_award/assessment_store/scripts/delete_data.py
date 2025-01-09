#!/usr/bin/env python3
from datetime import datetime

import click

from pre_award.assessment_store.db.models.assessment_record import AssessmentRecord, TagAssociation
from pre_award.assessment_store.db.models.comment import Comment, CommentsUpdate
from pre_award.assessment_store.db.models.flags import AssessmentFlag, FlagUpdate
from pre_award.assessment_store.db.models.qa_complete import QaComplete
from pre_award.assessment_store.db.models.score import Score
from pre_award.db import db


def delete_single_assessment(application_id: str, do_commit: bool = False):
    assessment_record = (
        db.session.query(AssessmentRecord).where(AssessmentRecord.application_id == application_id).one_or_none()
    )
    if assessment_record:
        print(f"{datetime.now()} Starting to delete assessment record {application_id}")
        tags_deleted = db.session.query(TagAssociation).filter(TagAssociation.application_id == application_id).delete()
        print(f"\tDeleted {tags_deleted} tags")
        scores_deleted = db.session.query(Score).filter(Score.application_id == application_id).delete()
        print(f"\tDeleted {scores_deleted} scores")
        qa_completed_deleted = db.session.query(QaComplete).filter(QaComplete.application_id == application_id).delete()
        print(f"\tDeleted {qa_completed_deleted} scores")

        associated_flags = db.session.query(AssessmentFlag).filter(AssessmentFlag.application_id == application_id)
        if associated_flags.count() > 0:
            print(f"\tDeleting {associated_flags.count()} flags")
            db.session.query(FlagUpdate).filter(
                FlagUpdate.assessment_flag_id.in_(
                    db.session.query(AssessmentFlag.id).filter(AssessmentFlag.application_id == application_id)
                )
            ).delete()
            associated_flags.delete()

        comments = db.session.query(Comment).filter(Comment.application_id == application_id)
        if comments.count() > 0:
            print(f"\tDeleting {comments.count()} comments")
            db.session.query(CommentsUpdate).filter(
                CommentsUpdate.comment_id.in_(
                    db.session.query(Comment.id).filter(Comment.application_id == application_id)
                )
            ).delete()
            comments.delete()
        db.session.delete(assessment_record)
        if do_commit:
            db.session.commit()
        print(f"{datetime.now()} Deleted assessment record with application id {application_id}")
    else:
        print(f"No assessment record exists with application id {application_id}")


@click.group()
@click.option("-q", help="Do not prompt for confirmation", flag_value=True, default=False)
@click.pass_context
def cli(ctx, q):
    # Ensure that ctx.obj exists and is a dict
    ctx.ensure_object(dict)
    # Apply group-wide feature switches
    ctx.obj["q"] = q


@cli.command()
@click.option("-id", prompt=True)
@click.option(
    "-c",
    "--do-commit",
    flag_value=True,
    default=False,
    help="Whether to commit changes to DB",
)
@click.pass_context
def delete_assessment_record(ctx, id, do_commit):
    """Deletes a single assessment record, along with child records (tags,
    comments, scores, flags)"""
    print(f"Record with application id {id} will be deleted, {'and committed' if do_commit else 'but not committed'}")
    q = ctx.obj.get("q")
    if q or (not q and click.confirm("Do you want to continue?")):
        delete_single_assessment(id, do_commit)


@cli.command()
@click.option("-r", "--round-id", prompt=True)
@click.option(
    "-c",
    "--do-commit",
    flag_value=True,
    default=False,
    help="Whether to commit changes to DB",
)
@click.pass_context
def delete_all_assessments_in_round(ctx, round_id, do_commit):
    """Deletes all assessment records in a round, along with their child records
    (tags, comments, scores, flags)"""
    results = db.session.query(AssessmentRecord.application_id).filter(AssessmentRecord.round_id == round_id)
    if results.count() > 0:
        print(f"Found {results.count()} assessments to delete")
        print(f"These deletes will{'' if do_commit else ' not'} be committed to the database")
        q = ctx.obj.get("q")
        if q or (not q and click.confirm("Do you want to continue?")):
            for r in results.all():
                delete_single_assessment(str(r[0]), do_commit)
        print(f"These deletes WERE{'' if do_commit else ' NOT'} committed to the database")

    else:
        print(f"No assessments found for round {round_id}")


if __name__ == "__main__":
    from app import create_app

    app = create_app()
    from pre_award.config import Config

    with app.app_context():
        if Config.FLASK_ENV.casefold() == "production":
            print("Will not run in production")
            exit(1)
        cli()
