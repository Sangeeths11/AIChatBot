import firebase_admin
from firebase_admin import credentials, firestore
from flask_restful import Resource, reqparse
from flask import jsonify
import api.appconfig as config
from enum import Enum

db = firestore.client()

class RegisterError(Enum):
    PASSWORD_MISSMATCH = 1
    USER_ALREADY_EXISTS = 2
    
def tryRegisterUser(name, password, passwordConfirmation):
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
    uploadUserImage(file)