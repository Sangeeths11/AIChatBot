from firebase_admin import credentials, firestore
from flask import jsonify

db = firestore.client()

def getDocumentById(userId, subjectId, documentId):
    """
    Retrieves a document from the database.

    Args:
      userId (str): The ID of the user.
      subjectId (str): The ID of the subject.
      documentId (str): The ID of the document.

    Returns:
      dict: A dictionary containing the document data.
      None: If the document does not exist.

    Examples:
      >>> getDocumentById('user1', 'subject1', 'document1')
      {'name': 'Document 1', 'url': 'www.example.com/document1'}
    """
    ref = db.collection("users").document(userId).collection("subjects").document(subjectId).collection("documents").document(documentId)
    data = ref.get()
    if data.exists:
        return data.to_dict()
    else:
        return None

def createNewDocument(userId, subjectId, name, url):
        """
    Creates a new document in the database.

    Args:
      userId (str): The ID of the user.
      subjectId (str): The ID of the subject.
      name (str): The name of the document.
      url (str): The URL of the document.

    Returns:
      str: The ID of the newly created document.

    Examples:
      >>> createNewDocument('user1', 'subject1', 'Document 1', 'www.example.com/document1')
      'document1'
    """
        time, ref = db.collection("users").document(userId).collection("subjects").document(subjectId).collection("documents").add({
            "name": name,
            "url": url,
            }) 
        ref.update({"id": ref.id})       
        return ref.id

def updateDocument(userId, subjectId, documentId, name, url):
    """
    Updates an existing document in the database.

    Args:
      userId (str): The ID of the user.
      subjectId (str): The ID of the subject.
      documentId (str): The ID of the document.
      name (str): The name of the document.
      url (str): The URL of the document.

    Returns:
      bool: True if the document was successfully updated.

    Examples:
      >>> updateDocument('user1', 'subject1', 'document1', 'Document 2', 'www.example.com/document2')
      True
    """
    ref = db.collection("users").document(userId).collection("subjects").document(subjectId).collection("documents").document(documentId)
    data = {
            "name": name,
            "url": url
            }

    ref.update(data)
    return True

def deleteDocument(userId, subjectId, documentId):
    """
    Deletes an existing document from the database.

    Args:
      userId (str): The ID of the user.
      subjectId (str): The ID of the subject.
      documentId (str): The ID of the document.

    Returns:
      bool: True if the document was successfully deleted.

    Examples:
      >>> deleteDocument('user1', 'subject1', 'document1')
      True
    """
    ref = db.collection("users").document(userId).collection("subjects").document(subjectId).collection("documents").document(documentId)
    ref.delete()
    return True  

def getAllDocuments(userId, subjectId):
    """
    Retrieves all documents from the database.

    Args:
      userId (str): The ID of the user.
      subjectId (str): The ID of the subject.

    Returns:
      list: A list of dictionaries containing the document data.

    Examples:
      >>> getAllDocuments('user1', 'subject1')
      [{'name': 'Document 1', 'url': 'www.example.com/document1'}, {'name': 'Document 2', 'url': 'www.example.com/document2'}]
    """
    ref =  db.collection("users").document(userId).collection("subjects").document(subjectId).collection("documents")  
    documents = ref.stream()
    return [docs.to_dict() for docs in documents]
    
    
    
from videoOperations.fileStorageHelper import uploadDocumentFile
def uploadFile(file):
    """
    Uploads a file to the file storage.

    Args:
      file (file): The file to be uploaded.

    Returns:
      str: The URL of the uploaded file.

    Examples:
      >>> uploadFile(file)
      'www.example.com/file'
    """
    return uploadDocumentFile(file)
    