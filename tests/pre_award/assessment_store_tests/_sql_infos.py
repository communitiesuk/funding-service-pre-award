import datetime
import os
from collections import defaultdict
from statistics import mean

from rich import print as fancy_print
from rich.syntax import Syntax
from rich.text import Text
from sqlalchemy import event
from sqlalchemy.engine import Engine

from pre_award.config import Config
from pre_award.db import db

query_info = {
    "queries_types": defaultdict(int),
    "slow_queries": [],
    "query_times": [],
}


def attach_listeners():
    @event.listens_for(db.Session, "do_orm_execute")
    def receive_do_orm_execute(orm_execute_state):
        if orm_execute_state.is_select:
            query_info["queries_types"]["selects"] = +1
        if orm_execute_state.is_insert:
            query_info["queries_types"]["inserts"] = +1

    @event.listens_for(Engine, "before_cursor_execute")
    def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
        conn.info.setdefault("query_start_time", []).append(datetime.datetime.now())

    @event.listens_for(Engine, "after_cursor_execute")
    def after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
        time_for_query = datetime.datetime.now() - conn.info["query_start_time"].pop(-1)

        ignores = ["--IGNORE", "SAVEPOINT"]

        # PYTEST_CURRENT_TEST contains the current test running and its state.
        # (setup, call, teardown)
        if "call" in os.environ["PYTEST_CURRENT_TEST"] and not any(ignore in statement for ignore in ignores):
            if time_for_query.microseconds / 1000 > Config.WARN_IF_QUERIES_OVER_MS:
                query_info["slow_queries"].append(
                    {
                        "statement": statement,
                        "time": time_for_query.microseconds / 1000,
                        "during": os.environ["PYTEST_CURRENT_TEST"],
                    }
                )
            query_info["query_times"].append(
                {
                    "statement": statement,
                    "time": time_for_query.microseconds / 1000,
                    "during": os.environ["PYTEST_CURRENT_TEST"],
                }
            )


def pytest_terminal_summary(terminalreporter):
    terminalreporter.section("Database test information")

    database_url = Config.SQLALCHEMY_DATABASE_URI
    terminalreporter.write_line(f"Database URL: {database_url}")

    terminalreporter.section("SQL Query information")
    query_times = [query["time"] for query in query_info["query_times"]]
    terminalreporter.write_line(f"Average query time: {round(mean(query_times or [0]), 3)}")

    if query_info["slow_queries"] != []:
        terminalreporter.write_line("Slow queries found!")

        for query in query_info["slow_queries"]:
            statement_string = Text("Statement:", style="bold underline magenta")
            time_string = Text("Time: ", style="bold blue")
            during_string = Text("During: ", style="bold green")

            statement = Syntax(query["statement"], "sql", theme="autumn", dedent=True)

            time = Text(f"{query['time']}", style="italic black")
            time_string.append(time)

            during = Text(f"{query['during']}", style="italic black")
            during_string.append(during)

            fancy_print(statement_string)
            fancy_print(statement)
            fancy_print(time_string)
            fancy_print(during_string)

    for query in query_info["query_times"]:
        statement_string = Text("Statement:", style="bold underline    magenta")
        time_string = Text("Time: ", style="bold blue")
        during_string = Text("During: ", style="bold green")

        statement = Syntax(
            query["statement"],
            "sql",
            theme="xcode",
            dedent=True,
            background_color="default",
        )
        time = Text(f"{query['time']}", style="italic black")

        time_string.append(time)

        during = Text(f"{query['during']}", style="italic black")
        during_string.append(during)

        fancy_print(statement_string)
        fancy_print(statement)
        fancy_print(time_string)
        fancy_print(during_string)
