from data_base import models
from tests.factory_mockup import AddressFactory


class AddressFactoryLocal(AddressFactory):
    class Meta:
        model = models.Address
