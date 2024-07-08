
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import Config

# Setup the data engine
engine = create_engine(Config.SQLALCHEMY_DATABASE_URI, echo=True)

# Create a configured Session class
Session = sessionmaker(bind=engine)

# Create a session
session = Session()

# Base class for classes definition
Base = declarative_base()