import os
import sys
import logging

# Ensure the 'scripts' directory is added to the system path to find 'app'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, db
from app.models import Stat

logging.basicConfig(level=logging.INFO)

def add_stats(stats):
    with app.app_context():
        for stat in stats:
            existing_stat = Stat.query.filter_by(name=stat["name"]).first()
            if not existing_stat:
                new_stat = Stat(name=stat["name"], description=stat["description"])
                db.session.add(new_stat)
                logging.info(f"Added new stat: {stat['name']}")
            else:
                logging.info(f"Stat already exists: {stat['name']}")

        db.session.commit()
        logging.info("S.P.E.C.I.A.L. stats added to the database.")

if __name__ == "__main__":
    stats = [
        {"name": "Strength", "description": "A measure of your raw physical power. It affects how much you can carry and the damage of all melee attacks."},
        {"name": "Perception", "description": "A measure of your environmental and situational awareness. It affects weapon accuracy in V.A.T.S."},
        {"name": "Endurance", "description": "A measure of your overall physical fitness. It affects your total Health and the Action Point drain from sprinting."},
        {"name": "Charisma", "description": "A measure of your ability to charm and convince others. It affects your success to persuade in dialogue and prices when you barter."},
        {"name": "Intelligence", "description": "A measure of your overall mental acuity. It affects the number of Experience Points earned."},
        {"name": "Agility", "description": "A measure of your overall finesse and reflexes. It affects the number of Action Points in V.A.T.S. and your ability to sneak."},
        {"name": "Luck", "description": "A measure of your general good fortune. It affects the recharge rate of Critical Hits."}
    ]

    try:
        add_stats(stats)
    except Exception as e:
        logging.error(f"Error adding stats to the database: {e}")
        sys.exit(1)
