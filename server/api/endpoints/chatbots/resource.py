import firebase_admin
from firebase_admin import credentials, firestore
from flask_restful import Resource, reqparse
from flask import jsonify
from api.endpoints.chatbots.model import getConversationHistory, promptChatbot



class Chatbot(Resource):
    """
    Resource for handling chatbot requests.
    """
    def __init__(self):
        """
        Initializes the Chatbot resource.

        Args:
          None

        Returns:
          None
        """
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("chatbot")
        self.parser.add_argument("count")
        self.parser.add_argument("prompt")
        self.parser.add_argument("id")

    def get(self, userId, subjectId):
        """
        Retrieves the conversation history for a given user and subject.

        Args:
          userId (str): The ID of the user.
          subjectId (str): The ID of the subject.
          chatbot (str, optional): The chatbot to use.
          count (int, optional): The number of conversation steps to retrieve.

        Returns:
          dict: A dictionary containing the message and conversation history.
        """
        args = self.parser.parse_args()
        hist = getConversationHistory(userId, subjectId, chatbot=args.get("chatbot", None), count=args.get("count", None))
        return {"message": "ConversationHistory retrived", "conversationHistory": hist}, 200


    def post(self, userId, subjectId):
        """
        Prompts the chatbot with a given prompt.

        Args:
          userId (str): The ID of the user.
          subjectId (str): The ID of the subject.
          chatbot (str, optional): The chatbot to use.
          prompt (str): The prompt to send to the chatbot.

        Returns:
          dict: A dictionary containing the message, question, and answer.
        """
        args = self.parser.parse_args()
        conversationStep = promptChatbot(userId, subjectId, chatbot=args.get("chatbot", None), prompt=args["prompt"] )
        return {"message": "Sent successfully", "question": conversationStep.get("question", ""), "answer": conversationStep.get("answer", "")}