import firebase_admin
from firebase_admin import credentials, firestore
from flask_restful import Resource, reqparse
from flask import jsonify,request
from api.endpoints.users.model import *


class User(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("name")
        self.parser.add_argument("password")
        self.parser.add_argument("id")

    def get(self, userId= None):
        if userId is None:
            users = getAllUsers()
            return jsonify({"users": users})
        else:
            userData = getUserById(userId)
            if userData is None:
                return {"message": "User not found"}, 404
            return jsonify(userData)


    def post(self):
        args = self.parser.parse_args()
        if "file" not in request.files:
            newUserId = createNewUser(args["name"], args["password"])
            return {"message": "User created", "userId": newUserId}, 201
        file = request.files["file"]      
        imageUrl = uploadImage(file)
        if imageUrl is None:
            return {"message": "Fileupload failed"}, 400
        newUserId = createNewUser(args["name"], args["password"], imageUrl)
        return {"message": "User created", "userId": newUserId, "imageUrl" : imageUrl}, 201


    def put(self, userId):
        args = self.parser.parse_args()
        success = updateUser(userId, args["name"], args["password"])
        if success:
            return {"message": "User updated"}, 200
        return {"message": "User not found"}, 404

    def delete(self, userId):
        success = deleteUser(userId)
        if success:
            return {"message": "User deleted"}, 200
        return {"message": "User not found"}, 404
    

