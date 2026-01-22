from flask import Flask
from .db import db, migrate
from .models import owner, plant, water_log, moisture_log, plant_status
from .routes.plant_routes import bp as plants_bp
from .routes.owner_routes import bp as owners_bp
import os

def create_app(config=None):
    app = Flask(__name__)

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')


    if config:
        # Merge `config` into the app's configuration
        # to override the app's default settings for testing
        app.config.update(config)

    db.init_app(app)
    migrate.init_app(app, db)

    # Register Blueprints here
    app.register_blueprint(plants_bp)
    app.register_blueprint(owners_bp)


    return app
