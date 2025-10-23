import argparse
import json
import os
import re
import sys
from collections import defaultdict
from pathlib import Path

from sqlalchemy.sql import func

from pre_award.db import db
from pre_award.form_store.db.models.form_definition import FormDefinition
from pre_award.fund_store.db.models.form_name import FormName
from pre_award.fund_store.db.models.section import Section


def strip_leading_digits(text: str) -> str:
    """Strip section numbering patterns like '1.1. ' or '2. ' or '1 ' from section titles."""
    parts = text.split()
    if not parts:
        return text

    first_part = parts[0]
    # Check if first part consists only of digits and dots
    if re.match(r"^[\d.]+$", first_part):
        return " ".join(parts[1:])

    return text


def get_display_name_from_section(url_path: str) -> str | None:
    """Get display name from section table via form_name join, checking both English and Welsh."""
    # First try to match on English
    result = (
        db.session.query(Section.title_json)
        .join(FormName, FormName.section_id == Section.id)
        .filter(func.json_extract_path_text(FormName.form_name_json, "en") == url_path)
        .first()
    )

    if result and result.title_json:
        # Extract the English title and strip leading digits
        title = result.title_json.get("en", "")
        if title:
            return strip_leading_digits(title)

    # If no English match found, try Welsh
    result = (
        db.session.query(Section.title_json)
        .join(FormName, FormName.section_id == Section.id)
        .filter(func.json_extract_path_text(FormName.form_name_json, "cy") == url_path)
        .first()
    )

    if result and result.title_json:
        # Extract the Welsh title and strip leading digits
        title = result.title_json.get("cy", "")
        if title:
            return strip_leading_digits(title)

    return None


def load_json_files() -> dict[str, list[Path]]:
    """Load all JSON files from the form_jsons directory."""
    json_forms_dir = Path("../digital-form-builder-adapter/fsd_config/form_jsons")
    if not json_forms_dir.exists():
        print(f"Error: Directory {json_forms_dir} does not exist")
        sys.exit(1)
    files_by_name = defaultdict(list)
    for json_file in json_forms_dir.rglob("*.json"):
        files_by_name[json_file.name].append(json_file)
    return files_by_name


def update_or_create_form(url_path: str, json_content: dict = None) -> str:
    """
    Update or create a single form definition.
    Returns status: 'inserted', 'updated', 'skipped', or 'error'
    """
    try:
        # Get display name from section table
        display_name = get_display_name_from_section(url_path)

        # Check if form already exists
        existing_form = FormDefinition.query.filter_by(url_path=url_path).first()

        if existing_form:
            # Update existing form with display_name if it's missing
            if not existing_form.display_name:
                if not display_name:
                    print(f"Skipping {url_path} - form exists but no display_name could be retrieved")
                    return "skipped"
                else:
                    existing_form.display_name = display_name
                    existing_form.updated_at = func.now()
                    print(f"Updated {url_path} - display_name set to {display_name}")
                    return "updated"
            else:
                print(f"Skipping {url_path} - form exists and already has display_name")
                return "skipped"
        else:
            # Create new FormDefinition only if we have JSON content
            if json_content is None:
                print(f"Skipping {url_path} - no JSON content provided for new form")
                return "skipped"

            form_def = FormDefinition(
                url_path=url_path,
                display_name=display_name or url_path.replace("-", " ").capitalize(),
                published_at=func.now(),
                draft_json=json_content,
                published_json=json_content if not url_path.startswith("nwp-r1") else {},
            )
            db.session.add(form_def)
            print(
                f"Added form definition: {url_path}" + (f" with display_name: {display_name}" if display_name else "")
            )
            return "inserted"

    except Exception as e:
        print(f"Error processing {url_path}: {e}")
        return "error"


def process_forms(files_by_name: dict[str, list[Path]] | None = None, update_orphans: bool = False) -> None:
    """
    Process form definitions - either from JSON files or update orphaned forms in DB.
    """
    stats = {"inserted": 0, "updated": 0, "skipped": 0, "error": 0}
    processed_url_paths = set()  # Track which forms we've already processed

    # Process forms from JSON files if provided
    if files_by_name:
        for filename, file_paths in files_by_name.items():
            # Use the filename without extension as the url_path
            form_url_path = filename.replace(".json", "")
            processed_url_paths.add(form_url_path)  # Mark as processed

            # Use the first file if there are duplicates
            json_file_path = file_paths[0]
            if len(file_paths) > 1:
                print(f"Warning: Multiple files found for {filename}, using {json_file_path}")

            try:
                # Load JSON content
                with open(json_file_path, "r", encoding="utf-8") as f:
                    json_content = json.load(f)

                status = update_or_create_form(form_url_path, json_content)
                stats[status] += 1

            except Exception as e:
                print(f"Error loading {json_file_path}: {e}")
                stats["error"] += 1

    # Process orphaned forms (those without display_name) if requested
    if update_orphans:
        print("\nUpdating orphaned forms without display_name...")
        forms_without_display = FormDefinition.query.filter(
            (FormDefinition.display_name == None) | (FormDefinition.display_name == "")  # noqa: E711
        ).all()

        for form in forms_without_display:
            # Skip if we already processed this form from JSON files
            if form.url_path in processed_url_paths:
                print(f"Skipping {form.url_path} - already processed from JSON files")
                continue

            status = update_or_create_form(form.url_path)
            stats[status] += 1

    # Commit all changes
    try:
        db.session.commit()
        print("\nResults:")
        print(f"  Inserted: {stats['inserted']} form definitions")
        print(f"  Updated: {stats['updated']} form definitions")
        print(f"  Skipped: {stats['skipped']} form definitions")
        if stats["error"] > 0:
            print(f"  Errors: {stats['error']} form definitions")
    except Exception as e:
        db.session.rollback()
        print(f"Error committing to database: {e}")
        sys.exit(1)


def main() -> None:
    parser = argparse.ArgumentParser(description="Load JSON form definitions into database")
    parser.add_argument("database_url", help="Database connection string")
    parser.add_argument(
        "--upsert-from-fsd-config",
        action="store_true",
        help="Load form JSON files from ../digital-form-builder-adapter/fsd_config/form_jsons directory",
    )
    parser.add_argument(
        "--update-orphans",
        action="store_true",
        help="Also update display_name for forms without corresponding JSON files",
    )
    args = parser.parse_args()

    # Create Flask app with the provided database URL
    os.environ["DATABASE_URL"] = args.database_url
    from app import create_app

    app = create_app()

    with app.app_context():
        print("Loading JSON files...")
        files_by_name = load_json_files() if args.upsert_from_fsd_config else {}
        print(f"Found {sum(len(paths) for paths in files_by_name.values())} JSON files")

        print("\nProcessing form definitions...")
        process_forms(files_by_name, update_orphans=args.update_orphans)


if __name__ == "__main__":
    main()
