
import os
import sys

# Ensure the 'scripts' directory is added to the system path to find 'app'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, db
from app.models import Origin

# Use the Flask application context
with app.app_context():
    # List of origins to add to the database
    origins = [
        {"name": "Vault Dweller", "description": "A resident of one of the many Vaults created by Vault-Tec to preserve human life in the event of a nuclear apocalypse.", "rule_id": 1},
        {"name": "Wastelander", "description": "A survivor from the harsh, irradiated wasteland. Adapted to scavenging and surviving in the ruins of civilization.", "rule_id": 2},
        {"name": "Brotherhood of Steel", "description": "A member of the Brotherhood of Steel, a group dedicated to preserving pre-war technology and combating the threats of the wasteland.", "rule_id": 3},
        {"name": "Super Mutant", "description": "A human mutated by the Forced Evolutionary Virus (FEV), possessing great strength and resilience but often viewed as a monster by others.", "rule_id": 4},
        {"name": "Raider", "description": "A member of a brutal gang of marauders, living by raiding and pillaging the remains of civilization.", "rule_id": 5},
        {"name": "Ghoul", "description": "A human who has been heavily irradiated but has not died, becoming a ghoul. Ghouls have extended lifespans and some retain their sanity.", "rule_id": 6},
        {"name": "NCR Citizen", "description": "A citizen of the New California Republic, a large faction aiming to restore order and democracy in the post-apocalyptic world.", "rule_id": 7},
        {"name": "Enclave", "description": "A member of the Enclave, the remnants of the pre-war United States government and military, known for their advanced technology and secretive nature.", "rule_id": 8}
    ]

    # Add each origin to the database
    for origin in origins:
        new_origin = Origin(name=origin["name"], description=origin["description"], rule_id=origin["rule_id"])
        db.session.add(new_origin)

    # Commit the changes
    db.session.commit()

    print("Origins added to the database.")
