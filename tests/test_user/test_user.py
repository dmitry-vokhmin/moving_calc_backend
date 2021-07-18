from tests.test_user.fixtures import *
from tests.factory_mockup import session


def test_user_reg_and_auth(user_data, client):
    registration = client.post("/registration/", json=user_data)
    authorization = client.post("/authorization/", json=user_data)
    assert registration.status_code == 201
    assert authorization.status_code == 200