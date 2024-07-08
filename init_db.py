
import os
from database import Base, engine
# Add all models here
from models import Player, Character 

# Ensure instance directory exists
instance_path = 'instance'
if not os.path.exists(instance_path):
    os.makedirs(instance_path)

# Create all tables in the database
Base.metadata.create_all(engine)
print("Database initialized!")