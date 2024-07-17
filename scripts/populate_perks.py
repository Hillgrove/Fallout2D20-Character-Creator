import os
import sys
import logging

# Ensure the 'scripts' directory is added to the system path to find 'app'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, db
from app.models import Perk

logging.basicConfig(level=logging.INFO)

def add_perks(perks):
    with app.app_context():
        for perk in perks:
            existing_perk = Perk.query.filter_by(name=perk["name"]).first()
            if not existing_perk:
                new_perk = Perk(
                    name=perk["name"],
                    description=perk["description"]
                )
                db.session.add(new_perk)
                logging.info(f"Added new perk: {perk['name']}")
            else:
                logging.info(f"Perk already exists: {perk['name']}")

        db.session.commit()
        logging.info("Perks added to the database.")

if __name__ == "__main__":
    perks = [
        {"name": "Iron Fist", "description": "Channel your chi to unleash devastating fury! Punching attacks do +20% damage."},
        {"name": "Big Leagues", "description": "Swing for the fences! Do +20% damage with melee weapons."},
        {"name": "Armorer", "description": "Protect yourself from the dangers of the Wasteland with access to base level and Rank 1 armor mods."},
        {"name": "Blacksmith", "description": "Fire up the forge and gain access to base level and Rank 1 melee weapon mods."},
        {"name": "Heavy Gunner", "description": "Thanks to practice and conditioning, heavy guns do +20% damage."},
        {"name": "Commando", "description": "Your automatic weapons now do +20% damage."},
        {"name": "Sneak", "description": "Become whisper, become shadow. You are 20% harder to detect while sneaking."},
        {"name": "Mister Sandman", "description": "As an agent of death itself, you can instantly kill a sleeping person."},
        {"name": "Hacker", "description": "Knowledge of cutting-edge computer encryption allows you to hack Advanced terminals."},
        {"name": "Locksmith", "description": "Your nimble fingers allow you to pick Advanced locks."}
    ]

    try:
        add_perks(perks)
    except Exception as e:
        logging.error(f"Error adding perks to the database: {e}")
        sys.exit(1)
