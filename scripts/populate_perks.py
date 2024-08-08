import os
import sys
import logging
import csv

# Ensure the 'scripts' directory is added to the system path to find 'app'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, db
from app.models import Perk, Stat

logging.basicConfig(level=logging.INFO)

def add_perks_from_csv(file_path):
    with app.app_context():
        with open(file_path, newline='', encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';')
            headers = [header.strip() for header in reader.fieldnames]

            # Strip BOM from the first header if it exists
            if headers and headers[0].startswith('\ufeff'):
                headers[0] = headers[0][1:]

            for row in reader:
                row = {key.strip(): value.strip() for key, value in row.items()}
                stat_1 = Stat.query.filter_by(name=row['stat 1']).first() if row.get('stat 1') else None
                stat_2 = Stat.query.filter_by(name=row['stat 2']).first() if row.get('stat 2') else None

                new_perk = Perk(
                    name=row['Name'],
                    description=row['description'],
                    stat_1=stat_1,
                    amount_1=int(row['amount 1']) if row.get('amount 1') else None,
                    stat_2=stat_2,
                    amount_2=int(row['amount 2']) if row.get('amount 2') else None,
                    mutual_exclusive=row['mutual exclusive']
                )
                existing_perk = Perk.query.filter_by(name=row['Name']).first()
                if not existing_perk:
                    db.session.add(new_perk)
                    logging.info(f"Added new perk: {row['Name']}")
                else:
                    existing_perk.description = new_perk.description
                    existing_perk.stat_1 = new_perk.stat_1
                    existing_perk.amount_1 = new_perk.amount_1
                    existing_perk.stat_2 = new_perk.stat_2
                    existing_perk.amount_2 = new_perk.amount_2
                    existing_perk.mutual_exclusive = new_perk.mutual_exclusive
                    logging.info(f"Updated existing perk: {row['Name']}")

        db.session.commit()
        logging.info("Perks added/updated in the database.")

if __name__ == "__main__":
    # Update this path to your actual CSV file location
    file_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'perks.csv')

    try:
        add_perks_from_csv(file_path)
    except Exception as e:
        logging.error(f"Error adding perks to the database: {e}")
        sys.exit(1)
