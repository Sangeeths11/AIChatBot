import firebase_admin
from firebase_admin import credentials, firestore
from flask_restful import Resource, reqparse
from flask import jsonify
from .model import *


class Register(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('name')
        self.parser.add_argument('password')
        self.parser.add_argument('passwordConfirmation')


    def post(self):
        args = self.parser.parse_args()
        newUserId = tryRegisterUser(args["name"], args["password"], args["passwordConfirmation"])
        
        if newUserId is RegisterError.PASSWORD_MISSMATCH:
            return {'message': 'Passwords do not match'}, 400
        elif newUserId is RegisterError.USER_ALREADY_EXISTS:
            return {'message': 'A user with this name already exists, login instead'}, 409
        return {'message': 'User created', 'userId': newUserId}, 201

