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
        {"name": "Educated", "description": "You have one additional tag skill.", "trait_data": {"extra_tag_skills": 1}, "is_selectable": True},
        {"name": "Fast Shot", "description": "If you take a second major action in combat, and use it to make a ranged attack, the additional major action only costs 1 AP, rather than 2.", "trait_data": {}, "is_selectable": True},
        {"name": "Gifted", "description": "Choose two S.P.E.C.I.A.L. attributes and increase them by +1 each.", "trait_data": {"extra_special_points": 2}, "is_selectable": True},
        {"name": "Heavy Handed", "description": "Your Melee Damage bonus increases by +1 CD", "trait_data": {"extra_melee_damage": 1}, "is_selectable": True},
        {"name": "Small Frame", "description": "You may re-roll 1d20 on all AGI tests which rely on balance or contortion.", "trait_data": {}, "is_selectable": True},
        {"name": "Extra Perk", "description": "1 more perk", "trait_data": {"extra_perks": 1}, "is_selectable": True},
        {"name": "Reduced END Test Difficulty", "description": "Reduces the difficulty of all END tests to resist the effects of disease.", "trait_data": {}, "is_selectable": False},
        {"name": "Luck Point Recovery", "description": "Once per quest, the GM may introduce a complication related to your early life of isolation and confinement within the Vault. If the GM does this, you immediately regain one Luck Point.", "trait_data": {}, "is_selectable": False},
        {"name": "Additional Tag Skill", "description": "Your carefully-planned upbringing means you have one additional tag skill of your choice.", "trait_data": {"extra_tag_skills": 1}, "is_selectable": False},
        {"name": "Tag Energy Weapons", "description": "Free tag in Energy Weapons", "trait_data": {"tag": "Energy Weapons"}, "is_selectable": True},
        {"name": "Tag Repair", "description": "Free tag in Repair", "trait_data": {"tag": "Repair"}, "is_selectable": True},
        {"name": "Tag Science", "description": "Free tag in Science", "trait_data": {"tag": "Science"}, "is_selectable": True},
        {"name": "Rad Healing", "description": "You regain 1 HP for every 3 points of radiation damage inflicted upon you.", "trait_data": {}, "is_selectable": False},
        {"name": "Rad Resting", "description": "When resting in an irradiated location, you may re-roll your dice pool when checking if your injuries heal", "trait_data": {}, "is_selectable": False},
        {"name": "Tag Survival", "description": "Free tag in Survival", "trait_data": {"tag": "Survival"}, "is_selectable": False},
        {"name": "Improved Sensors", "description": "You have 360° vision and improved sensory systems that can detect smells, chemicals, and radiation, reducing the difficulty of Perception tests that rely on sight and smell by 1.", "trait_data": {}, "is_selectable": False},
        {"name": "Immune to Radiation", "description": "You are immune to radiation.", "trait_data": {}, "is_selectable": False},
        {"name": "Immune to Poison", "description": "You are also immune to poison.", "trait_data": {}, "is_selectable": False},
        {"name": "Robo Body", "description": "You cannot use chems, nor can you benefit from food, drink, or rest.", "trait_data": {}, "is_selectable": False},
        {"name": "Robo Recovery", "description": "You cannot recover from your own injuries or heal health points without receiving repairs.", "trait_data": {}, "is_selectable": False},
        {"name": "Robo Carry", "description": "Your carry weight is 150 lbs., and it cannot be increased by your Strength or perks, but it can be increased by modified armor.", "trait_data": {"carry_weight": 150}, "is_selectable": False},
        {"name": "Hovering", "description": "You move by jet propulsion, hovering above the ground, unaffected by difficult terrain or obstacles.", "trait_data": {}, "is_selectable": False},
        {"name": "Robo Pistol", "description": "You can make ranged attacks using a 10mm auto pistol.", "trait_data": {}, "is_selectable": True},
        {"name": "Robo Saw", "description": "You can cut objects and make melee attacks with a circular saw. The buzz-saw inflicts 3 DC Piercing 1 physical damage", "trait_data": {}, "is_selectable": True},
        {"name": "Robo Flamer", "description": "You can set objects alight, cook food, or make ranged attacks with a short-range flamethrower", "trait_data": {}, "is_selectable": True},
        {"name": "Robo Laser", "description": "You can cut objects or make ranged attacks using a laser", "trait_data": {}, "is_selectable": True},
        {"name": "Robo Pincer", "description": "You can pick up objects with an individual pincer that weighes no more than 40 lbs. and manipulate objects in your environment. You may also make unarmed attacks (2 DC physical damage) with the pincer.", "trait_data": {}, "is_selectable": True},
        {"name": "Super Mutant Ranks", "description": "You may not have more than 4 ranks in any skill.", "trait_data": {"Max Ranks": 4}, "is_selectable": False},
        {"name": "Super Mutant Armor", "description": "You can only wear armor which has been made to fit a super mutant.", "trait_data": {}, "is_selectable": False}
        # {"name": "", "description": "", "trait_data": {}, "is_selectable": False}
    ]

    add_traits(traits)

if __name__ == '__main__':
    try:
        populate_traits()
    except Exception as e:
        logging.error(f"Error populating traits: {e}")
        sys.exit(1)
