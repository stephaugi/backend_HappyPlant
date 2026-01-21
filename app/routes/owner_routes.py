from flask import Blueprint, request, Response
from ..db import db
from app.models.owner import Owner
from .route_utilities import create_model

bp = Blueprint("owners_bp", __name__, url_prefix="/owners")
# REQUIRED_PARAMS = ["name", "desired_moisture_level", "user_id"]
# OPTIONAL_PARAMS = ["description", "photo", "current_moisture_level", "next_water_date"]

@bp.post("")
def create_owner():
    request_body = request.get_json()
    
    return create_model(Owner, request_body)

@bp.get("")
def get_all_owners():
    query = db.select(Owner)

    owners = db.session.scalars(query)
    return [owner.to_dict() for owner in owners]