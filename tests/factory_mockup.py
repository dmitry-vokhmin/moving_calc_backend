import random
import factory
from data_base.database import session_local
from factory import alchemy, Faker, SubFactory
from data_base import models
from sqlalchemy.orm import scoped_session

session = scoped_session(session_local)


def get_test_db():
    try:
        db = session
        yield db
    finally:
        db.close()


class ZipFactory(alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = models.ZipCode
        sqlalchemy_session = session
        sqlalchemy_session_persistence = "commit"

    id = Faker("pyint", min_value=2, max_value=100)
    zip_code = Faker("zipcode_in_state")
    city = Faker("city")
    state = Faker("state_abbr")


class AddressFactory(alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = models.Address
        sqlalchemy_session = session
        sqlalchemy_session_persistence = "commit"

    id = Faker("pyint", min_value=2, max_value=100)
    street = Faker("street_name")
    apartment = Faker("building_number")
    zip_code = SubFactory(ZipFactory)


class CompanyFactory(alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = models.Company
        sqlalchemy_session = session
        sqlalchemy_session_persistence = "commit"

    id = Faker("pyint", min_value=2, max_value=100)
    name = Faker("company")
    is_active = True
    address = SubFactory(AddressFactory)


class UserRoleFactory(alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = models.UserRole
        sqlalchemy_session = session
        sqlalchemy_session_persistence = "commit"

    id = Faker("pyint", min_value=2, max_value=100)
    role = random.choice(["admin", "owner", "sales"])


class UserFactory(factory.Factory):
    class Meta:
        model = models.User

    id = Faker("pyint", min_value=2, max_value=100)
    fullname = Faker("name")
    password = Faker("password")
    email = Faker("ascii_email")
    is_staff = True
    company = SubFactory(CompanyFactory)
    user_role = SubFactory(UserRoleFactory)


class UserPrivilegeFactory(alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = models.UserPrivilege
        sqlalchemy_session = session
        sqlalchemy_session_persistence = "commit"

    id = Faker("pyint", min_value=2, max_value=100)
    privilege = random.choice(["calculator", "equipment", "user_management", "configuration", "inventory"])



