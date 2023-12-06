import firebase_admin
from firebase_admin import credentials, firestore
from flask_restful import Resource, reqparse
from flask import jsonify
import api.appconfig as config



db = firestore.client()

# Functions to interact with your database (e.g., Firestore) would be defined here
# You should replace these placeholders with actual database operations

def tryLogin(name, password):
    """
    Attempts to log in a user with the given name and password.

    Args:
      name (str): The name of the user.
      password (str): The password of the user.

    Returns:
      str: The ID of the user if the login is successful, None otherwise.

    Examples:
      >>> tryLogin('John', 'password123')
      '123456789'
    """

    query = db.collection("users").where('name', '==', name).where('password', '==', password)
    queryResp = query.stream()
    docs = [doc for doc in queryResp]
    if len(docs) == 1:
        return docs[0].id
    return None