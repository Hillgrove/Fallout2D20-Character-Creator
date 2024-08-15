import os
import sys
import logging
import csv
import ast

# Ensure the 'scripts' directory is added to the system path to find 'app'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, db
from app.models import Origin, Trait, OriginTrait

logging.basicConfig(level=logging.INFO)

def add_origin_and_traits_from_csv(file_path):
    with app.app_context():
        with open(file_path, newline='', encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';')
            headers = [header.strip() for header in reader.fieldnames]

            # Strip BOM from the first header if it exists
            if headers and headers[0].startswith('\ufeff'):
                headers[0] = headers[0][1:]

            for row in reader:
                row = {key.strip(): value.strip() for key, value in row.items()}
                existing_origin = Origin.query.filter_by(name=row['name']).first()

                if not existing_origin:
                    new_origin = Origin(
                        name=row['name'],
                        description=row['description'],
                        selectable_traits_limit=int(row['selectable_traits_limit']) if row.get('selectable_traits_limit') else 0
                    )
                    db.session.add(new_origin)
                    db.session.commit()  # Commit to get the new origin's id

                    # Evaluate the traits string as a Python list
                    traits = ast.literal_eval(row['traits'])
                    for trait_name in traits:
                        existing_trait = Trait.query.filter_by(name=trait_name).first()
                        if existing_trait:
                            origin_trait = OriginTrait(
                                origin_id=new_origin.id,
                                trait_id=existing_trait.id
                            )
                            db.session.add(origin_trait)
                            logging.info(f"Added trait '{trait_name}' to origin '{new_origin.name}'")
                        else:
                            logging.warning(f"Trait '{trait_name}' does not exist and was not added to origin '{new_origin.name}'")

                    db.session.commit()
                    logging.info(f"Added new origin: {row['name']}")
                else:
                    logging.info(f"Origin '{row['name']}' already exists in the database.")

if __name__ == "__main__":
    file_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'origins.csv')

    try:
        add_origin_and_traits_from_csv(file_path)
    except Exception as e:
        logging.error(f"Error adding origins and traits to the database: {e}")
        sys.exit(1)
