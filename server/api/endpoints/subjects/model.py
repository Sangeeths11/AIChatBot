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
        "conversationHistoryDocsQuestions" : [],
        "conversationHistoryDocsAnswers" : [],
        "conversationHistoryGeneralQuestions" : [],
        "conversationHistoryGeneralAnswers" : [],
        })
    ref.update({"id": ref.id})

    if imageUrl:
        ref.update({"imageUrl" : imageUrl})
    return ref.id

# def updateSubject(userId, subjectId, imageUrl=None, name=None, conversationHistoryDocsQuestions=None, conversationHistoryDocsAnswers=None,  conversationHistoryGeneralQuestions=None, conversationHistoryGeneralAnswers=None):
#     ref = db.collection("users").document(userId).collection("subjects").document(subjectId)
#     data = {}
#     if name:
#         data["name"] = name
#     if imageUrl:
#         data["imageUrl"] = imageUrl
#     if conversationHistoryDocsQuestions:
#         data["conversationHistoryDocsQuestions"] = conversationHistoryDocsQuestions
#     if conversationHistoryDocsAnswers:
#         data["conversationHistoryDocsAnswers"] = conversationHistoryDocsAnswers
#     if conversationHistoryGeneralQuestions:
#         data["conversationHistoryGeneralQuestions"] = conversationHistoryGeneralQuestions
#     if conversationHistoryGeneralAnswers:
#         data["conversationHistoryGeneralAnswers"] = conversationHistoryGeneralAnswers
#     if data and ref:
#         ref.update(data)
#     return True
def updateSubject(userId, subjectId, imageUrl=None, name=None,
                  conversationHistoryDocsQuestions=None, conversationHistoryDocsAnswers=None,
                  conversationHistoryGeneralQuestions=None, conversationHistoryGeneralAnswers=None,
                  clearHistory=False):
    ref = db.collection("users").document(userId).collection("subjects").document(subjectId)
    data = {}

    if clearHistory:
        data["conversationHistoryDocsQuestions"] = []
        data["conversationHistoryDocsAnswers"] = []
        data["conversationHistoryGeneralQuestions"] = []
        data["conversationHistoryGeneralAnswers"] = []
    else:
        if name:
            data["name"] = name
        if imageUrl:
            data["imageUrl"] = imageUrl
        if conversationHistoryDocsQuestions is not None:
            data["conversationHistoryDocsQuestions"] = conversationHistoryDocsQuestions
        if conversationHistoryDocsAnswers is not None:
            data["conversationHistoryDocsAnswers"] = conversationHistoryDocsAnswers
        if conversationHistoryGeneralQuestions is not None:
            data["conversationHistoryGeneralQuestions"] = conversationHistoryGeneralQuestions
        if conversationHistoryGeneralAnswers is not None:
            data["conversationHistoryGeneralAnswers"] = conversationHistoryGeneralAnswers

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
    
from videoOperations.fileStorageHelper import uploadSubjectImage
def uploadImage(file):
    return uploadSubjectImage(file)
    
# ------- VideoContentGenerator --------

from videoOperations.videoWorkflow import videoWorkflow
# from api.app import celery

# @celery.task
def generate(userId, subjectId):
    data = getSubjectById(userId, subjectId)
    subject = data.get("name", None)
    result = videoWorkflow(userId, subjectId, subject)
    return result
    
