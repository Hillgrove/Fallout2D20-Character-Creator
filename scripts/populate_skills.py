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

    # Athletics STR Lifting, pushing, pulling, jumping, running, and swimming
    # Barter CHA Buying and selling
    # Big Guns END Using heavy weapons such as miniguns, Fat Mans, and gatling lasers
    # Energy Weapons PER Using energy weapons such as laser guns, and plasma guns
    # Explosives PER Blowing things up, or stopping them from doing that
    # Lockpick PER Opening locks without the key
    # Medicine INT Healing people and stabilizing the dying
    # Melee Weapons STR Fighting people with bats, clubs, knives, boards, wrenches, and sledges
    # Pilot PER Flying and driving
    # Repair INT Fixing stuff, crafting things, and building machines
    # Science INT Hacking, programming, and brewing chems
    # Small Guns AGI Shooting people with pistols, rifles, and shotguns
    # Sneak AGI Moving quietly and staying hidden
    # Speech CHA Making friends, influencing people, and lying to them if you have to
    # Survival END Foraging, hunting, cooking, and enduring the wastes
    # Throwing AGI Launching weapons from your hands, like spears or knives
    # Unarmed STR Fighting without a weapon by making unarmed attacks

    try:
        add_skills(skills)
    except Exception as e:
        logging.error(f"Error adding skills to the database: {e}")
        sys.exit(1)
