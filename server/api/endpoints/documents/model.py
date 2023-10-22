import firebase_admin
from firebase_admin import credentials, firestore
from flask_restful import Resource, reqparse
from flask import jsonify
import appconfig as config

db = firestore.client()

def getDocumentById(userId, subjectId, documentId):
    ref = db.collection("users").document(userId).collection("subjects").document(subjectId).collection("documents").document(documentId)
    data = ref.get()
    if data.exists:
        return data.to_dict()
    else:
        return None

def createNewDocument(userId, subjectId, title):
        time, ref = db.collection("users").document(userId).collection("subjects").document(subjectId).collection("documents").add({
            "title": title
            })        
        return ref.id

def updateDocument(userId, subjectId, documentId, title):
    ref = db.collection("users").document(userId).collection("subjects").document(subjectId).collection("documents").document(documentId)
    data = {
        "title": title
    }

    ref.update(data)
    return True

def deleteDocument(userId, subjectId, documentId):
    ref = db.collection("users").document(userId).collection("subjects").document(subjectId).collection("documents").document(documentId)
    ref.delete()
    return True  

def getAllDocuments(userId, subjectId):
    ref =  db.collection("users").document(userId).collection("subjects").document(subjectId).collection("documents")  
    documents = ref.stream()
    return [docs.to_dict() for docs in documents]
    