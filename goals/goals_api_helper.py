import requests

class GoalsApiHelper:
    BASE_URL = "https://api.clickup.com/api/v2"
    TEAM_ID = "90121762516"
    HEADERS = {
        'Authorization': 'pk_302462603_1XI8DMDJ143Z6Y9O643PPQH82LGRDQHK',
        'Content-Type': 'application/json'
    }

    INVALID_HEADERS = {
        "Authorization": "invalid_token_xyz",
        "Content-Type": "application/json",
    }

    NO_TOKEN_HEADERS = {
        "Content-Type": "application/json",
    }

    def get_all_goals(self, headers=None):
        return requests.get(self.BASE_URL + "/team/" + self.TEAM_ID + "/goal",
                            headers=headers or self.HEADERS)

    def get_goal(self, folder_id, headers=None):
        return requests.get(self.BASE_URL + "/goal/" + folder_id + "/",
                            headers=headers or self.HEADERS)

    def create_goal(self, goal_name, headers=None):
        return requests.post(self.BASE_URL + "/team/" + self.TEAM_ID + "/goal",
                             headers=headers or self.HEADERS,
                             json={'name': goal_name})

    def update_goal(self, goal_id, updated_goal_name, headers=None):
        return requests.put(self.BASE_URL + "/goal/" + goal_id + "/",
                            headers=headers or self.HEADERS,
                            json={'name': updated_goal_name})

    def delete_goal(self, goal_id, headers=None):
        return requests.delete(self.BASE_URL + "/goal/" + goal_id,
                               headers=headers or self.HEADERS)