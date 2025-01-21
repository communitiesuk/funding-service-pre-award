import inspect
import os
from contextlib import contextmanager

from invoke import task

# Needed for invoke to work on python3.11
# Remove once invoke has been updated.
if not hasattr(inspect, "getargspec"):
    inspect.getargspec = inspect.getfullargspec


@contextmanager
def _env_var(key, value):
    old_val = os.environ.get(key, "")
    os.environ[key] = value
    yield
    os.environ[key] = old_val


def _echo_print(to_print):
    from colored import attr, fg, stylize

    ECHO_STYLE = fg("blue") + attr("bold")

    print(stylize(to_print, ECHO_STYLE))


def _error_print(to_print):
    from colored import attr, fg, stylize

    ECHO_STYLE = fg("red") + attr("bold")

    print(stylize(to_print, ECHO_STYLE))


def _echo_input(to_print):
    from colored import attr, fg, stylize

    ECHO_STYLE = fg("blue") + attr("bold")

    return input(stylize(to_print, ECHO_STYLE))


@task
def profile_pytest(c, testrows=100, resultsfile="profile.txt"):
    """Runs profiling during pytest to help find slow code."""

    if not resultsfile.endswith(".txt"):
        resultsfile = resultsfile.split(".")
        resultsfile = resultsfile[0] + ".txt"
    _echo_print("Profiling tests.")
    c.run(f"python -m cProfile -s tottime -m pytest > {resultsfile}")
    _echo_print(f"Results saved in f{resultsfile}")


@task
def reqs(c):
    """Runs the pip-compile commands in the correct order."""

    c.run("pip-compile requirements.in")
    c.run("pip-compile requirements-dev.in")
