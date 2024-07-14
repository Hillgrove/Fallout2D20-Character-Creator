
import os
import sys

# Ensure the 'scripts' directory is added to the system path to find 'app'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, db
from app.models import Origin

# Use the Flask application context
with app.app_context():
    origins = [
        {"name": "Vault Dweller", "description": "A resident of one of the many Vaults created by Vault-Tec to preserve human life in the event of a nuclear apocalypse.", "trait_id": 1},
        {"name": "Wastelander", "description": "A survivor from the harsh, irradiated wasteland. Adapted to scavenging and surviving in the ruins of civilization.", "trait_id": 2},
        {"name": "Brotherhood of Steel", "description": "A member of the Brotherhood of Steel, a group dedicated to preserving pre-war technology and combating the threats of the wasteland.", "trait_id": 3},
        {"name": "Super Mutant", "description": "A human mutated by the Forced Evolutionary Virus (FEV), possessing great strength and resilience but often viewed as a monster by others.", "trait_id": 4},
        {"name": "Raider", "description": "A member of a brutal gang of marauders, living by raiding and pillaging the remains of civilization.", "trait_id": 5},
        {"name": "Ghoul", "description": "A human who has been heavily irradiated but has not died, becoming a ghoul. Ghouls have extended lifespans and some retain their sanity.", "trait_id": 6},
        {"name": "NCR Citizen", "description": "A citizen of the New California Republic, a large faction aiming to restore order and democracy in the post-apocalyptic world.", "trait_id": 7},
        {"name": "Enclave", "description": "A member of the Enclave, the remnants of the pre-war United States government and military, known for their advanced technology and secretive nature.", "trait_id": 8}
    ]

    for origin in origins:
        existing_origin = Origin.query.filter_by(name=origin["name"]).first()
        if not existing_origin:
            new_origin = Origin(name=origin["name"], description=origin["description"], trait_id=origin["trait_id"])
            db.session.add(new_origin)

    db.session.commit()
    print("Origins added to the database.")
