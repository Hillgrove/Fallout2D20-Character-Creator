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
            "name": "Ghoul",
            "description": ("""<p>You age at a much-decreased rate, and you’re probably
                            older than your unmutated companions—you may even have
                            survived the Great War of 2077—but you’re sterile: “the first
                            generation of ghouls is the last” as the saying goes. You may
                            face discrimination from “smoothskins” (humans who aren’t
                            ghouls), increasing the difficulty or complication range of
                            Charisma tests depending on your opponent’s beliefs.</p>
                            
                            <p>You are immune to radiation damage. In fact, you’re healed
                            by it—you regain 1 HP for every 3 points of radiation
                            damage inflicted upon you, and if you rest in an irradiated
                            location, you may re-roll your dice pool when checking if
                            your injuries heal. In addition, Survival becomes a Tag skill,
                            increasing it by 2 ranks.</p>"""),
            "selectable_traits_limit": 0,
            "traits": [
                "Rad Healing",
                "Rad Resting",
                "Tag Survival"
            ]
        },
        {
            "name": "Mister Handy",
            "description": ("""<p>The General Atomics International robot “Mister
                            Handy” exploded onto the robotic market as a
                            reliable construction robot, known for its durability
                            and ease of maintenance, but its real breakthrough
                            came in a collaboration with RobCo to produce a
                            domestic model.</p>

                            <p>You are one of these domestic automatons, produced
                            some time between 2037 and 2077, seeking to provide
                            every household in America with butler-like servitude.
                            Equipped with state-of-the-art programming, you have
                            initiative and can adapt your own coding to learn more
                            from your environment. This capacity for self-determination
                            is what has enabled your survival beyond the
                            Great War; where other robots may have broken down,
                            you have managed to shake loose from the shackles of
                            your programming and find a life for yourself.</p>

                            <p>Many models exist, and you could come from any
                            of the Mister Handy, Mister Gutsy, Miss Nanny, or
                            Mister Orderly series. You are powered by a nuclear
                            core, can replace your own fuel, and repair yourself
                            or other Mister Handy units. Your model has three
                            mechanical arms and three mechanical eyes on stalks,
                            and your jet propulsion keeps you hovering above the
                            ground, providing you have all the fuel you need. With
                            this rugged design, you have survived so far.</p>
                            
                            <p>You have 360° vision and improved sensory systems that
                            can detect smells, chemicals, and radiation, reducing the
                            difficulty of Perception tests that rely on sight and smell by
                            1. You are also immune to radiation and poison damage,
                            but you cannot use chems, nor can you benefit from food,
                            drink, or rest. You move by jet propulsion, hovering above
                            the ground, unaffected by difficult terrain or obstacles. Your
                            carry weight is 150 lbs., and it cannot be increased by
                            your Strength or perks, but it can be increased by modified
                            armor. You cannot recover from your own injuries or
                            heal health points without receiving repairs.</p>

                            <p>You cannot manipulate the physical
                            world like humans do, instead you have
                            three of the arm attachments in the Arm
                            Attachments table, determined by your
                            choice of equipment pack. If you select an arm
                            that features a weapon, you also gain 20 shots of
                            ammo for that weapon.</p>"""),
            "selectable_traits_limit": 3,
            "traits": [
                "Improved Sensors",
                "Immune to Radiation",
                "Immune to Poison",
                "Robo Body",
                "Hovering",
                "Robo Carry",
                "Robo Recovery",
                "Robo Pistol",
                "Robo Saw",
                "Robo Flamer",
                "Robo Laser",
                "Robo Pincer"
            ]
        },
        {
            "name": "Super Mutant",
            "description": ("""<p>You are a brutal, mutated human, forced to evolve
                            from thoughtless experiments by the twisted science
                            of the pre- and post-war world. Infected with
                            the Forced Evolutionary Virus (F.E.V.), your body has
                            mutated into a tall, muscular killing machine, filled
                            with a rage.</p>

                            <p>You could have originated from the Master’s army
                            at the Mariposa military base, California, created
                            as he experimented on unwilling human victims,
                            splitting into one of the factions upon his death to
                            attack or rebuild the wasteland with its survivors.
                            Your origins could be rooted in the Evolutionary
                            Experimentation Program of Vault 87, whose super
                            mutant groups terrorize the Capital Wasteland. You
                            could have been abducted from the Commonwealth
                            and exposed to the F.E.V. by the Institute and disposed
                            of back into the wasteland to fend for yourself
                            in small bands of raiders. Or finally, you could have
                            been a resident of Huntersville, Appalachia, whose
                            water supply was contaminated with the virus and
                            the mutations went unchecked.</p>
                            
                            <p>Your initial Strength and Endurance attributes are increased
                            by +2 each, and your maximum Strength and Endurance
                            are increased to 12, but your maximum Intelligence and
                            Charisma are both reduced to 6. You may not have more
                            than 4 ranks in any skill. You are completely immune to
                            radiation and poison damage.
                            You stand over seven feet tall, and your body is bulky and
                            muscular. Your skin is green, yellow, or grey, regardless of
                            what color it was when you were human. You do not seem to
                            age, but you are sterile.
                            You can only wear armor
                            which has been made to
                            fit a super mutant.</p>"""),
            "selectable_traits_limit": 0,
            "traits": [               
                "Immune to Radiation",
                "Immune to Poison",
                "Super Mutant Ranks",
                "Super Mutant Armor",
                "Strength Max",
                "Endurance Max",
                "Charisma Max",
                "Intelligence Max"
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