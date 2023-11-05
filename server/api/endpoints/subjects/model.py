import firebase_admin
from firebase_admin import credentials, firestore
from flask_restful import Resource, reqparse
from flask import jsonify



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

    if imageUrl:
        ref.update({"imageUrl" : imageUrl})
    return ref.id

def updateSubject(userId, subjectId, imageUrl=None, name=None, conversationHistoryDocs=None, conversationHistoryGeneral=None):
    ref = db.collection("users").document(userId).collection("subjects").document(subjectId)
    data = {}
    if name:
        data["name"] = name
    if imageUrl:
        data["imageUrl"] = imageUrl
    if conversationHistoryDocs:
        data["conversationHistoryDocs"] = conversationHistoryDocs
    if conversationHistoryGeneral:
        data["conversationHistoryGeneral"] = conversationHistoryGeneral
    if data:
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
    
from server.videoOperations.fileStorageHelper import uploadSubjectImage
def uploadImage(file):
    return uploadSubjectImage(file)
    
# ------- VideoContentGenerator --------

from server.videoOperations.videoWorkflow import videoWorkflow
# from api.app import celery

# @celery.task
def generate(userId, subjectId):
    data = getSubjectById(userId, subjectId)
    subject = data["name"]
    result = videoWorkflow(userId, subjectId, subject)
    return result.id
    
# ------------- Chatbots ---------------

from server.chatbots.documentQuestionAnswering import documentQA
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
    
    
    
    
# from server.chatbots.generalQuestionAnswering import ......
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
    