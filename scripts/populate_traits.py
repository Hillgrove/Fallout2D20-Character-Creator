import os
import sys
import logging

# Ensure the 'scripts' directory is added to the system path to find 'app'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, db
from app.models import Trait

logging.basicConfig(level=logging.INFO)

def add_traits(traits):
    with app.app_context():
        for trait_data in traits:
            existing_trait = Trait.query.filter_by(name=trait_data["name"]).first()
            if not existing_trait:
                new_trait = Trait(
                    name=trait_data["name"],
                    description=trait_data["description"],
                    trait_data=trait_data["trait_data"],
                    is_selectable=trait_data.get("is_selectable", False)
                )
                db.session.add(new_trait)
                logging.info(f"Added new trait: {trait_data['name']}")
            else:
                logging.info(f"Trait already exists: {trait_data['name']}")
        
        db.session.commit()
        logging.info("Traits added to the database.")

def populate_traits():
    traits = [
        {"name": "Example Trait", "description": "This is an example trait.", "trait_data": {"example_key": "example_value"}},
        {"name": "Strength Max", "description": "Strength can be raised to a max of 12.", "trait_data": {"stat": "Strength", "max": 12}},
        {"name": "Endurance Max", "description": "Endurance can be raised to a max of 12.", "trait_data": {"stat": "Endurance", "max": 12}},
        {"name": "Charisma Max", "description": "Charisma can be raised to a max of 6.", "trait_data": {"stat": "Charisma", "max": 6}},
        {"name": "Intelligence Max", "description": "Intelligence can be raised to a max of 6.", "trait_data": {"stat": "Intelligence", "max": 6}},
        {"name": "Educated", "description": "You have one additional tag skill.", "trait_data": {"bonus": "extra_tag_skill"}, "is_selectable": True},
        {"name": "Fast Shot", "description": "If you take a second major action in combat, and use it to make a ranged attack, the additional major action only costs 1 AP, rather than 2.", "trait_data": {}, "is_selectable": True},
        {"name": "Gifted", "description": "Choose two S.P.E.C.I.A.L. attributes and increase them by +1 each.", "trait_data": {"bonus": "extra_special_points", "amount": 2}, "is_selectable": True},
        {"name": "Heavy Handed", "description": "Your Melee Damage bonus increases by +1 CD", "trait_data": {"bonus": "melee_damage", "amount": 1}, "is_selectable": True},
        {"name": "Small Frame", "description": "You may re-roll 1d20 on all AGI tests which rely on balance or contortion.", "trait_data": {}, "is_selectable": True},
        {"name": "Extra Perk", "description": "1 more perk", "trait_data": {"bonus": "extra_perk"}, "is_selectable": True},
        {"name": "Reduced END Test Difficulty", "description": "Reduces the difficulty of all END tests to resist the effects of disease.", "trait_data": {"effect": "reduce_END_test_difficulty"}, "is_selectable": False},
        {"name": "Luck Point Recovery", "description": "Once per quest, the GM may introduce a complication related to your early life of isolation and confinement within the Vault. If the GM does this, you immediately regain one Luck Point.", "trait_data": {"effect": "luck_point_recovery"}, "is_selectable": False},
        {"name": "Additional Tag Skill", "description": "Your carefully-planned upbringing means you have one additional tag skill of your choice.", "trait_data": {"bonus": "additional_tag_skill"}, "is_selectable": False}
    ]

    add_traits(traits)

if __name__ == '__main__':
    try:
        populate_traits()
    except Exception as e:
        logging.error(f"Error populating traits: {e}")
        sys.exit(1)
