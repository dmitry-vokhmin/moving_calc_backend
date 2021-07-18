from .fixtures import *


def test_user_privilege_get(client, token_and_user_privilege):
    token, privilege = token_and_user_privilege
    response = client.get("/user_privilege/", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()[0]["privilege"] == privilege
