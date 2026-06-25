
class TestGetAllGoals:

    def test_get_all_goals_status_200(self, api):
        response = api.get_all_goals()
        print(response.json())
        assert response.status_code == 200

    def test_get_all_goals_returns_list(self, api):
        response = api.get_all_goals()
        body = response.json()
        assert "goals" in body
        assert isinstance(body["goals"], list)

    def test_get_all_goals_invalid_token_returns_401(self, api, invalid_headers):

        response = api.get_all_goals(headers = invalid_headers)
        assert response.status_code == 401, (
            f"Очікували 401, отримали {response.status_code}"
        )

    def test_get_all_goals_without_token_returns_401(self, api, no_token_headers):

        create_resp = api.create_goal("__test_no_token__")
        assert create_resp.status_code == 200
        goal_id = create_resp.json()["goal"]["id"]

        try:
            response = api.get_all_goals(headers = no_token_headers)
            assert response.status_code == 401
        finally:
            api.delete_goal(goal_id)

class TestCreateGoal:

    def test_create_goal_returns_200(self, api):
        response = api.create_goal("test_create_simple")
        assert response.status_code == 200
        goal = response.json()["goal"]
        assert goal["name"] == "test_create_simple"

        api.delete_goal(goal["id"])

    def test_create_goal_has_required_fields(self, api):
        response = api.create_goal("test_fields_check")
        assert response.status_code == 200
        goal = response.json()["goal"]
        for field in ("id", "name", "team_id"):
            assert field in goal, f"Відсутнє поле '{field}' у відповіді"
        api.delete_goal(goal["id"])

    def test_create_goal_name_matches(self, api):
        name = "unique_goal_name_abc123"
        response = api.create_goal(name)
        assert response.status_code == 200
        goal = response.json()["goal"]
        assert goal["name"] == name
        api.delete_goal(goal["id"])

class TestGetGoal:

    def test_get_goal_returns_200(self, api, created_goal):

        response = api.get_goal(created_goal["id"])
        print(f"URL: {response.url}")
        print(f"Response: {response.json()}")
        assert response.status_code == 200

    def test_get_goal_correct_data(self, api, created_goal):

        response = api.get_goal(created_goal["id"])
        assert response.status_code == 200
        goal = response.json()["goal"]
        assert goal["id"] == created_goal["id"]
        assert goal["name"] == created_goal["name"]

    def test_get_goal_invalid_id_returns_error(self, api):

        response = api.get_goal("000000000000")
        assert response.status_code in (400, 404), (
            f"Очікували 400/404, отримали {response.status_code}"
        )

class TestUpdateGoal:

    def test_update_goal_returns_200(self, api, created_goal):

        response = api.update_goal(created_goal["id"], "updated_name_test")
        assert response.status_code == 200

    def test_update_goal_name_changes(self, api, created_goal):

        new_name = "goal_renamed_xyz"
        api.update_goal(created_goal["id"], new_name)

        get_resp = api.get_goal(created_goal["id"])
        assert get_resp.status_code == 200
        assert get_resp.json()["goal"]["name"] == new_name

    def test_update_goal_without_token_returns_401(self, api, no_token_headers):

        create_resp = api.create_goal("__test_update_no_token__")
        assert create_resp.status_code == 200
        goal_id = create_resp.json()["goal"]["id"]

        try:
            response = api.INVALID_HEADERS.update_goal(goal_id, "hacked_name")
            assert response.status_code == 401
        finally:
            api.delete_goal(goal_id)

    def test_update_nonexistent_goal_returns_error(self, api):
        response = api.update_goal("000000000000", "ghost_name")
        assert response.status_code in (400, 404)

class TestDeleteGoal:

    def test_delete_goal_returns_200(self, api):

        create_resp = api.create_goal("__test_to_delete__")
        assert create_resp.status_code == 200
        goal_id = create_resp.json()["goal"]["id"]

        delete_resp = api.delete_goal(goal_id)
        assert delete_resp.status_code == 200

    def test_deleted_goal_is_not_accessible(self, api):

        create_resp = api.create_goal("__test_delete_then_get__")
        assert create_resp.status_code == 200
        goal_id = create_resp.json()["goal"]["id"]

        api.delete_goal(goal_id)

        get_resp = api.get_goal(goal_id)
        assert get_resp.status_code in (400, 404), (
            f"Видалена ціль все ще повертає {get_resp.status_code}"
        )

    def test_delete_goal_without_token_returns_401(self, api, no_token_headers):

        create_resp = api.create_goal("__test_delete_no_token__")
        assert create_resp.status_code == 200
        goal_id = create_resp.json()["goal"]["id"]

        try:
            response = api.NO_TOKEN_HEADERS.delete_goal(goal_id)
            assert response.status_code == 401
        finally:
            api.delete_goal(goal_id)

    def test_delete_nonexistent_goal_returns_error(self, api):

        response = api.delete_goal("000000000000")
        assert response.status_code in (400, 404)