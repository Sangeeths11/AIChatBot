import firebase_admin
from firebase_admin import credentials, firestore
from flask_restful import Resource, reqparse
from flask import jsonify, request
from api.endpoints.register.model import uploadImage, tryRegisterUser, RegisterError


class Register(Resource):
    """
    Resource for registering a new user.
    """
    def __init__(self):
        """
        Initializes the Register class.

        Args:
          self (Register): The Register instance.
        """
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('name')
        self.parser.add_argument('password')
        self.parser.add_argument('passwordConfirmation')


    def post(self):
        """
        Handles a POST request for registering a new user.

        Args:
          self (Register): The Register instance.

        Returns:
          dict: A message and userId if successful, or an error message if unsuccessful.

        Examples:
          >>> Register.post()
          {'message': 'User created', 'userId': newUserId}
        """
        args = self.parser.parse_args()
        imageUrl = None
        if "file" not in request.files:
            newUserId = tryRegisterUser(args["name"], args["password"], args["passwordConfirmation"])
        else:
            file = request.files["file"]
            imageUrl = uploadImage(file)
            if imageUrl is None:
                return {"message": "Fileupload failed"}, 400
            newUserId = tryRegisterUser(args["name"], args["password"], args["passwordConfirmation"], imageUrl)
        
        if newUserId is RegisterError.PASSWORD_MISSMATCH:
            return {'message': 'Passwords do not match'}, 400
        elif newUserId is RegisterError.USER_ALREADY_EXISTS:
            return {'message': 'A user with this name already exists, login instead'}, 409
        
        if imageUrl is None:
            return {'message': 'User created', 'userId': newUserId}, 201
        return {'message': 'User created', 'userId': newUserId, "imageUrl": imageUrl}, 201
