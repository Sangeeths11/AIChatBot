import firebase_admin
from firebase_admin import credentials, firestore
from flask_restful import Resource, reqparse
from flask import jsonify
# import server.api.appconfig as config

db = firestore.client()

def getSubjectById(userId, subjectId):
    ref = db.collection("users").document(userId).collection("subjects").document(subjectId)
    data = ref.get()
    if data.exists:
        return data.to_dict()
    else:
        return None


def createNewSubject(userId, name, imageUrl=None):
        time, ref = db.collection("users").document(userId).collection("subjects").add({
            "name": name,
            "conversationHistoryDocs" : [],
            "conversationHistoryGeneral" : [],
            })        
        ref.update({"id": ref.id})       
        
        if imageUrl is not None:
            ref.update({"imageUrl" : imageUrl})
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
    
from videoOperations.fileStorageHelper import uploadSubjectImage
def uploadImage(file):
    uploadSubjectImage(file)
    
# ------- VideoContentGenerator --------

from videoOperations.videoWorkflow import videoWorkflow

def generate(userId, subjectId):
    data = getSubjectById(userId, subjectId)
    subject = data["name"]
    videoWorkflow(userId, subjectId, subject)
    
    
    
# ------------- Chatbots ---------------

from chatbots.documentQuestionAnswering import documentQA
def postDocsPrompt(userId, subjectId, prompt):
    
    # add prompt
    ref = db.collection("users").document(userId).collection("subjects").document(subjectId)
    hist = ref.get().to_dict()["conversationHistoryDocs"]
    hist.append([prompt, ""])
    data = {
        "conversationHistoryDocs" : hist
    }
    ref.update(data)

    # get answer
    answer = documentQA(userId, subjectId, prompt)
    
    # add the answer
    hist[-1] = [prompt, answer]
    data = {
        "conversationHistoryDocs" : hist
    }
    ref.update(data)
    
    
    
    
# from chatbots.generalQuestionAnswering import ......
def postGeneralPrompt(userId, subjectId, prompt):
    
    # add prompt
    ref = db.collection("users").document(userId).collection("subjects").document(subjectId)
    hist = ref.get().to_dict()["conversationHistoryGeneral"]
    hist.append([prompt, ""])
    data = {
        "conversationHistoryGeneral" : hist
    }
    ref.update(data)


    answer = "Get General bot answer"


    # add the answer
    hist[-1] = [prompt, answer]
    data = {
        "conversationHistoryGeneral" : hist
    }
    ref.update(data)
    