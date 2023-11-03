import firebase_admin
from firebase_admin import credentials, firestore
from flask_restful import Resource, reqparse
from flask import jsonify
import appconfig as config



db = firestore.client()

# Functions to interact with your database (e.g., Firestore) would be defined here
# You should replace these placeholders with actual database operations

def getUserById(userId):
    ref = db.collection("users").document(userId)
    userData = ref.get()
    
    if userData.exists:
        return userData.to_dict()
    else:
        return None

def createNewUser(name, password):
        time, ref = db.collection("users").add({
            "name": name,
            "password": password
            })        
        ref.update({"id": ref.id})
        return ref.id

def updateUser(userId, name, password):
    ref = db.collection("users").document(userId)
    data = {
            "name": name,
            "password": password
            }

    # Update the user document with the new data
    ref.update(data)
    
    return True  # Assuming the update operation succeeded

def deleteUser(userId):
    user_ref = db.collection("users").document(userId)
    user_ref.delete()
    
    return True  # Assuming the delete operation succeeded

def getAllUsers():
    usersRef = db.collection("users")  
    users = usersRef.stream()
    return [user.to_dict() for user in users]
    