from tests.test_address.fixtures import *


def test_address_post(client, address_data):
    response = client.post("/address/", json=address_data)
    response_second = client.post("/address/", json=address_data)
    assert response.status_code == 201 and response_second.status_code == 201
    assert response.json()["id"] == response_second.json()["id"]


def test_address_get(client, address_from_db):
    response = client.get("/address/", params=address_from_db)
    assert response.status_code == 200
    assert response.json()["id"] == address_from_db["address_id"]
