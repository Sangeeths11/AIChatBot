from firebase_admin import credentials, firestore
from flask import jsonify

db = firestore.client()

def getDocumentById(userId, subjectId, documentId):
    ref = db.collection("users").document(userId).collection("subjects").document(subjectId).collection("documents").document(documentId)
    data = ref.get()
    if data.exists:
        return data.to_dict()
    else:
        return None

def createNewDocument(userId, subjectId, name, url):
        time, ref = db.collection("users").document(userId).collection("subjects").document(subjectId).collection("documents").add({
            "name": name,
            "url": url,
            }) 
        ref.update({"id": ref.id})       
        return ref.id

def updateDocument(userId, subjectId, documentId, name, url):
    ref = db.collection("users").document(userId).collection("subjects").document(subjectId).collection("documents").document(documentId)
    data = {
            "name": name,
            "url": url
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
    
    
    
from videoOperations.fileStorageHelper import uploadDocumentFile
def uploadFile(file):
    return uploadDocumentFile(file)
    