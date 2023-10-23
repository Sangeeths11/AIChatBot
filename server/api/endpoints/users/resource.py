import firebase_admin
from firebase_admin import credentials, firestore
from flask_restful import Resource, reqparse
from flask import jsonify
from .model import *


class User(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('name')
        self.parser.add_argument('password')

    def get(self, userId= None):
        if userId is None:
            users = getAllUsers()
            return jsonify({'users': users})
        else:
            userData = getUserById(userId)
            if userData is None:
                return {'message': 'User not found'}, 404
            return jsonify(userData)


    def post(self):
        # Implement logic to create a new user
        args = self.parser.parse_args()
        newUserId = createNewUser(args["name"], args["password"])
        return {'message': 'User created', 'userId': newUserId}, 201

    def put(self, userId):
        # Implement logic to update an existing user by their ID
        args = self.parser.parse_args()
        success = updateUser(userId, args["name"], args["password"])
        if success:
            return {'message': 'User updated'}, 200
        return {'message': 'User not found'}, 404

    def delete(self, userId):
        # Implement logic to delete a user by their ID
        success = deleteUser(userId)
        if success:
            return {'message': 'User deleted'}, 200
        return {'message': 'User not found'}, 404
    

