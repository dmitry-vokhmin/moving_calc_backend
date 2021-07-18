import pytest
from tests.factory_mockup import UserPrivilegeFactory


@pytest.fixture
def token_and_user_privilege(not_staff_user_and_token, session_and_models):
    session = session_and_models[0]
    token, user = not_staff_user_and_token
    user_privilege = UserPrivilegeFactory()
    user_privilege.user_role.append(user.user_role)
    session.commit()
    return token, user_privilege.privilege
