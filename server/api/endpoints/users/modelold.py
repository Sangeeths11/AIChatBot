import firebase_admin
from firebase_admin import credentials, firestore
from flask_restful import Resource, reqparse

db = firestore.client()


# User Model
class User(Resource):
    def __init__(self, firstname,lastname, email, id=None):
        self.id = id
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.topics = []

    def to_dict(self):
        return {
            "firstname": self.firstname,
            "lastname": self.lastname,
            "email": self.email,
            "topics": self.topics
        }
        
    #from_dict()
        
    def create(self):
        time, id = db.collection("users").add({
            self.to_dict()
        })        
        return id
        
    @classmethod
    def getAll(cls):
        docs = db.collection("users").stream()
        return docs