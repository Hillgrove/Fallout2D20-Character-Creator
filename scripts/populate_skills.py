import os
import sys
import logging

# Ensure the 'scripts' directory is added to the system path to find 'app'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, db
from app.models import Skill

logging.basicConfig(level=logging.INFO)

def add_skills(skills):
    with app.app_context():
        for skill in skills:
            existing_skill = Skill.query.filter_by(name=skill["name"]).first()
            if not existing_skill:
                new_skill = Skill(name=skill["name"], description=skill["description"])
                db.session.add(new_skill)
                logging.info(f"Added new skill: {skill['name']}")
            else:
                logging.info(f"Skill already exists: {skill['name']}")

        db.session.commit()
        logging.info("Skills added to the database.")

if __name__ == "__main__":
    skills = [
        {"name": "Athletics", "description": "Physical fitness and agility."},
        {"name": "Barter", "description": "Negotiating and trading skills."},
        {"name": "Energy Weapons", "description": "Use of energy-based weapons."},
        {"name": "Explosives", "description": "Handling and deploying explosives."},
        {"name": "Guns", "description": "Proficiency with conventional firearms."},
        {"name": "Lockpick", "description": "Ability to pick locks."},
        {"name": "Medicine", "description": "Medical knowledge and healing."},
        {"name": "Melee Weapons", "description": "Proficiency with melee weapons."},
        {"name": "Repair", "description": "Repairing and maintaining equipment."},
        {"name": "Science", "description": "Scientific knowledge and research."},
        {"name": "Sneak", "description": "Ability to move quietly and remain unseen."},
        {"name": "Speech", "description": "Persuasion and communication skills."},
        {"name": "Survival", "description": "Wilderness survival skills."},
        {"name": "Unarmed", "description": "Hand-to-hand combat skills."}
    ]

    try:
        add_skills(skills)
    except Exception as e:
        logging.error(f"Error adding skills to the database: {e}")
        sys.exit(1)
