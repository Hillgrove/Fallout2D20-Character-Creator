
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

# Create a Flask instance
app = Flask(__name__)

# Apply configuration settings from Config class
app.config.from_object(Config)

# Initialize extentions
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"  # Route name for the login view
login_manager.login_message_category = "info"  # Bootstrap class for flash messages

# Import routes to register them with the app
from app import routes