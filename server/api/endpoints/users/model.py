import firebase_admin
from firebase_admin import credentials, firestore
from flask_restful import Resource, reqparse
from flask import jsonify



db = firestore.client()


# Functions to interact with your database (e.g., Firestore) would be defined here
# You should replace these placeholders with actual database operations

def getUserById(userId):
    user_ref = db.collection("Users").document(userId)
    user_data = user_ref.get()
    
    if user_data.exists:
        return user_data.to_dict()
    else:
        return None

def createNewUser(firstName, lastName, email):
        time, id = db.collection("users").add({
            "firstName": firstName,
            "lastName": lastName,
            "email": email})        
        return id

def updateUser(userId, firstName, lastName, email):
    user_ref = db.collection("Users").document(userId)
    
    user_data = {
        "firstname": firstName,
        "lastname": lastName,
        "email": email
    }

    # Update the user document with the new data
    user_ref.update(user_data)
    
    return True  # Assuming the update operation succeeded

def deleteUser(userId):
    user_ref = db.collection("Users").document(userId)
    
    # Delete the user document
    user_ref.delete()
    
    return True  # Assuming the delete operation succeeded
