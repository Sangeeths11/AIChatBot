import firebase_admin
from firebase_admin import credentials, firestore
from flask_restful import Resource, reqparse
from flask import jsonify
import api.appconfig as config



db = firestore.client()

# Functions to interact with your database (e.g., Firestore) would be defined here
# You should replace these placeholders with actual database operations

def getUserById(userId):
    """
    Retrieves a user from the database by their ID.

    Args:
      userId (str): The ID of the user to retrieve.

    Returns:
      dict: A dictionary containing the user's data, or None if the user does not exist.

    Examples:
      >>> getUserById("12345")
      {
        "name": "John Doe",
        "password": "password123",
        "imageUrl": "https://example.com/image.jpg"
      }
    """
    ref = db.collection("users").document(userId)
    userData = ref.get()
    
    if userData.exists:
        return userData.to_dict()
    else:
        return None

def createNewUser(name, password, imageUrl = None):
    """
    Creates a new user in the database.

    Args:
      name (str): The name of the user.
      password (str): The user's password.
      imageUrl (str, optional): The URL of the user's profile image.

    Returns:
      str: The ID of the newly created user.

    Examples:
      >>> createNewUser("John Doe", "password123", "https://example.com/image.jpg")
      "12345"
    """
    time, ref = db.collection("users").add({
        "name": name,
        "password": password
        })        
    ref.update({"id": ref.id})
    if imageUrl is not None:
        ref.update({"imageUrl" : imageUrl})
    return ref.id
    
    
def updateUser(userId, name, password):
    """
    Updates an existing user in the database.

    Args:
      userId (str): The ID of the user to update.
      name (str): The new name of the user.
      password (str): The new password of the user.

    Returns:
      bool: True if the user was successfully updated, False otherwise.

    Examples:
      >>> updateUser("12345", "John Smith", "password456")
      True
    """
    ref = db.collection("users").document(userId)
    data = {
            "name": name,
            "password": password
            }
    ref.update(data)
    return True 

def deleteUser(userId):
    """
    Deletes an existing user from the database.

    Args:
      userId (str): The ID of the user to delete.

    Returns:
      bool: True if the user was successfully deleted, False otherwise.

    Examples:
      >>> deleteUser("12345")
      True
    """
    user_ref = db.collection("users").document(userId)
    user_ref.delete()
    return True 

def getAllUsers():
    """
    Retrieves all users from the database.

    Returns:
      list: A list of dictionaries containing the data of all users.

    Examples:
      >>> getAllUsers()
      [
        {
          "name": "John Doe",
          "password": "password123",
          "imageUrl": "https://example.com/image.jpg"
        },
        {
          "name": "John Smith",
          "password": "password456",
          "imageUrl": "https://example.com/image2.jpg"
        }
      ]
    """
    usersRef = db.collection("users")  
    users = usersRef.stream()
    return [user.to_dict() for user in users]
    
from videoOperations.fileStorageHelper import uploadUserImage
def uploadImage(file):
    """
    Uploads an image to the file storage service.

    Args:
      file (str): The file to upload.

    Returns:
      None

    Side Effects:
      Uploads the file to the file storage service.

    Examples:
      >>> uploadImage("image.jpg")
      None
    """
    uploadUserImage(file)