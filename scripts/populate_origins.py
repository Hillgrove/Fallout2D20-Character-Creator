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
            "description": ("""<p>Your healthier start to life at the hands of trained doctors and sophisticated auto-docs
                            means you reduce the difficulty of all END tests to resist the effects of disease. In addition, 
                            your carefully-planned upbringing means you have one additional tag skill of your choice.</p>
                            
                            <p>You may also work with the Gamemaster to determine what sort of experiment took place within your Vault. 
                            Once per quest, the GM may introduce a complication which reflects the nature of the experiment you 
                            unwittingly took part in, or introduce a complication related to your early life of isolation and 
                            confinement within the Vault. If the GM does this, you immediately regain one Luck Point.</p>"""),
            "selectable_traits_limit": 0,
            "traits": [
                "Reduced END Test Difficulty",
                "Luck Point Recovery",
                "Additional Tag Skill"
            ]
        },
        {
            "name": "Survivor",
            "description": ("""<p>You are the living legacy of the people who prepared
                            for Armageddon on their own. You are only alive in
                            the post-nuclear apocalyptic landscape because your
                            forebears dug in, survived, and found community
                            enough to continue humanity’s existence.</p>

                            <p>You could be from any number of settlements, isolated
                            shelters, or traveling groups that sparsely populate the
                            wasteland from West Coast to East Coast. You could
                            be from the New California Republic, carrying on the
                            legacy of Vault 15 and Shady Sands. You could fight
                            to protect others, calling a group of survivors like the
                            Minutemen or the Regulators your home. You could
                            also be a merciless raider or be born into one of these
                            groups but escaped in order to rehabilitate and reform.</p>

                            <p>Wherever you are from, or wherever you travel, making
                            connections and laying down roots can be hard.
                            Survivors are naturally wary of others, and are always
                            on the lookout for the next conman, raiding party,
                            or thief that will take their hard-earned resources.
                            Travelling vast distances is difficult too, and many travelling
                            survivors—particularly trading caravans—move
                            between large settlements within their area of the
                            wasteland, rather than travelling from coast to coast.</p>"""),
            "selectable_traits_limit": 2,
            "traits": [
                "Educated",
                "Fast Shot",
                "Gifted",
                "Heavy Handed",
                "Small Frame",
                "Extra Perk"
            ]
        },
        {
            "name": "Brotherhood of Steel",
            "description": ("""<p>As a member of the Brotherhood of Steel, you are bound by
                            the chain of command: The Chain that Binds. You must carry
                            out the orders of your immediate superiors, and you are
                            responsible for your subordinate siblings. If you do not carry
                            out your duty, you are expelled from the Brotherhood and
                            your technology will be reclaimed—by any means necessary</p>
                            
                            <p>You gain one additional Tag skill, which must be one of
                            Energy Weapons, Science, or Repair.</p>"""),
            "selectable_traits_limit": 1,
            "traits": [
                "Tag Energy Weapons",
                "Tag Science", 
                "Tag Repair"
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
