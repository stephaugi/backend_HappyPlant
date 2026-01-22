from app import create_app, db

from app.models.plant import Plant

# REQUIRED_PARAMS = ["name", "desired_moisture_level", "user_id"]
my_app = create_app()
with my_app.app_context():
    plants = [
        Plant(name="Jelly", desired_moisture_level=2, owner_id=2),
        Plant(name="Danger", desired_moisture_level=1, owner_id=1),
    ]
    db.session.add_all(plants)
    db.session.commit()

# from app.models.owner import Owner

# my_app = create_app()
# with my_app.app_context():
#     owners = [
#         Owner(first_name="James", last_name="Bond", email="jamesbond007@gmail.com"),
#         Owner(first_name="Spongebob", last_name="Squarepants", email="wholivesinapineapple@gmail.com")
#     ]
#     db.session.add_all(owners)
#     db.session.commit()
