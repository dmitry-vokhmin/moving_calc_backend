import factory
from factory import Faker, SubFactory
from data_base import models
from tests.factory_mockup import AddressFactory


class CompanyFactory(factory.Factory):
    class Meta:
        model = models.Company

    id = Faker("pyint", min_value=2, max_value=100)
    name = Faker("company")
    address = SubFactory(AddressFactory)
