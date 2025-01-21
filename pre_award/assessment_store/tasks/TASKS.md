# Helpful Dev Commands 👾

This module contains useful commands written using a framework called invoke. This framework allows you to write python functions and execute them from the console.

To execute any of the following, do the following:

1. Ensure that `invoke` is installed.
2. run`invoke {function name}`.

##  `bootstrap_dev_db`

Creates a database using the URL given by the `DATABASE_URL` env.

## `seed_dev_db`

Uses the `tests.conftest.seed_database` function to insert test data into your dev database.

## `create_seeded_db`

Executes the above commands in sequence to create a database with seeded data.

## `profile_pytest`

Profiles your code while running pytest. This is useful for seeing what python functions are not performant.

Results are saved to a `profile.txt` file in your working directory.

## `reqs`

Runs `pip-compile requirements.in` and `pip-compile requirements-dev.in` in that order.

## `generate_test_data`

Execute the above command to create test data into app.json
