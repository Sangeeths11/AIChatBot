import firebase_admin
from firebase_admin import credentials, firestore
from flask_restful import Resource, reqparse
from flask import jsonify
import appconfig as config



db = firestore.client()

def getSubjectById(userId, subjectId):
    subjectRef = db.collection("users").document(userId).collection("subjects").document(subjectId)
    subjectData = subjectRef.get()
    
    if subjectData.exists:
        return subjectData.to_dict()
    else:
        return None

def createNewSubject(userId, name):
        time, id = db.collection("users").document(userId).collection("subjects").add({
            "name": name
            })        
        return id

def updateSubject(userId, subjectId, name):
    subjectRef = db.collection("users").document(userId).collection("subjects")
    subjectData = {
        "name": name
    }

    subjectRef.update(subjectData)
    return True

def deleteSubject(userId, subjectId):
    subjectRef = db.collection("users").document(userId).collection("subjects")
    subjectRef.delete()
    return True  

def getAllSubjects(userId):
    subjectsRef =  db.collection("users").document(userId).collection("subjects")  
    subjects = subjectsRef.stream()
    return [subject.to_dict() for subject in subjects]
    