import pytest
from .factory_mockup import CompanyFactory


@pytest.fixture
def company_data():
    data = CompanyFactory()
    return {
        "name": data.name,
        "street": data.address.street,
        "apartment": data.address.apartment,
        "zip_code": data.address.zip_code.zip_code,
        "city": data.address.zip_code.city,
        "state": data.address.zip_code.state
    }
