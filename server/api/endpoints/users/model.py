import firebase_admin
from firebase_admin import credentials, firestore
from flask_restful import Resource, reqparse
from flask import jsonify
import appconfig as config



db = firestore.client()

# Functions to interact with your database (e.g., Firestore) would be defined here
# You should replace these placeholders with actual database operations

def getUserById(userId):
    user_ref = db.collection("users").document(userId)
    user_data = user_ref.get()
    
    if user_data.exists:
        return user_data.to_dict()
    else:
        return None

def createNewUser(firstName, lastName, email):
        time, ref = db.collection("users").add({
            "firstname": firstName,
            "lastname": lastName,
            "email": email})        
        return ref.id

def updateUser(userId, firstName, lastName, email):
    user_ref = db.collection("users").document(userId)
    
    user_data = {
        "firstname": firstName,
        "lastname": lastName,
        "email": email
    }

    # Update the user document with the new data
    user_ref.update(user_data)
    
    return True  # Assuming the update operation succeeded

def deleteUser(userId):
    user_ref = db.collection("users").document(userId)
    
    # Delete the user document
    user_ref.delete()
    
    return True  # Assuming the delete operation succeeded

def getAllUsers():
    usersRef = db.collection("users")  
    users = usersRef.stream()
    return [user.to_dict() for user in users]
    