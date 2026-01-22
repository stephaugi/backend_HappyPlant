from app.db import db
import pytest

# test plant gets created correctly
# test plant that doesn't exist raises error


# test plant gets deleted
def test_delete_plant(client, one_owner, one_plant):
    # Act
    response = client.delete("/plants/1")
    response_body = client.get("owners/1/plants").get_json()

    # Assert
    assert response.status_code == 204
    assert response_body == []

# test plant gets updated with description
def test_update_plant(client, one_owner, one_plant):
    request_body = {"description": "My sweetest baby that likes to live life on the edge. Very dry."}
    # Act
    response = client.patch("/plants/1", json=request_body)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == {"id": 1,
                            "name": "Danger",
                            "description": "My sweetest baby that likes to live life on the edge. Very dry.",
                            "current_moisture_level": None,
                            "desired_moisture_level": 1,
                            "next_water_date": None,
                            "photo": None}