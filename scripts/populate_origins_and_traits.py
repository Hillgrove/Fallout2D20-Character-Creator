import os
import sys

# Ensure the 'scripts' directory is added to the system path to find 'app'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, db
from app.models import Origin, Trait

def add_origin_and_traits(origin_data):
    existing_origin = Origin.query.filter_by(name=origin_data["name"]).first()
    if not existing_origin:
        new_origin = Origin(
            name=origin_data["name"],
            description=origin_data["description"],
            selectable_traits_limit=origin_data.get("selectable_traits_limit", 0)  # Set the limit here
        )
        db.session.add(new_origin)
        db.session.commit()  # Commit to get the new origin's id

        # Add traits for the new origin
        for trait_data in origin_data["traits"]:
            # Ensure trait name is unique by appending the origin name
            unique_trait_name = f"{trait_data['name']} ({new_origin.name})"
            existing_trait = Trait.query.filter_by(name=unique_trait_name, origin_id=new_origin.id).first()
            if not existing_trait:
                new_trait = Trait(
                    name=unique_trait_name,
                    description=trait_data["description"],
                    trait_data=trait_data["trait_data"],
                    origin_id=new_origin.id,
                    is_selectable=trait_data.get("is_selectable", False)  # Set is_selectable here
                )
                db.session.add(new_trait)
    else:
        print(f"Origin '{origin_data['name']}' already exists in the database.")


def populate_origins_and_traits():
    origins_with_traits = [
        {
            "name": "Vault Dweller",
            "description": "A resident of one of the many Vaults created by Vault-Tec to preserve human life in the event of a nuclear apocalypse.",
            "traits": [
                {"name": "Example Trait", "description": "This is an example trait for Vault Dwellers.", "trait_data": {"example_key": "example_value"}}
            ]
        },
        {
            "name": "Wastelander",
            "description": "A survivor from the harsh, irradiated wasteland. Adapted to scavenging and surviving in the ruins of civilization.",
            "selectable_traits_limit": 0,
            "traits": [
                {"name": "Example Trait", "description": "This is an example trait for Wastelanders.", "trait_data": {"example_key": "example_value"}}
            ]
        },
        {
            "name": "Brotherhood of Steel",
            "description": "A member of the Brotherhood of Steel, a group dedicated to preserving pre-war technology and combating the threats of the wasteland.",
            "selectable_traits_limit": 0,
            "traits": [
                {"name": "Example Trait", "description": "This is an example trait for Brotherhood of Steel.", "trait_data": {"example_key": "example_value"}}
            ]
        },
        {
            "name": "Super Mutant",
            "description": "A human mutated by the Forced Evolutionary Virus (FEV), possessing great strength and resilience but often viewed as a monster by others.",
            "selectable_traits_limit": 0,
            "traits": [
                {"name": "Strength Max", "description": "Strength can be raised to a max of 12.", "trait_data": {"stat": "Strength", "max": 12}},
                {"name": "Endurance Max", "description": "Endurance can be raised to a max of 12.", "trait_data": {"stat": "Endurance", "max": 12}},
                {"name": "Charisma Max", "description": "Charisma can be raised to a max of 6.", "trait_data": {"stat": "Charisma", "max": 6}},
                {"name": "Intelligence Max", "description": "Intelligence can be raised to a max of 6.", "trait_data": {"stat": "Intelligence", "max": 6}}
            ]
        },
        {
            "name": "Raider",
            "description": "A member of a brutal gang of marauders, living by raiding and pillaging the remains of civilization.",
            "selectable_traits_limit": 0,
            "traits": [
                {"name": "Example Trait", "description": "This is an example trait for Raiders.", "trait_data": {"example_key": "example_value"}}
            ]
        },
        {
            "name": "Ghoul",
            "description": "A human who has been heavily irradiated but has not died, becoming a ghoul. Ghouls have extended lifespans and some retain their sanity.",
            "traits": [
                {"name": "Example Trait", "description": "This is an example trait for Ghouls.", "trait_data": {"example_key": "example_value"}}
            ]
        },
        {
            "name": "NCR Citizen",
            "description": "A citizen of the New California Republic, a large faction aiming to restore order and democracy in the post-apocalyptic world.",
            "selectable_traits_limit": 0,
            "traits": [
                {"name": "Example Trait", "description": "This is an example trait for NCR Citizens.", "trait_data": {"example_key": "example_value"}}
            ]
        },
        {
            "name": "Enclave",
            "description": "A member of the Enclave, the remnants of the pre-war United States government and military, known for their advanced technology and secretive nature.",
            "selectable_traits_limit": 0,
            "traits": [
                {"name": "Example Trait", "description": "This is an example trait for Enclave members.", "trait_data": {"example_key": "example_value"}}
            ]
        },
        {
            "name": "Survivor",
            "description": "A hardy individual who has learned to thrive in the harsh post-apocalyptic world.",
            "selectable_traits_limit": 2,
            "traits": [
                {"name": "Educated", "description": "+1 tag skill", "trait_data": {"bonus": "extra_tag_skill"}, "is_selectable": True},
                {"name": "Gifted", "description": "2 more SPECIAL (stat points)", "trait_data": {"bonus": "extra_special_points", "amount": 2}, "is_selectable": True},
                {"name": "Small Frame", "description": "just a description", "trait_data": {}, "is_selectable": True},
                {"name": "Fast Shot", "description": "just a description", "trait_data": {}, "is_selectable": True},
                {"name": "Heavy Handed", "description": "+1 CD to melee and unarmed damage", "trait_data": {"bonus": "melee_damage", "amount": 1}, "is_selectable": True},
                {"name": "Extra Perk", "description": "1 more perk", "trait_data": {"bonus": "extra_perk"}, "is_selectable": True}
            ]
        }
    ]

    for origin_data in origins_with_traits:
        add_origin_and_traits(origin_data)

    db.session.commit()
    print("Origins and traits added to the database.")

if __name__ == '__main__':
    with app.app_context():
        populate_origins_and_traits()
