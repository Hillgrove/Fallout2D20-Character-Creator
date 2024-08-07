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
        {"name": "Athletics", "description": "Lifting, pushing, pulling, jumping, running, and swimming"},
        {"name": "Barter", "description": "Buying and selling"},
        {"name": "Big Guns", "description": "Using heavy weapons such as miniguns, Fat Mans, and gatling lasers"},
        {"name": "Energy Weapons", "description": "Using energy weapons such as laser guns, and plasma guns"},
        {"name": "Explosives", "description": "Blowing things up, or stopping them from doing that"},
        {"name": "Lockpick", "description": "Opening locks without the key"},        
        {"name": "Medicine", "description": "Healing people and stabilizing the dying"},
        {"name": "Melee Weapons", "description": "Fighting people with bats, clubs, knives, boards, wrenches, and sledges"},
        {"name": "Pilot", "description": "Flying and driving"},
        {"name": "Repair", "description": "Fixing stuff, crafting things, and building machines"},
        {"name": "Small Guns", "description": "Shooting people with pistols, rifles, and shotguns"},
        {"name": "Science", "description": "Hacking, programming, and brewing chems"},
        {"name": "Sneak", "description": "Moving quietly and staying hidden"},
        {"name": "Speech", "description": "Making friends, influencing people, and lying to them if you have to"},
        {"name": "Survival", "description": "Foraging, hunting, cooking, and enduring the wastes"},
        {"name": "Throwing", "description": "Launching weapons from your hands, like spears or knives"},
        {"name": "Unarmed", "description": "Hand-to-hand combat skills."}
    ]

    try:
        add_skills(skills)
    except Exception as e:
        logging.error(f"Error adding skills to the database: {e}")
        sys.exit(1)
