from datetime import datetime

from gorest_api import GorestAPI
api = GorestAPI()

def get_users(page=1, per_page=5):
    params = {"page": page, "per_page": per_page}
    users = api.create_api_call("GET", api.USERS_URL, params=params)
    dict={}
    for user in users:
        dict[user['id']] = {
            "name": user['name'],
            "email": user['email'],
            "status": user['status']
        }
    return dict

def get_posts(page=1, per_page=5):
    params = {"page": page, "per_page": per_page}
    return api.create_api_call("GET", api.POSTS_URL, params=params)

def get_comments(page=1, per_page=5):
    params = {"page": page, "per_page": per_page}
    return api.create_api_call("GET", api.COMMENTS_URL, params=params)

def get_todos(page=1, per_page=5):
    params = {"page": page, "per_page": per_page}
    return api.create_api_call("GET", api.TODOS_URL, params=params)

def create_user(user_data):
    return api.create_api_call("POST", api.USERS_URL,data=user_data)


#get count of all users   before create user: 2944, after create user 2945
def get_user_count(per_page=100):
    total_users = 0
    page = 1
    while True:
        params = {"page": page, "per_page": per_page}
        response=api.create_api_call("GET", api.USERS_URL, params=params)
        if not response:
            break
        total_users += len(response)
        page += 1

    return total_users

#get user id by name
def get_user_id_by_name(name):
    params={"name": name}

    response = api.create_api_call("GET", api.USERS_URL, params=params)
    format_name=name.strip().lower()
    for user in response:
        if user['name'].strip().lower()==format_name:
            return user["id"]

#Display first 20 active users
def get_active_users(page=1, per_page=50):
    params = {"page": page, "per_page": per_page}

    response = api.create_api_call("GET", api.USERS_URL, params=params)
    active_users=[]

    for user in response:
        if user['status']=='active':
            active_users.append(user)
    first_20_users=active_users[:20]

    return first_20_users

def get_users_with_middle_name(page=1, per_page=50):
    params = {"page": page, "per_page": per_page}

    response = api.create_api_call("GET", api.USERS_URL, params=params)
    users_with_middle_name = []
    for user in response:
        name=user['name'].split()
        if len(name)>2:
            users_with_middle_name.append(user)
    firs_5_users=users_with_middle_name[:5]
    return firs_5_users


def create_post(user_id, post_data):
    return api.create_api_call("POST", f"{api.USERS_URL}/{user_id}/{api.POSTS_URL}",data=post_data)
def create_comment(post_id, post_data):
    #id will be id from posts, not user_id
    return api.create_api_call("POST", f"{api.POSTS_URL}/{post_id}/{api.COMMENTS_URL}", data=post_data)
def create_todos(user_id, post_data):
    return api.create_api_call("POST", f"{api.USERS_URL}/{user_id}/{api.TODOS_URL}",data=post_data)

def get_user_id(user_id):
    return api.create_api_call("GET", f"{api.USERS_URL}/{user_id}")

def update_email(user_id,new_email_data):
    return api.create_api_call("PUT", f"{api.USERS_URL}/{user_id}", data=new_email_data)

def convert_due_on(todo):
    return datetime.fromisoformat(todo['due_on'])

def get_sort_todos(page=1, per_page=50):
    params = {"page": page, "per_page": per_page}

    response = api.create_api_call("GET", api.TODOS_URL, params=params)
    todos20 = response[:20]
    sorted_todos = sorted(todos20, key=convert_due_on)
    return sorted_todos


if __name__ == "__main__":
    #get users
    print(get_users())

    #get posts
    posts = get_posts()
    for post in posts:
        print(post)

    #get comments
    comments = get_comments()
    for comment in comments:
        print(comment)

    #get todos
    todos = get_todos()
    for todo in todos:
        print(todo)

    new_user_data = {
        "name": "TestTest2",
        "email": "jtesttest12322222@ai.com",
        "gender": "male",
        "status": "active"
    }
    print(create_user(new_user_data))
#
    print(get_user_count())
    print(get_user_id_by_name("John Doe"))
    print(get_active_users())
    print(get_users_with_middle_name())
    user_id = 7474661
    post_data = {
        "title": "Sample title post",
        "body": "This is the content of the post"
    }

    created_post = create_post(user_id, post_data)
    print("Created Post:", created_post)

    post_id="162032"
    comments_data={
        "name": "Test2test2 Comment",
        "email": "testets2@doeecomment.ai",
        "body":"Fugit voluptatem eum. Nihil quo eligendi. Et laboriosam dolor"

    }
    comments = create_comment(post_id, comments_data)
    print("Created comment:", comments)


    todos_data={
        "title": "Title2test2e",
        "due_on": "2024-11-07T00:00:00.000+05:30",
        "status": "completed"
}
    print(create_todos(user_id,todos_data))

    print(get_user_id(user_id))
    email= {
        "email": "changed_email@mail.com"
 }
    print(update_email(user_id,email))

    print(get_sort_todos())


