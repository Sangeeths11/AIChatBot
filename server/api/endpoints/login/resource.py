import firebase_admin
from firebase_admin import credentials, firestore
from flask_restful import Resource, reqparse
from flask import jsonify
from api.endpoints.login.model import *


class Login(Resource):
    """
    Resource for logging in a user.
    """
    def __init__(self):
        """
        Initializes the Login resource.

        Args:
          None

        Returns:
          None
        """
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('name')
        self.parser.add_argument('password')

    def post(self):
        """
        Logs in a user.

        Args:
          name (str): The name of the user.
          password (str): The password of the user.

        Returns:
          dict: A dictionary containing a message and either the userId or name of the user.
          int: The HTTP status code.

        Examples:
          >>> post(name='John', password='password123')
          {'message': 'User logged in', 'userId': '12345'}, 201
        """
        args = self.parser.parse_args()
        newUserId = tryLogin(args["name"], args["password"])
        
        if newUserId is None:
            return {'message': 'User does not exist', 'name': args["name"]}, 404
        return {'message': 'User logged in', 'userId': newUserId}, 201

