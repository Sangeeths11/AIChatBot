import firebase_admin
from firebase_admin import credentials, firestore
from flask_restful import Resource, reqparse
from flask import jsonify



db = firestore.client()

def getSubjectById(userId, subjectId):
    """
    Retrieves a subject from the database.

    Args:
      userId (str): The ID of the user.
      subjectId (str): The ID of the subject.

    Returns:
      dict: A dictionary containing the subject data.
      None: If the subject does not exist.

    Examples:
      >>> getSubjectById("user1", "subject1")
      {
        "name": "subject1",
        "conversationHistoryDocsQuestions": [],
        "conversationHistoryDocsAnswers": [],
        "conversationHistoryGeneralQuestions": [],
        "conversationHistoryGeneralAnswers": []
      }
    """
    ref = db.collection("users").document(userId).collection("subjects").document(subjectId)
    data = ref.get()
    if data.exists:
        return data.to_dict()
    else:
        return None


def createNewSubject(userId, name, imageUrl=None):
    """
    Creates a new subject in the database.

    Args:
      userId (str): The ID of the user.
      name (str): The name of the subject.
      imageUrl (str, optional): The URL of the subject's image.

    Returns:
      str: The ID of the newly created subject.

    Examples:
      >>> createNewSubject("user1", "subject1", "imageUrl1")
      "subject1"
    """
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
    """
    Updates a subject in the database.

    Args:
      userId (str): The ID of the user.
      subjectId (str): The ID of the subject.
      imageUrl (str, optional): The URL of the subject's image.
      name (str, optional): The name of the subject.
      conversationHistoryDocsQuestions (list, optional): A list of questions from documents.
      conversationHistoryDocsAnswers (list, optional): A list of answers from documents.
      conversationHistoryGeneralQuestions (list, optional): A list of general questions.
      conversationHistoryGeneralAnswers (list, optional): A list of general answers.
      clearHistory (bool, optional): Whether to clear the conversation history.

    Returns:
      bool: True if the subject was updated, False otherwise.

    Examples:
      >>> updateSubject("user1", "subject1", name="subject2")
      True
    """
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
    """
    Deletes a subject from the database.

    Args:
      userId (str): The ID of the user.
      subjectId (str): The ID of the subject.

    Returns:
      bool: True if the subject was deleted, False otherwise.

    Examples:
      >>> deleteSubject("user1", "subject1")
      True
    """
    ref = db.collection("users").document(userId).collection("subjects").document(subjectId)
    ref.delete()
    return True  

def getAllSubjects(userId):
    """
    Retrieves all subjects from the database.

    Args:
      userId (str): The ID of the user.

    Returns:
      list: A list of dictionaries containing the subject data.

    Examples:
      >>> getAllSubjects("user1")
      [
        {
          "name": "subject1",
          "conversationHistoryDocsQuestions": [],
          "conversationHistoryDocsAnswers": [],
          "conversationHistoryGeneralQuestions": [],
          "conversationHistoryGeneralAnswers": []
        },
        {
          "name": "subject2",
          "conversationHistoryDocsQuestions": [],
          "conversationHistoryDocsAnswers": [],
          "conversationHistoryGeneralQuestions": [],
          "conversationHistoryGeneralAnswers": []
        }
      ]
    """
    ref =  db.collection("users").document(userId).collection("subjects")  
    subjects = ref.stream()
    return [subject.to_dict() for subject in subjects]
    
from videoOperations.fileStorageHelper import uploadSubjectImage
def uploadImage(file):
    """
    Uploads an image to the file storage.

    Args:
      file (file): The image file.

    Returns:
      str: The URL of the uploaded image.

    Examples:
      >>> uploadImage(file1)
      "imageUrl1"
    """
    return uploadSubjectImage(file)
    
# ------- VideoContentGenerator --------

from videoOperations.videoWorkflow import videoWorkflow
# from api.app import celery

# @celery.task
def generate(userId, subjectId):
    """
    Generates a video from the subject data.

    Args:
      userId (str): The ID of the user.
      subjectId (str): The ID of the subject.

    Returns:
      str: The URL of the generated video.

    Examples:
      >>> generate("user1", "subject1")
      "videoUrl1"
    """
    data = getSubjectById(userId, subjectId)
    subject = data.get("name", None)
    result = videoWorkflow(userId, subjectId, subject)
    return result
    
