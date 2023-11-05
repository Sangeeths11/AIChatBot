import firebase_admin
from firebase_admin import credentials, firestore
from flask_restful import Resource, reqparse
from flask import jsonify
from server.api.endpoints.login.model import *


class Login(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('name')
        self.parser.add_argument('password')

    def post(self):
        args = self.parser.parse_args()
        newUserId = tryLogin(args["name"], args["password"])
        
        if newUserId is None:
            return {'message': 'User does not exist', 'name': args["name"]}, 404
        return {'message': 'User logged in', 'userId': newUserId}, 201

