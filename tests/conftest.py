# add 3 users
# add 1 user
# no user
# 1 plant
# 3 plants
# 1 user with 3 plants and 5 moisture logs on one, 

import pytest
from app import create_app
from app.db import db
from flask.signals import request_finished
from dotenv import load_dotenv
import os
from app.models.owner import Owner
from app.models.plant import Plant
from app.models.moisture_log import MoistureLog
from app.models.water_log import WaterLog
from datetime import datetime

load_dotenv()

@pytest.fixture
def app():
    # create the app with a test configuration
    test_config = {
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": os.environ.get('SQLALCHEMY_TEST_DATABASE_URI')
    }
    app = create_app(test_config)

    @request_finished.connect_via(app)
    def expire_session(sender, response, **extra):
        db.session.remove()

    with app.app_context():
        db.create_all()
        yield app

    # close and remove the temporary database
    with app.app_context():
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()

# This fixture gets called in every test that
# references "one_owner"
# This fixture creates an owner and saves it in the database
@pytest.fixture
def one_owner(app):
    new_owner = Owner(first_name="James",
                    last_name="Bond",
                    email="jamesbond007@gmail.com")
    
    db.session.add(new_owner)
    db.session.commit()

# This fixture gets called in every test that
# references "one_plant"
# This fixture creates a plant and saves it in the database
@pytest.fixture
def one_plant(app):
    new_plants = Plant(name="Danger",
                    desired_moisture_level=1,
                    owner_id=1)
    db.session.add(new_plants)
    db.session.commit()

@pytest.fixture
def two_plants(app):
    new_plants = [Plant(name="Danger",
                    desired_moisture_level=1,
                    owner_id=1),
                Plant(name="Jelly",
                    desired_moisture_level=2,
                    owner_id=1)
    ]
    db.session.add_all(new_plants)
    db.session.commit()
