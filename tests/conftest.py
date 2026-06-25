
import pytest
from goals.goals_api_helper import GoalsApiHelper

@pytest.fixture(scope="session")
def api():
    return GoalsApiHelper()

@pytest.fixture(scope="session")
def invalid_headers():
    return GoalsApiHelper.INVALID_HEADERS

@pytest.fixture(scope="session")
def no_token_headers():
    return GoalsApiHelper.NO_TOKEN_HEADERS

@pytest.fixture
def created_goal(api):
    response = api.create_goal("__test_lifecycle_goal__")
    print(response.url)
    print(response.json())
    assert response.status_code == 200
    goal = response.json()["goal"]
    yield goal
    api.delete_goal(goal["id"])