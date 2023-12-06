import firebase_admin
from firebase_admin import credentials, firestore
from flask_restful import Resource, reqparse
from flask import jsonify,request
from api.endpoints.users.model import *


class User(Resource):
    """
    Resource class for user endpoints.
    """
    def __init__(self):
        """
        Initializes the User class.

        Args:
          None

        Returns:
          None
        """
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("name")
        self.parser.add_argument("password")
        self.parser.add_argument("id")

    def get(self, userId= None):
        """
        Retrieves a user or all users.

        Args:
          userId (int, optional): The ID of the user to retrieve.

        Returns:
          dict: A dictionary containing the user data or a list of all users.

        Examples:
          >>> User.get(1)
          {'name': 'John', 'password': '12345', 'id': 1}
          >>> User.get()
          [{'name': 'John', 'password': '12345', 'id': 1}, {'name': 'Jane', 'password': 'abcde', 'id': 2}]
        """
        if userId is None:
            users = getAllUsers()
            return jsonify({"users": users})
        else:
            userData = getUserById(userId)
            if userData is None:
                return {"message": "User not found"}, 404
            return jsonify(userData)


    def post(self):
        """
        Creates a new user.

        Args:
          name (str): The name of the user.
          password (str): The password of the user.
          file (file, optional): An image file to upload.

        Returns:
          dict: A dictionary containing the user ID and image URL (if applicable).

        Examples:
          >>> User.post('John', '12345')
          {'message': 'User created', 'userId': 1}
          >>> User.post('John', '12345', file)
          {'message': 'User created', 'userId': 1, 'imageUrl': 'https://example.com/image.jpg'}
        """
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
        """
        Updates a user.

        Args:
          userId (int): The ID of the user to update.
          name (str): The name of the user.
          password (str): The password of the user.

        Returns:
          dict: A dictionary containing a success message.

        Examples:
          >>> User.put(1, 'John', '12345')
          {'message': 'User updated'}
        """
        args = self.parser.parse_args()
        success = updateUser(userId, args["name"], args["password"])
        if success:
            return {"message": "User updated"}, 200
        return {"message": "User not found"}, 404

    def delete(self, userId):
        """
        Deletes a user.

        Args:
          userId (int): The ID of the user to delete.

        Returns:
          dict: A dictionary containing a success message.

        Examples:
          >>> User.delete(1)
          {'message': 'User deleted'}
        """
        success = deleteUser(userId)
        if success:
            return {"message": "User deleted"}, 200
        return {"message": "User not found"}, 404
    

