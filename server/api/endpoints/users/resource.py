from flask import Flask, request, jsonify
from model import User

app = Flask(__name__)

# Route to create a new user
@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    user = User(id=None, name=data['name'], email=data['email'])
    user_id = save_user(user)
    return jsonify({'id': user_id}), 201

# Route to get all users
@app.route('/users', methods=['GET'])
def get_all_users():
    users = get_all_users_from_db()
    user_dicts = [user.to_dict() for user in users]
    return jsonify({'users': user_dicts})

