import os
import sys
import logging
import csv

# Ensure the 'scripts' directory is added to the system path to find 'app'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, db
from app.models import Stat

logging.basicConfig(level=logging.INFO)

def add_stats_from_csv(file_path):
    with app.app_context():
        with open(file_path, newline='', encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';')
            headers = [header.strip() for header in reader.fieldnames]

            # Strip BOM from the first header if it exists
            if headers and headers[0].startswith('\ufeff'):
                headers[0] = headers[0][1:]

            for row in reader:
                row = {key.strip(): value.strip() for key, value in row.items()}
                existing_stat = Stat.query.filter_by(name=row['Name']).first()
                if not existing_stat:
                    new_stat = Stat(name=row['Name'], description=row['Description'])
                    db.session.add(new_stat)
                    logging.info(f"Added new stat: {row['Name']}")
                else:
                    logging.info(f"Stat already exists: {row['Name']}")

        db.session.commit()
        logging.info("S.P.E.C.I.A.L. stats added to the database.")

if __name__ == "__main__":
    # Update this path to your actual CSV file location
    file_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'stats.csv')

    try:
        add_stats_from_csv(file_path)
    except Exception as e:
        logging.error(f"Error adding stats to the database: {e}")
        sys.exit(1)
