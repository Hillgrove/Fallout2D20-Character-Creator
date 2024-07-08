
from flask import Flask, render_template, redirect, url_for, request, session
from config import Config
from database import Base, engine
from models import Player

app = Flask(__name__)
app.config.from_object(Config)

# Import models and routes here


Base.metadata.create_all(engine)

if __name__ == "__main__":
    app.run(debug=True)