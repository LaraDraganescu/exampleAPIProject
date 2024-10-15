from datetime import datetime

import requests
import json
from flask import Flask, jsonify, request

app=Flask(__name__)

BASE_URL = "https://gorest.co.in/public/v2"
token="009a45cfe9eb237ab4befe424a04f5c81789d0521c9c9dfef311b5957848a976"

@app.route('/users',methods=['GET'])
def get_users():
    response=requests.get(f"{BASE_URL}/users?page=1&per_page=50",verify=False)
    users=response.json()
    # formatted_users = []
    # for user in users:
    #     formatted_users.append({
    #         "id": user["id"],
    #         "name": user["name"],
    #         "email": user["email"],
    #         "status": user["status"]
    #     })
    # return formatted_users
    return jsonify(users)

@app.route('/posts',methods=['GET'])
def get_posts():
    response=requests.get(f"{BASE_URL}/posts?page=1&per_page=50",verify=False)
    posts=response.json()
    return jsonify(posts)

@app.route('/comments',methods=['GET'])
def get_comments():
    response=requests.get(f"{BASE_URL}/comments?page=1&per_page=50",verify=False)
    comments=response.json()
    return jsonify(comments)

@app.route('/todos',methods=['GET'])
def get_todos():
    response=requests.get(f"{BASE_URL}/todos?page=1&per_page=50",verify=False)
    todos=response.json()
    return jsonify(todos)


#Create user
@app.route('/createUser', methods=['POST'])
def create_user():
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    user_data=request.json
    response = requests.post(f"{BASE_URL}/users",headers=headers, json=user_data,verify=False)
    return jsonify(response.json())
    # if response.status_code==200:
    #     return jsonify(response.json()),200



#get count of all users
def get_user_count():
    response = requests.get(f"{BASE_URL}/users", verify=False)
    if response.status_code == 200:
        return len(response.json())
    else:
        return 0

@app.route('/userCount', methods=['GET'])
def user_count():
    count=get_user_count()
    return jsonify({"total_users":count}),200


#get user id by name
@app.route('/getUserIdByName', methods=['GET'])
def get_user_id_by_name():
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    name = request.args.get('name')
    response = requests.get(f"{BASE_URL}/users",headers=headers, verify=False)
    if response.status_code == 200:
        users = response.json()
        format_name=name.strip().lower()

        for user in users:
            if user['name'].strip().lower()==format_name:
                return jsonify({"id": user["id"]}),200
        return jsonify({"error":"User not found"})


#Display first 20 active users
@app.route('/activeUsers', methods=['GET'])
def get_active_users():
    response = requests.get(f"{BASE_URL}/users?page=1&per_page=50", verify=False)
    if response.status_code == 200:
        users = response.json()
        active_users=[]

        for user in users:
            if user['status']=='active':
                active_users.append(user)
        first_20_users=active_users[:20]

        return jsonify(first_20_users)


@app.route('/usersWithMiddleName', methods=['GET'])
def get_users_with_middle_name():
    response = requests.get(f"{BASE_URL}/users?page=1&per_page=50", verify=False)
    if response.status_code == 200:
        users = response.json()
        users_with_middle_name = []
        for user in users:
            name=user['name'].split()
            if len(name)>2:
                users_with_middle_name.append(user)
        firs_5_users=users_with_middle_name[:5]
        return jsonify(firs_5_users)


@app.route('/createPost', methods=['POST'])
def create_post():
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    user_id = request.args.get('id')
    post_data = request.json

    response = requests.post(f"{BASE_URL}/users/{user_id}/posts",headers=headers, json=post_data,verify=False)
    return jsonify(response.json())


@app.route('/createComment', methods=['POST'])
def create_comment():
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    #id will be id from posts, not user_id
    user_id = request.args.get('id')
    post_data = request.json

    response = requests.post(f"{BASE_URL}/posts/{user_id}/comments",headers=headers, json=post_data,verify=False)
    return jsonify(response.json())


@app.route('/createTodos', methods=['POST'])
def create_todos():
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    user_id = request.args.get('id')
    post_data = request.json

    response = requests.post(f"{BASE_URL}/users/{user_id}/todos",headers=headers, json=post_data,verify=False)
    return jsonify(response.json())



@app.route('/getUserById', methods=['GET'])
def get_user_id():
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    user_id = request.args.get('id')
    response = requests.get(f"{BASE_URL}/users/{user_id}", headers=headers, verify=False)

    return jsonify(response.json())


@app.route('/getPostById', methods=['GET'])
def get_post_id():
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    #this will be user_id
    user_id = request.args.get('id')
    response = requests.get(f"{BASE_URL}/users/{user_id}/posts", headers=headers, verify=False)

    return jsonify(response.json())

#update e-mail for a specific id
@app.route('/updateEmail', methods=['PUT'])
def update_email():
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    user_id = request.args.get('id')
    new_email_data = request.json

    response = requests.put(f"{BASE_URL}/users/{user_id}", headers=headers,json=new_email_data,verify=False)
    return jsonify(response.json()), 200

def convert_due_on(todo):
    return datetime.fromisoformat(todo['due_on'].replace('Z', '+00:00'))

#sort todos
@app.route('/getTodosSorted', methods=['GET'])
def get_sort_todos():
    response = requests.get(f"{BASE_URL}/todos?page=1&per_page=50", verify=False)
    if response.status_code == 200:
        todos = response.json()
        todos20 = todos[:20]

        sorted_todos = sorted(todos20, key=convert_due_on)
        return jsonify(sorted_todos)

if __name__ == '__main__':
    app.run(debug=True, port=8080)


