from flask import abort, make_response, Response
from ..db import db
from datetime import datetime

def get_models_with_filters(cls, filters=None):
    query = db.select(cls)
    if filters:
        for attribute, value in filters.items():
            if hasattr(cls, attribute):
                query = query.where(getattr(cls, attribute).ilike(f"%{value}%"))

    models = db.session.scalars(query.order_by(cls.id))

    return [model.to_dict() for model in models]


def validate_model(cls, id):
    try:
        int(id)
    except:
        response = {"message": f"{cls.__name__} {id} invalid"}
        abort(make_response(response, 400))

    query = db.select(cls).where(cls.id == id)
    model = db.session.scalar(query)
    if not model:
        response = {"message": f"{cls.__name__} {id} not found"}
        abort(make_response(response, 404))
    
    return model

def validate_log(cls, date_string):
    # try:
    #     datetime.date(date_string)
    # except:
    #     response = {"message": f"{cls.__name__} {date_string} invalid"}
    #     abort(make_response(response, 400))
    # return date_string
    query = db.select(cls).where(cls.timestamp == date_string)
    model = db.session.scalar(query)
    if not model:
        return False
    
    return model

def create_model(cls, model_data):
    try:
        new_model = cls.from_dict(model_data)
    except KeyError:
        response_body = {"details": "Invalid data. Required attrs missing."}
        abort(make_response(response_body, 400))

    db.session.add(new_model)
    db.session.commit()

    return new_model.to_dict(), 201

def delete_model(cls, id):
    model = validate_model(cls, id)

    db.session.delete(model)
    db.session.commit()

    return Response(status=204, mimetype="application/json")

# update model
def update_model(cls, id, request_body, allowed_params):
    model = validate_model(cls, id)

    for param, value in request_body.items():
        if hasattr(cls, param) and param in allowed_params:
            setattr(model, param, value)

    db.session.commit()

    return model.to_dict(), 200