import pytest
from .factory_mockup import ZipFactory
from tests.factory_mockup import ZipFactory as ZipFactoryDB


@pytest.fixture
def zip_code_data():
    data = ZipFactory()
    return {"zip_code": data.zip_code, "city": data.city, "state": data.state}


@pytest.fixture
def zip_code_data_from_db():
    data = ZipFactoryDB()
    return {"zip_code": data.zip_code}
