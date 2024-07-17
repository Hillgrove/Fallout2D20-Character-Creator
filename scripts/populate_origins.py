import os
import sys
import logging

# Ensure the 'scripts' directory is added to the system path to find 'app'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, db
from app.models import Origin, Trait, OriginTrait

logging.basicConfig(level=logging.INFO)

def add_origin_and_traits(origin_data):
    with app.app_context():
        existing_origin = Origin.query.filter_by(name=origin_data["name"]).first()
        if not existing_origin:
            new_origin = Origin(
                name=origin_data["name"],
                description=origin_data["description"],
                selectable_traits_limit=origin_data.get("selectable_traits_limit", 0)
            )
            db.session.add(new_origin)
            db.session.commit()  # Commit to get the new origin's id

            for trait_name in origin_data["traits"]:
                existing_trait = Trait.query.filter_by(name=trait_name).first()
                if existing_trait:
                    origin_trait = OriginTrait(
                        origin_id=new_origin.id,
                        trait_id=existing_trait.id
                    )
                    db.session.add(origin_trait)
                    logging.info(f"Added trait '{trait_name}' to origin '{new_origin.name}'")
                else:
                    logging.warning(f"Trait '{trait_name}' does not exist and was not added to origin '{new_origin.name}'")
            db.session.commit()
            logging.info(f"Added new origin: {origin_data['name']}")
        else:
            logging.info(f"Origin '{origin_data['name']}' already exists in the database.")

def populate_origins_and_traits():
    origins_with_traits = [
        {
            "name": "Vault Dweller",
            "description": "A resident of one of the many Vaults created by Vault-Tec to preserve human life in the event of a nuclear apocalypse.",
            "selectable_traits_limit": 0,
            "traits": [
                "Example Trait"
            ]
        },
        {
            "name": "Wastelander",
            "description": "A survivor from the harsh, irradiated wasteland. Adapted to scavenging and surviving in the ruins of civilization.",
            "selectable_traits_limit": 0,
            "traits": [
                "Example Trait"
            ]
        },
        {
            "name": "Brotherhood of Steel",
            "description": "A member of the Brotherhood of Steel, a group dedicated to preserving pre-war technology and combating the threats of the wasteland.",
            "selectable_traits_limit": 0,
            "traits": [
                "Example Trait"
            ]
        },
        {
            "name": "Super Mutant",
            "description": "A human mutated by the Forced Evolutionary Virus (FEV), possessing great strength and resilience but often viewed as a monster by others.",
            "selectable_traits_limit": 0,
            "traits": [
                "Strength Max",
                "Endurance Max",
                "Charisma Max",
                "Intelligence Max"
            ]
        },
        {
            "name": "Raider",
            "description": "A member of a brutal gang of marauders, living by raiding and pillaging the remains of civilization.",
            "selectable_traits_limit": 0,
            "traits": [
                "Example Trait"
            ]
        },
        {
            "name": "Ghoul",
            "description": "A human who has been heavily irradiated but has not died, becoming a ghoul. Ghouls have extended lifespans and some retain their sanity.",
            "traits": [
                "Example Trait"
            ]
        },
        {
            "name": "NCR Citizen",
            "description": "A citizen of the New California Republic, a large faction aiming to restore order and democracy in the post-apocalyptic world.",
            "selectable_traits_limit": 0,
            "traits": [
                "Example Trait"
            ]
        },
        {
            "name": "Enclave",
            "description": "A member of the Enclave, the remnants of the pre-war United States government and military, known for their advanced technology and secretive nature.",
            "selectable_traits_limit": 0,
            "traits": [
                "Example Trait"
            ]
        },
        {
            "name": "Survivor",
            "description": "A hardy individual who has learned to thrive in the harsh post-apocalyptic world.",
            "selectable_traits_limit": 2,
            "traits": [
                "Educated",
                "Gifted",
                "Small Frame",
                "Fast Shot",
                "Heavy Handed",
                "Extra Perk"
            ]
        }
    ]

    for origin_data in origins_with_traits:
        add_origin_and_traits(origin_data)

if __name__ == '__main__':
    try:
        populate_origins_and_traits()
    except Exception as e:
        logging.error(f"Error populating origins and traits: {e}")
        sys.exit(1)
