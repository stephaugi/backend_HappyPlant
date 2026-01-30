from flask import Blueprint, request, Response, abort, make_response
from ..db import db
from app.models.plant import Plant
from app.models.water_log import WaterLog
from app.models.moisture_log import MoistureLog
import datetime
from .route_utilities import create_model, validate_model, update_model, delete_model, get_models_with_filters

bp = Blueprint("plants_bp", __name__, url_prefix="/plants")

@bp.get("")
def get_all_plants():
    params = request.args

    return get_models_with_filters(Plant, params)

@bp.get("/<plant_id>")
def get_one_plant(plant_id):
    plant = validate_model(Plant, plant_id)
    
    return plant.to_dict()

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

@bp.patch("/<plant_id>")
def update_plant(plant_id):
    allowed_params = ["name", "description", "photo", "desired_moisture_level"]
    try:
        request_body = request.get_json()
        return update_model(Plant, plant_id, request_body, allowed_params)
    except:
        valid_attrs = ", ".join(allowed_params)
        response_body = {"message":
            f"Valid request body must be included. Valid attrs: {valid_attrs}."}
        abort(make_response(response_body, 400))

@bp.post("/<plant_id>/water")
def water_plant(plant_id):
    plant = validate_model(Plant, plant_id)
    curr_date = datetime.date.today()
    water_plant_dict = {"plant_id": plant_id,
                        "timestamp": curr_date}
    # log number of times watered.
    # calculate average water time
    return create_model(WaterLog, water_plant_dict)
    # if len(plant.water_history) > 1:
    #     average_water_time = (len(plant.water_history)-1)

@bp.post("/<plant_id>/moisture")
def track_moisture(plant_id):
    plant = validate_model(Plant, plant_id)

    try:
        request_body = request.get_json()
        plant_status_dict = {"plant_id": plant_id,
                            "timestamp": request_body["timestamp"],
                            "moisture_level": request_body["moisture_level"],
                            }
        # log number of times watered.
        # calculate average water time
        return create_model(MoistureLog, plant_status_dict)
    except:
        required_attrs = ", ".join(["moisture_level", "timestamp", "plant_id"])
        response_body = {"message":
            f"Valid request body must be included. Required attrs: {required_attrs}."}
        abort(make_response(response_body, 400))

@bp.get("/<plant_id>/moisture")
def get_one_plant_moisture_logs(plant_id):
    # params = request.args
    plant = validate_model(Plant, plant_id)
    moisture_logs = plant.moisture_history
    # params = {"plant_id": plant_id}

    return [moisture_log.to_dict() for moisture_log in moisture_logs]