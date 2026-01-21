from flask import Blueprint, request, Response
from ..db import db
from app.models.plant import Plant
from app.models.waterlog import WaterLog
# from .route_utilities import create_model

bp = Blueprint("plants_bp", __name__, url_prefix="/plants")
REQUIRED_PARAMS = ["name", "desired_moisture_level", "user_id"]
OPTIONAL_PARAMS = ["description", "photo", "current_moisture_level", "next_water_date"]

@bp.post("")
def create_plant():
    request_body = request.get_json()
    pass
    # return create_model(Plant, request_body, class_params=[REQUIRED_PARAMS, OPTIONAL_PARAMS])