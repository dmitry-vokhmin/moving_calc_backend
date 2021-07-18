import pytest
from .factory_mockup import AddressFactory
from tests.factory_mockup import AddressFactory as AddressFactoryDB


@pytest.fixture
def address_data():
    data = AddressFactory()
    return {"street": data.street, "apartment": data.apartment, "zip_code_id": data.zip_code.id}


@pytest.fixture
def address_from_db():
    data = AddressFactoryDB()
    return {"address_id": data.id}
