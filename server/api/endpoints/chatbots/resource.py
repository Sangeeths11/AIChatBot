import firebase_admin
from firebase_admin import credentials, firestore
from flask_restful import Resource, reqparse
from flask import jsonify
from api.endpoints.chatbots.model import getConversationHistory, promptChatbot



class Chatbot(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("chatbot")
        self.parser.add_argument("count")
        self.parser.add_argument("prompt")
        self.parser.add_argument("id")

    def get(self, userId, subjectId):
        args = self.parser.parse_args()
        hist = getConversationHistory(userId, subjectId, chatbot=args.get("chatbot", None), count=args.get("count", None))
        return {"message": "ConversationHistory retrived", "conversationHistory": hist}, 200


    def post(self, userId, subjectId):
        args = self.parser.parse_args()
        promptChatbot(userId, subjectId, chatbot=args.get("chatbot", None), prompt=args["prompt"] )
        return {"message": "prompt has been posted"}