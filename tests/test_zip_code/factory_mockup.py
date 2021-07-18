import factory
from factory import Faker
from data_base import models


class ZipFactory(factory.Factory):
    class Meta:
        model = models.ZipCode

    id = Faker("pyint", min_value=2, max_value=100)
    zip_code = Faker("zipcode_in_state")
    city = Faker("city")
    state = Faker("state_abbr")
