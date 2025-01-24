import glob
import os
import re
from contextlib import contextmanager

from alembic import command
from alembic.config import Config
from invoke import task

from app import create_app
from pre_award.account_store.db.models.queries import get_email_address
from pre_award.account_store.tasks import seed_local_account_store_impl
from pre_award.application_store.db.queries.application.queries import search_applications
from pre_award.apply.models.round import Round
from pre_award.assessment_store.tasks.db_tasks import seed_assessment_store_db_impl
from pre_award.fund_store.db.queries import (
    get_rounds_where_reminder_date_today,
    get_rounds_with_reminder_date_in_future,
)
from pre_award.fund_store.scripts.fund_round_loaders.load_fund_round_from_fab import load_fund_from_fab_impl
from pre_award.fund_store.scripts.load_all_fund_rounds import load_all_fund_rounds
from services.notify import get_notification_service

_VALID_JINJA_EXTENSIONS = (".html", ".jinja", ".jinja2", ".j2")


def _remove_whitespace_newlines_from_trans_tags(file, content: str):
    matches = re.findall(r"({%\s*trans\s*%}(.|[\S\s]*?){%\s*endtrans\s*%})", content)

    content_replaced = content
    for outer, center in matches:
        normalised_whitespace_trans = re.sub(r"\s+", " ", center).strip()

        outer_replaced = outer.replace(center, normalised_whitespace_trans)

        rwhitespace = center[len(center.rstrip()) :]  # noqa: E203
        lwhitespace = center[: len(center) - len(center.lstrip())]

        outer_replaced_whitespace = lwhitespace + outer_replaced + rwhitespace
        content_replaced = content_replaced.replace(outer, outer_replaced_whitespace)

    if content != content_replaced:
        with open(file, "w") as f:
            f.write(content_replaced)
        print(f"Removed newlines/tabs from {file}")
    else:
        print(f"No newlines/tabs to remove from {file}")

    return 0


def _find_missing_translations(file, content: str):
    matches = list(
        re.findall(
            r"(msgid (?:\".*\"\n)+)(?=msgstr" r" \"\"(?!\n\")\n*(?=\n|msgid|\"\"))",
            content,
        )
    )

    missing_translations = []
    for match in matches:
        original = "".join(re.findall(r"\"(.*)\"", match))
        missing_translations.append(original)

    # echo missing translations to stdout with a newline between each
    if missing_translations:
        print(f"Missing translations in {file}:")
        for translation in missing_translations:
            print(f"  {translation}")
        print()
    else:
        print(f"No missing translations in {file}")

    return 0


def _process_file(file: str, function: callable):
    with open(file, "r") as f:
        content = f.read()
    return function(file, content)


def _traverse_files(path: str, function: callable, extensions: tuple[str]):
    ret = 0

    if os.name == "nt":
        path = path.replace("/", "\\")

    filepath = os.path.join(os.getcwd(), path)
    if os.path.isfile(filepath) and filepath.endswith(extensions):
        ret |= _process_file(filepath, function)

    for full_filepath in glob.glob(filepath + "/**", recursive=True):
        if full_filepath.endswith(extensions):
            ret |= _process_file(full_filepath, function)

    return ret


@task
def fix_trans_tags(_, path="apply/templates"):
    return _traverse_files(
        path,
        _remove_whitespace_newlines_from_trans_tags,
        _VALID_JINJA_EXTENSIONS,
    )


@task
def find_missing_trans(_, path="translations/cy/LC_MESSAGES/messages.po"):
    return _traverse_files(path, _find_missing_translations, (".po",))


@task
def pybabel_extract(c):
    c.run("pybabel extract -F babel.cfg -o messages.pot .")


@task
def pybabel_update(c):
    c.run("pybabel update -i messages.pot -d translations")


@task
def pybabel_compile(c):
    c.run("pybabel compile -d translations")


@task
def reminder_emails(c):
    print("Building!")
    app = create_app()
    with app.app_context():
        print("IN APP CONTEXT")
        rounds: list[Round] = get_rounds_with_reminder_date_in_future()
        print([round.reminder_date for round in rounds])
        rounds_with_reminder_today = get_rounds_where_reminder_date_today()
        for r in rounds_with_reminder_today:
            non_submitted_applications = search_applications(
                round_id=str(r.id), status_only=["IN_PROGRESS", "NOT_STARTED", "COMPLETED"], forms=False
            )
            for a in non_submitted_applications:
                email_address = get_email_address(a["account_id"])
                print(email_address)
                print(r.fund)
                breakpoint()
                get_notification_service().send_application_deadline_reminder_email(
                    email_address=email_address,
                    fund_name=r.fund,
                    application_reference=a["reference"],
                    round_name=r.title_json["en"],
                    deadline=r.deadline,
                    contact_help_email=r.contact_email,
                )
                # current_app.logger.info(
                #     "Sent notification %(notification_id)s for application %(application_reference)s",
                #     dict(
                #         notification_id=notification.id,
                #         application_reference=application["application"]["reference"],
                #     ),


@task
def full_bootstrap(c):
    @contextmanager
    def _env_var(key, value):
        old_val = os.environ.get(key, "")
        os.environ[key] = value
        yield
        os.environ[key] = old_val

    with _env_var("FLASK_ENV", "development"):
        with create_app().app_context():
            alembic_cfg = Config("pre_award/db/migrations/alembic.ini")
            alembic_cfg.set_main_option("script_location", "pre_award/db/migrations")
            command.upgrade(alembic_cfg, "head")

            load_all_fund_rounds()
            load_fund_from_fab_impl(seed_all_funds=True)
            seed_assessment_store_db_impl("local")
            seed_local_account_store_impl()
