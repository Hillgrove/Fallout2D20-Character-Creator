import os
import sys
import logging

# Ensure the 'scripts' directory is added to the system path to find 'app'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, db

logging.basicConfig(level=logging.INFO)

def initialize_database():
    try:
        with app.app_context():
            db.create_all()
            logging.info("Database initialized successfully.")
    except Exception as e:
        logging.error(f"Error initializing the database: {e}")
        sys.exit(1)

if __name__ == "__main__":
    initialize_database()
