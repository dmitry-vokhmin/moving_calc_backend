from .fixtures import *


def test_company_post(client, company_data):
    response = client.post("/company/", json=company_data)
    response_data = response.json()
    assert response.status_code == 201
    assert response_data["name"] == company_data["name"]
    assert response_data["address"]["street"] == company_data["street"] and \
           response_data["address"]["apartment"] == company_data["apartment"]
    assert response_data["address"]["zip_code"]["zip_code"] == company_data["zip_code"]


def test_company_update(client, token, company_data, session_and_models):
    session, models = session_and_models
    response = client.put("/company/", json=company_data, headers={"Authorization": f"Bearer {token}"})
    response_user = client.get("/user/", headers={"Authorization": f"Bearer {token}"})
    user_company = session.query(models.Company).filter_by(id=(session.query(models.User.company_id).filter_by(id=response_user.json()["id"]))).first()
    assert response.status_code == 200
    assert user_company.name == company_data["name"]
