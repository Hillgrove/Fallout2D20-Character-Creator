
import os
import sys

# Ensure the 'scripts' directory is added to the system path to find 'app'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, db

with app.app_context():
    db.create_all()

print("Database initialzed.")