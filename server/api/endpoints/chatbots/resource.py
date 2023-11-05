import firebase_admin
from firebase_admin import credentials, firestore
from flask_restful import Resource, reqparse
from flask import jsonify
from api.endpoints.chatbotGenerall.model import *


class ChatbotGenerall(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        # self.parser.add_argument('name')
        # self.parser.add_argument('password')

    def get(self, conversationToken):
        args = self.parser.parse_args()

        if conversationToken is None:
            return {'message': "Token invalid"}, 404
        
        
        
        return jsonify(userData)


    def post(self):
        # sends request
        args = self.parser.parse_args()
        newUserId = createNewUser(args["name"], args["password"])
        return {'message': 'User created', 'conversationToken': conversationToken}, 201

