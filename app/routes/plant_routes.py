from flask import Blueprint, request, Response
from ..db import db
from app.models.plant import Plant
from app.models.water_log import WaterLog
from app.models.moisture_log import MoistureLog
from .route_utilities import create_model, validate_model, update_model, delete_model

bp = Blueprint("plants_bp", __name__, url_prefix="/plants")

@bp.put("/<plant_id>")
def edit_plant(plant_id):
    request_body = request.get_json()
    allowed_params = ["name",
                    "desired_moisture_level",
                    "description",
                    "photo",
                    "current_moisture_level"
    ]
    plant = validate_model(plant_id)
    update_model(Plant, plant_id, request_body, allowed_params)

    return plant.to_dict()

@bp.post("/<plant_id>/moisture_log")
def add_moisture_log(plant_id):
    request_body = request.get_json()
    plant = validate_model(Plant, plant_id)

    request_body["plant_id"] = plant.id

    create_model(MoistureLog, request_body)

@bp.delete("/<plant_id>")
def delete_plant(plant_id):
    return delete_model(Plant, plant_id)