import os
import sys
import logging
import csv
import json

# Ensure the 'scripts' directory is added to the system path to find 'app'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, db
from app.models import Trait

logging.basicConfig(level=logging.INFO)

def add_traits_from_csv(file_path):
    with app.app_context():
        with open(file_path, newline='', encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';')
            headers = [header.strip() for header in reader.fieldnames]

            # Strip BOM from the first header if it exists
            if headers and headers[0].startswith('\ufeff'):
                headers[0] = headers[0][1:]

            for row in reader:
                row = {key.strip(): value.strip() for key, value in row.items()}
                trait_data = json.loads(row['Trait Data']) if row.get('Trait Data') else {}
                is_selectable = row.get('Is Selectable', 'False').lower() in ['true', '1', 'yes']

                existing_trait = Trait.query.filter_by(name=row['Name']).first()
                if not existing_trait:
                    new_trait = Trait(
                        name=row['Name'],
                        description=row['Description'],
                        trait_data=trait_data,
                        is_selectable=is_selectable
                    )
                    db.session.add(new_trait)
                    logging.info(f"Added new trait: {row['Name']}")
                else:
                    logging.info(f"Trait already exists: {row['Name']}")
        
        db.session.commit()
        logging.info("Traits added to the database.")

if __name__ == "__main__":
    # Update this path to your actual CSV file location
    file_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'traits.csv')

    try:
        add_traits_from_csv(file_path)
    except Exception as e:
        logging.error(f"Error adding traits to the database: {e}")
        sys.exit(1)
