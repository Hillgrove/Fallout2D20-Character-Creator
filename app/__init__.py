
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from config import Config

# Create a Flask instance
app = Flask(__name__)

# Initialize CSRF protection and apply it to the Flask app
csrf = CSRFProtect(app)

# Apply configuration settings from Config class
app.config.from_object(Config)


# Initialize extentions
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"  # Route name for the login view
login_manager.login_message_category = "info"  # Bootstrap class for flash messages

# Import routes to register them with the app
from app import routes