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

def createNewUser(name, password, imageUrl = None):
    time, ref = db.collection("users").add({
        "name": name,
        "password": password
        })        
    ref.update({"id": ref.id})
    if imageUrl is not None:
        ref.update({"imageUrl" : imageUrl})
    return ref.id
    
    
def updateUser(userId, name, password):
    ref = db.collection("users").document(userId)
    data = {
            "name": name,
            "password": password
            }
    ref.update(data)
    return True 

def deleteUser(userId):
    user_ref = db.collection("users").document(userId)
    user_ref.delete()
    return True 

def getAllUsers():
    usersRef = db.collection("users")  
    users = usersRef.stream()
    return [user.to_dict() for user in users]
    
from videoOperations.fileStorageHelper import uploadUserImage
def uploadImage(file):
    uploadUserImage(file)