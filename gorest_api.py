import requests

class GorestAPI:
    # BASE_URL = "https://gorest.co.in/public/v2"
    TOKEN = "009a45cfe9eb237ab4befe424a04f5c81789d0521c9c9dfef311b5957848a976"
    USERS_URL = "/users"
    POSTS_URL = "/posts"
    TODOS_URL = "/todos"
    COMMENTS_URL = "/comments"

    def __init__(self):
        self.base_url = "https://gorest.co.in/public/v2"
        self.headers = {
            "Authorization": f"Bearer {self.TOKEN}",
            "Content-Type": "application/json"
        }
    def create_api_call(self,method,endpoint,params=None,data=None):
        url = f"{self.base_url}{endpoint}"
        if method == "GET":
            response = requests.get(url, headers=self.headers, params=params, verify=False)
        elif method == "POST":
            response = requests.post(url, headers=self.headers, json=data, verify=False)
        elif method == "PUT":
            response = requests.put(url, headers=self.headers, json=data, verify=False)
        else:
            return None
        return response.json()
