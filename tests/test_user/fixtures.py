import pytest
from tests.factory_mockup import UserFactory, session


@pytest.fixture
def user_data():
    data = UserFactory()
    return {
        "fullname": data.fullname,
        "password": data.password,
        "email": data.email,
        "company_id": data.company.id
    }
