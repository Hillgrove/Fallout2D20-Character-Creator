import os
import sys
import logging

# Ensure the 'scripts' directory is added to the system path to find 'app'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, db
from app.models import Attribute

logging.basicConfig(level=logging.INFO)

def add_attributes(attributes):
    with app.app_context():
        for attribute in attributes:
            existing_attribute = Attribute.query.filter_by(name=attribute["name"]).first()
            if not existing_attribute:
                new_attribute = Attribute(
                    name=attribute["name"],
                    description=attribute["description"]
                )
                db.session.add(new_attribute)
                logging.info(f"Added new attribute: {attribute['name']}")
            else:
                logging.info(f"Attribute already exists: {attribute['name']}")

        db.session.commit()
        logging.info("Attributes added to the database.")

if __name__ == "__main__":
    attributes = [
        {
            "name": "Tagged",
            "description": """A few of your skills are Tag skills, marking them as your areas of expertise. Tag skills represent a focused
training in those skills, a special affinity or talent with that discipline. 

Tag skills increase your chances of a critical success. When you use
a tagged skill, each d20 that rolls equal or under the skill rank is a critical success, scoring two successes instead of 1."""
        }
    ]

    try:
        add_attributes(attributes)
    except Exception as e:
        logging.error(f"Error adding attributes to the database: {e}")
        sys.exit(1)
