
import os
import sys

# Ensure the 'scripts' directory is added to the system path to find 'app'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, db
from app.models import Attribute

# Use the Flask application context
with app.app_context():
    attributes = [
        {
            "name": "Tagged",
            "description": """A few of your skills are Tag skills, marking them as your areas of expertise. Tag skills represent a focused
training in those skills, a special affinity or talent with that discipline. 

Tag skills increase your chances of a critical success. When you use
a tagged skill, each d20 that rolls equal or under the skill rank is a critical success, scoring two successes instead of 1."""
        }
    ]

    for attribute in attributes:
        existing_attribute = Attribute.query.filter_by(name=attribute["name"]).first()
        if not existing_attribute:
            new_attribute = Attribute(name=attribute["name"], description=attribute["description"])
            db.session.add(new_attribute)

    db.session.commit()
    print("Attributes added to the database.")
