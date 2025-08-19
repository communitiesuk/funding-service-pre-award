from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Iterable

import click

from app import create_app
from pre_award.account_store.db.queries.queries import (
    upsert_account,
    upsert_account_role,
)
from pre_award.db import db

# --------------------------- Configuration --------------------------------- #

# Grants to seed
GRANTS: tuple[str, ...] = (
    "cof-eoi",
    "cof",
    "cof25",
    "cyp",
    "dpif",
    "nstf",
    "ctdf",
)

# Grants that also receive country-scoped roles
GRANTS_WITH_COUNTRIES: frozenset[str] = frozenset({"cof"})

# Countries used for country-scoped roles
COUNTRIES: tuple[str, ...] = (
    "ENGLAND",
    "SCOTLAND",
    "NORTHERNIRELAND",
    "WALES",
)

# Base roles to create accounts for (emails will be {grant}_{role}@example.com)
BASE_ROLES: tuple[str, ...] = ("lead_assessor", "assessor", "commenter")

# Role hierarchy: each base role implies these grant-scoped roles
ROLE_HIERARCHY: dict[str, set[str]] = {
    "LEAD_ASSESSOR": {"LEAD_ASSESSOR", "ASSESSOR", "COMMENTER"},
    "ASSESSOR": {"ASSESSOR", "COMMENTER"},
    "COMMENTER": {"COMMENTER"},
}


@dataclass(frozen=True)
class SeedPlan:
    grant: str
    base_role: str
    email: str
    full_name: str
    roles_to_assign: list[str]


# --------------------------- Helpers --------------------------------------- #


def build_roles(grant: str, base_role_upper: str, include_country_roles: bool) -> list[str]:
    """
    Build the list of role names to upsert for a given grant and base role.
    Includes grant-scoped roles from ROLE_HIERARCHY and optional country roles.
    """
    grant_uc = grant.upper()
    roles: set[str] = {f"{grant_uc}_{r}" for r in ROLE_HIERARCHY[base_role_upper]}

    if include_country_roles:
        roles.update(f"{grant_uc}_{country}" for country in COUNTRIES)

    return sorted(roles)


def build_seed_plans() -> list[SeedPlan]:
    plans: list[SeedPlan] = []
    for grant in GRANTS:
        include_countries = grant in GRANTS_WITH_COUNTRIES
        for base_role in BASE_ROLES:
            base_role_upper = base_role.upper()
            email = f"{grant}_{base_role}@example.com"
            full_name = f"{grant}_{base_role}"
            roles = build_roles(grant, base_role_upper, include_countries)
            plans.append(
                SeedPlan(
                    grant=grant,
                    base_role=base_role_upper,
                    email=email,
                    full_name=full_name,
                    roles_to_assign=roles,
                )
            )
    return plans


def upsert_roles_for_account(account, roles: Iterable[str]) -> None:
    for role_name in roles:
        role = upsert_account_role(account=account, role=role_name)
        print(f"ensured role: {role.role}")


# --------------------------- CLI ------------------------------------------- #

def seed_e2e_user_accounts() -> None:
    """
    Seed end-to-end test accounts and roles.

    For each grant in GRANTS:
      - Create an account per base role (lead_assessor, assessor, commenter)
      - Grant-scoped roles follow ROLE_HIERARCHY
      - Country-scoped roles are added for grants in GRANTS_WITH_COUNTRIES
    """

    plans = build_seed_plans()
    print(f"Prepared {len(plans)} account plan(s).")

    created_accounts = 0
    try:
        for plan in plans:
            print(f"Processing {plan.grant} / {plan.base_role} -> {plan.email}")

            account = upsert_account(email=plan.email, full_name=plan.full_name)
            created_accounts += 1
            print(f"ensured account id={account.id} email={plan.email}")

            upsert_roles_for_account(account, plan.roles_to_assign)

        db.session.commit()
        print(f"Done. {created_accounts} account(s) processed.")
    except Exception as ex:
        print(f"Unexpected error: {ex}")
        db.session.rollback()


# --------------------------- Entrypoint ------------------------------------- #

def main() -> None:
    env = os.getenv("FLASK_ENV")
    if env and env == "development" or env == "dev" or env == "test" or env == "uat":
        app = create_app()
        with app.app_context():
            seed_e2e_user_accounts()
    else:
        print("FLASK_ENV is mandatory and cannot run on production environment.")


if __name__ == "__main__":
    main()
