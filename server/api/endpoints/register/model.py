import firebase_admin
from firebase_admin import credentials, firestore
from flask_restful import Resource, reqparse
from flask import jsonify
import api.appconfig as config
from enum import Enum

db = firestore.client()

class RegisterError(Enum):
    """
    Enum of possible errors that can occur when registering a user.

    Attributes:
      PASSWORD_MISSMATCH (int): Error code for when the passwords do not match.
      USER_ALREADY_EXISTS (int): Error code for when the user already exists.
    """
    PASSWORD_MISSMATCH = 1
    USER_ALREADY_EXISTS = 2
    
def tryRegisterUser(name, password, passwordConfirmation):
        """
    Attempts to register a user with the given name and password.

    Args:
      name (str): The name of the user to register.
      password (str): The password of the user to register.
      passwordConfirmation (str): The confirmation of the password.

    Returns:
      int: The ID of the user if successful, otherwise an error code from RegisterError.
    """
        if password != passwordConfirmation:
            return RegisterError.PASSWORD_MISSMATCH

        query = db.collection("users").where('name', '==', name)
        queryResp = query.stream()
        docs = [doc.to_dict() for doc in queryResp]

        if len(docs) != 0:
            return RegisterError.USER_ALREADY_EXISTS        
                
        time, ref = db.collection("users").add({
            "name": name,
            "password": password
            })        
        return ref.id
    
    
from videoOperations.fileStorageHelper import uploadUserImage
def uploadImage(file):
    """
    Uploads an image to the file storage.

    Args:
      file (file): The file to upload.

    Side Effects:
      Uploads the file to the file storage.

    Examples:
      >>> uploadImage(my_file)
      None
    """
    uploadUserImage(file)