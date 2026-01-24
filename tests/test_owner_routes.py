from app.models.owner import Owner
from app.db import db
import pytest


# test Owner.to_dict() returns correct dict
def test_owner_to_dict_no_plants():
    # Arrange
    new_owner = Owner(
        id=1, first_name="James", last_name="Bond", email="jamesbond007@gmail.com"
    )

    # Act
    owner_dict = new_owner.to_dict()

    # Assert
    assert len(owner_dict) == 5
    assert owner_dict["id"] == 1
    assert owner_dict["first_name"] == "James"
    assert owner_dict["last_name"] == "Bond"
    assert owner_dict["email"] == "jamesbond007@gmail.com"
    assert owner_dict["plants"] == []


def test_owner_to_dict_no_id():
    # Arrange
    new_owner = Owner(
        first_name="James", last_name="Bond", email="jamesbond007@gmail.com"
    )

    # Act
    owner_dict = new_owner.to_dict()

    # Assert
    assert len(owner_dict) == 5
    assert owner_dict["id"] is None
    assert owner_dict["first_name"] == "James"
    assert owner_dict["last_name"] == "Bond"
    assert owner_dict["email"] == "jamesbond007@gmail.com"
    assert owner_dict["plants"] == []


def test_task_from_dict():
    # Arrange
    owner_dict = dict(
        first_name="James",
        last_name="Bond",
        email="jamesbond007@gmail.com",
    )

    # Act
    owner_obj = Owner.from_dict(owner_dict)

    # Assert
    assert owner_obj.id == None
    assert owner_obj.first_name == "James"
    assert owner_obj.last_name == "Bond"
    assert owner_obj.email == "jamesbond007@gmail.com"
    assert owner_obj.plants == []

def test_create_owner(client, one_owner, one_plant):

    # Act
    # response = client.get("/owners")

    request_body = {
            "first_name": "Spongebob",
            "last_name": "Squarepants",
            "email": "wholivesinapineapple@gmail.com",
            "plants": [],
        }
    post_response_body = client.post("/owners", json=request_body)
    response = client.get("/owners")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200

    assert response_body == [{
        "id": 1,
        "first_name": "James",
        "last_name": "Bond",
        "email": "jamesbond007@gmail.com",
        "plants": [
            {
                "id": 1,
                "name": "Danger",
                "description": None,
                "photo": None,
                "current_moisture_level": None,
                "desired_moisture_level": 1,
                "next_water_date": None,
            }
        ],
    },
    {
        "id": 2,
        "first_name": "Spongebob",
        "last_name": "Squarepants",
        "email": "wholivesinapineapple@gmail.com",
        "plants": []
    }
    ]

def test_get_owners_one_owner(client, one_owner):

    # Act
    # response = client.get("/owners")
    response = client.get("/owners")
    response_body = response.get_json()

    print(response_body)
    # Assert
    assert response.status_code == 200

    assert response_body == [
        {
            "id": 1,
            "first_name": "James",
            "last_name": "Bond",
            "email": "jamesbond007@gmail.com",
            "plants": [],
        }
    ]


def test_get_owner_no_plant(client, one_owner):
    # Act
    response = client.get("/owners/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200

    assert response_body == {
        "id": 1,
        "first_name": "James",
        "last_name": "Bond",
        "email": "jamesbond007@gmail.com",
        "plants": [],
    }


def test_get_owner_one_plant(client, one_owner, one_plant):
    # Act
    response = client.get("/owners/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200

    assert response_body == {
        "id": 1,
        "first_name": "James",
        "last_name": "Bond",
        "email": "jamesbond007@gmail.com",
        "plants": [
            {
                "id": 1,
                "name": "Danger",
                "description": None,
                "photo": None,
                "current_moisture_level": None,
                "desired_moisture_level": 1,
                "next_water_date": None,
            }
        ],
    }


def test_get_plants(client, one_owner, two_plants):
    # Act
    response = client.get("/owners/1/plants")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 2
    assert response_body == [
        {
            "id": 1,
            "name": "Danger",
            "description": None,
            "photo": None,
            "current_moisture_level": None,
            "desired_moisture_level": 1,
            "next_water_date": None,
        },
        {
            "id": 2,
            "name": "Jelly",
            "description": None,
            "photo": None,
            "current_moisture_level": None,
            "desired_moisture_level": 2,
            "next_water_date": None,
        },
    ]


# @pytest.mark.skip
# test owner gets deleted
def test_delete_owner(client, one_owner, one_plant):
    # Act
    response = client.delete("/owners/1")
    response2 = client.get("/plants/1").get_json()
    response_body = client.get("/owners").get_json()

    # Assert
    assert response.status_code == 204
    assert response_body == []
    assert response2 == {
            "id": 1,
            "name": "Danger",
            "description": None,
            "photo": None,
            "current_moisture_level": None,
            "desired_moisture_level": 1,
            "next_water_date": None,
        }

# test owner gets updated
def test_update_owner(client, one_owner):
    request_body = {
        "last_name": "Li",
        "email": "jamieli@gmail.com"
    }
    # Act
    response = client.patch("/owners/1", json=request_body)
    response_body = response.get_json()
    response2 = client.get("/owners/1").get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == {
        "id": 1,
        "first_name": "James",
        "last_name": "Li",
        "email": "jamieli@gmail.com",
        "plants": [],
    }
    assert response2 == {
        "id": 1,
        "first_name": "James",
        "last_name": "Li",
        "email": "jamieli@gmail.com",
        "plants": [],
    }
    
# test post request plant
def test_create_plant(client, one_owner):
    request_body = {
                    "name": "Butterfly",
                    "desired_moisture_level": 3,
                    }
    # Act
    response = client.post("/owners/1/plants", json=request_body)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 201
    assert response_body == {
    "current_moisture_level": None,
    "description": None,
    "desired_moisture_level": 3,
    "id": 1,
    "name": "Butterfly",
    "next_water_date": None,
    "photo": None
}