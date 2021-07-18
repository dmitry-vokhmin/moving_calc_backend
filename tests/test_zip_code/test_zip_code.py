from tests.test_zip_code.fixtures import *


def test_zip_post(zip_code_data, client, token):
    response_token = client.post("/zip_code/",
                                 json=zip_code_data,
                                 headers={"Authorization": f"Bearer {token}"})
    response_no_token = client.post("/zip_code/", json=zip_code_data)
    assert response_token.status_code == 201
    assert response_no_token.status_code == 401


def test_zip_get_exact(zip_code_data_from_db, client):
    response = client.get(f"/zip_code/", params=zip_code_data_from_db)
    assert response.status_code == 200
    assert response.json()["zip_code"] == zip_code_data_from_db["zip_code"]
