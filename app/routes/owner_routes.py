from flask import Blueprint, request, Response, abort, make_response
from ..db import db
from app.models.owner import Owner
from app.models.plant import Plant
from .route_utilities import get_models_with_filters, create_model, validate_model, delete_model, update_model

bp = Blueprint("owners_bp", __name__, url_prefix="/owners")

@bp.post("")
def create_owner():
    request_body = request.get_json()
    
    return create_model(Owner, request_body)

@bp.get("")
def get_all_owners():
    params = request.args

    return get_models_with_filters(Owner, params)

@bp.get("<owner_id>")
def get_one_owner(owner_id):
    owner = validate_model(Owner, owner_id)
    
    return owner.to_dict()

@bp.delete("/<owner_id>")
def delete_owner(owner_id):
    # delete owner model
    return delete_model(Owner, owner_id)

@bp.patch("/<owner_id>")
def update_owner(owner_id):
    allowed_params = ["first_name", "last_name", "email"]
    try:
        request_body = request.get_json()
        return update_model(Owner, owner_id, request_body, allowed_params)
    except:
        valid_attrs = ", ".join(allowed_params)
        response_body = {"message":
            f"Valid request body must be included. Valid attrs: {valid_attrs}."}
        abort(make_response(response_body, 400))

@bp.post("/<owner_id>/plants")
def create_plant(owner_id):
    request_body = request.get_json()
    request_body["owner_id"] = owner_id
    # return request_body
    return create_model(Plant, request_body)

@bp.get("/<owner_id>/plants")
def get_plants(owner_id):
    owner = validate_model(Owner, owner_id)
    
    return [plant.to_dict() for plant in owner.plants]

