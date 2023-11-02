import firebase_admin
from firebase_admin import credentials, firestore
from flask_restful import Resource, reqparse
from flask import jsonify
import api.appconfig as config

db = firestore.client()

def getSubjectById(userId, subjectId):
    ref = db.collection("users").document(userId).collection("subjects").document(subjectId)
    data = ref.get()
    if data.exists:
        return data.to_dict()
    else:
        return None


def createNewSubject(userId, name):
        time, ref = db.collection("users").document(userId).collection("subjects").add({
            "name": name,
            "conversationHistory" : []
            })        
        ref.update({"id": ref.id})       
        return ref.id

def updateSubject(userId, subjectId, name):
    ref = db.collection("users").document(userId).collection("subjects").document(subjectId)
    data = {
        "name": name,
    }
    ref.update(data)
    return True

def deleteSubject(userId, subjectId):
    ref = db.collection("users").document(userId).collection("subjects").document(subjectId)
    ref.delete()
    return True  

def getAllSubjects(userId):
    ref =  db.collection("users").document(userId).collection("subjects")  
    subjects = ref.stream()
    return [subject.to_dict() for subject in subjects]
    
    
# ------- VideoContentGenerator --------

from videoOperations.videoWorkflow import videoWorkflow

def generate(userId, subjectId):
    data = getSubjectById(userId, subjectId)
    subject = data["name"]
    videoWorkflow(userId, subjectId, subject)
    
    
    
# Chatbots

from chatbots.documentQuestionAnswering import documentQA
def postDocsPrompt(userId, subjectId, prompt):
    
    pass

def postGeneralPrompt(userId, subjectId, prompt):
    pass