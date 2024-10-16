import requests
BASE_URL = "https://gorest.co.in/public/v2"

page = 0
all_ids = []

while True:
    response = requests.get(f"{BASE_URL}/users?page={page}&per_page=100", verify=False)

    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        break

    users = response.json()
    if not users:
        break

    user_ids = [user['id'] for user in users]
    all_ids.extend(user_ids)
    print(f"Page {page} found {len(users)} users. Ids: {user_ids}")

    if len(users) < 100:
        print(f"Nousers {page}.")
        break

    page += 1
print(f"Total ids: {len(all_ids)}")


