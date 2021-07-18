import pytest
from main import app
from data_base.database import get_db, engine
from data_base import models
from .factory_mockup import get_test_db, UserFactory, session
from fastapi.testclient import TestClient


@pytest.fixture
def client():
    app.dependency_overrides[get_db] = get_test_db
    return TestClient(app)


@pytest.fixture
def token(client):
    data = UserFactory()
    user_data = {
        "fullname": data.fullname,
        "password": data.password,
        "email": data.email,
        "company_id": data.company.id
    }
    client.post("/registration/", json=user_data)
    response = client.post("/authorization/", json=user_data)
    session.query(models.User).filter_by(fullname=data.fullname).update({"is_staff": True})
    session.commit()
    return response.json()["access_token"]


@pytest.fixture
def not_staff_user_and_token(client):
    data = UserFactory()
    user_data = {
        "fullname": data.fullname,
        "password": data.password,
        "email": data.email,
        "company_id": data.company.id,
        "user_role_id": data.user_role.id
    }
    client.post("/registration/", json=user_data)
    response = client.post("/authorization/", json=user_data)
    return response.json()["access_token"], data


@pytest.fixture(scope="module", autouse=True)
def drop_db():
    yield None
    models.Base.metadata.drop_all(bind=engine)
    models.Base.metadata.create_all(bind=engine)


@pytest.fixture
def session_and_models():
    return session, models
