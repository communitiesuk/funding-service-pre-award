import argparse
import json
import os
import sys
from collections import defaultdict
from pathlib import Path

from sqlalchemy.sql import func

from pre_award.db import db
from pre_award.form_store.db.models.form_definition import FormDefinition


def load_json_files():
    """Load all JSON files from the form_jsons directory."""
    json_forms_dir = Path("../digital-form-builder-adapter/fsd_config/form_jsons")
    if not json_forms_dir.exists():
        print(f"Error: Directory {json_forms_dir} does not exist")
        sys.exit(1)
    files_by_name = defaultdict(list)
    for json_file in json_forms_dir.rglob("*.json"):
        files_by_name[json_file.name].append(json_file)
    return files_by_name


def insert_form_definitions(files_by_name):
    """Insert form definitions into the database."""
    inserted_count = 0
    skipped_count = 0

    for filename, file_paths in files_by_name.items():
        # Use the filename without extension as the name
        form_name = filename.replace(".json", "")

        # Check if form already exists
        existing_form = FormDefinition.query.filter_by(name=form_name).first()
        if existing_form:
            print(f"Skipping {form_name} - already exists")
            skipped_count += 1
            continue

        # Use the first file if there are duplicates
        json_file_path = file_paths[0]
        if len(file_paths) > 1:
            print(f"Warning: Multiple files found for {filename}, using {json_file_path}")

        try:
            # Load JSON content
            with open(json_file_path, "r", encoding="utf-8") as f:
                json_content = json.load(f)

            # Create new FormDefinition
            form_def = FormDefinition(
                name=form_name,
                published_at=func.now(),
                draft_json=json_content,
                published_json=json_content,
            )

            db.session.add(form_def)
            print(f"Added form definition: {form_name}")
            inserted_count += 1

        except Exception as e:
            print(f"Error processing {json_file_path}: {e}")
            continue

    try:
        db.session.commit()
        print(f"\nSuccessfully inserted {inserted_count} form definitions")
        print(f"Skipped {skipped_count} existing form definitions")
    except Exception as e:
        db.session.rollback()
        print(f"Error committing to database: {e}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Load JSON form definitions into database")
    parser.add_argument("database_url", help="Database connection string")
    args = parser.parse_args()

    # Create Flask app with the provided database URL
    os.environ["DATABASE_URL"] = args.database_url
    from app import create_app

    app = create_app()

    with app.app_context():
        print("Loading JSON files...")
        files_by_name = load_json_files()
        print(f"Found {sum(len(paths) for paths in files_by_name.values())} JSON files")

        print("Inserting form definitions...")
        insert_form_definitions(files_by_name)


if __name__ == "__main__":
    main()
