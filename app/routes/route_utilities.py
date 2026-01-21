from flask import abort, make_response
from ..db import db
# utilities to write
# create model

def create_model(cls, model_data):
    try:
        new_model = cls.from_dict(model_data)
    except KeyError:
        response_body = {"details": "Invalid data"}
        abort(make_response(response_body, 400))

    db.session.add(new_model)
    db.session.commit()

    return new_model.to_dict(), 201

# delete model
# update model
# validate model
