from flask import Blueprint, request, Response, abort, make_response
from ..db import db
from app.models.plant import Plant
from app.models.water_log import WaterLog
from app.models.moisture_log import MoistureLog
from datetime import timedelta, datetime
import math
from .route_utilities import create_model, validate_model, validate_log, update_model, delete_model, get_models_with_filters

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
    try:
        request_body = request.get_json()
        for request_log in request_body:
            water_plant_dict = {"plant_id": plant_id,
                                "timestamp": request_log["timestamp"]}
            water_log_match = validate_log(WaterLog, request_log["timestamp"])
            if not request_log.get("watered"):

                if water_log_match:
                    delete_model(WaterLog, water_log_match.id)
                    
            elif request_log.get("watered"):
                if not water_log_match:
                    create_model(WaterLog, water_plant_dict)
        water_logs = plant.water_history
        if len(water_logs) > 1:
            # calculate water cycle length
            total_time = 0
            for i in range(1, len(water_logs)):
                total_time += (water_logs[i].timestamp - water_logs[i-1].timestamp).days
            average_water_cycle = total_time / (len(water_logs)-1)

            # set water cycle length
            plant.average_water_cycle = average_water_cycle
            plant.next_water_date = str(water_logs[-1].timestamp + timedelta(days=average_water_cycle))
            db.session.commit()
            # update next moisture check reminder


        return [water_log.to_dict() for water_log in water_logs]
    except Exception as e:
        # required_attrs = ", ".join(["watered", "timestamp", "plant_id"])
        response_body = {"message": f"{e}"}            
        abort(make_response(response_body, 400))

@bp.get("/<plant_id>/water")
def get_water_logs(plant_id):
    plant = validate_model(Plant, plant_id)
    water_logs = plant.water_history

    return [water_log.to_dict() for water_log in water_logs]

@bp.post("/<plant_id>/moisture")
def create_moisture_logs(plant_id):
    plant = validate_model(Plant, plant_id)
    allowed_params = ["plant_id", "timestamp", "moisture_level"]
    # expect to get a list of all moisture logs to create
    # [
    # {
    #     "id": 1,
    #     "moisture_level": 6,
    #     "timestamp": "2026-01-29",
    # },
    # {
    #     "id": 3,
    #     "moisture_level": 6,
    #     "timestamp": "2026-01-28",
    # },
    # ]
    try:
        request_body = request.get_json()
        if not isinstance(request_body, list):
            raise TypeError("Request body must be a list of dictionary objects.")
        for request_log in request_body:
            plant_status_dict = {
                "plant_id": plant_id,
                "timestamp": request_log["timestamp"],
                "moisture_level": request_log.get("moisture_level"),
            }
            moisture_log_match = validate_log(MoistureLog, request_log["timestamp"])
            if not moisture_log_match:
                create_model(MoistureLog, plant_status_dict)
            elif not plant_status_dict.get("moisture_level"):
                delete_model(MoistureLog, moisture_log_match.id)
            else:
                update_model(MoistureLog, moisture_log_match.id, plant_status_dict, allowed_params)
        moisture_logs = plant.moisture_history
        plant.current_moisture_level = moisture_logs[-1].moisture_level
        db.session.commit()
        if plant.current_moisture_level <= plant.desired_moisture_level:
            # create reminder
            return {"message":f"time to remind user. desired moisture: {plant.desired_moisture_level}. current moisture: {plant.current_moisture_level}"}, 200
        return [moisture_log.to_dict() for moisture_log in moisture_logs]
        # log number of times watered.
        # calculate average water time
    except Exception as e:
        required_attrs = ", ".join(["moisture_level", "timestamp", "plant_id"])
        response_body = {"message": f"{e}"}            
        abort(make_response(response_body, 400))

@bp.get("/<plant_id>/moisture")
def get_moisture_logs(plant_id):
    # params = request.args
    plant = validate_model(Plant, plant_id)
    moisture_logs = plant.moisture_history
    # params = {"plant_id": plant_id}

    return [moisture_log.to_dict() for moisture_log in moisture_logs]