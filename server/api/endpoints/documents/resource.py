import firebase_admin
from firebase_admin import credentials, firestore
from flask_restful import Resource, reqparse
from flask import jsonify, request
from api.endpoints.documents.model import *


class Document(Resource):
    """
    Resource class for documents.
    """
    def __init__(self):
        """
        Initializes the Document class.

        Args:
          self (Document): The Document object.
        """
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("name")
        self.parser.add_argument("url")
        self.parser.add_argument("id")

    def get(self, userId, subjectId, documentId=None):
        """
        Retrieves a document or all documents from a subject.

        Args:
          userId (str): The user's ID.
          subjectId (str): The subject's ID.
          documentId (str, optional): The document's ID.

        Returns:
          dict: A dictionary containing the document or all documents from the subject.

        Examples:
          >>> Document.get(userId, subjectId, documentId)
          {'documents': [{'name': 'document1', 'url': 'www.example.com/document1'}, {'name': 'document2', 'url': 'www.example.com/document2'}]}
        """
        if documentId is None:
            documents = getAllDocuments(userId, subjectId)
            return jsonify({"documents": documents})
        else:
            subjectData = getDocumentById(userId, subjectId, documentId)
            if subjectData is None:
                return {"message": "Document not found"}, 404
            return jsonify(subjectData)

    def post(self, userId, subjectId):
        """
        Uploads a file and creates a document.

        Args:
          userId (str): The user's ID.
          subjectId (str): The subject's ID.

        Returns:
          dict: A dictionary containing the document IDs, URLs, and filenames of the uploaded files.

        Examples:
          >>> Document.post(userId, subjectId)
          {'message': 'Documents created', 'documentIds': ['document1', 'document2'], 'urls': ['www.example.com/document1', 'www.example.com/document2'], 'filenames': ['document1.txt', 'document2.txt']}
        """
        if "file" not in request.files:
            return {"message": "No file provided"}, 400
        
        documentIds = []
        urls = []
        filenames = []
        files = request.files.getlist("file")

        for file in files:
            url = uploadFile(file)
            if url is None:
                return {"message": "Fileupload failed", "AlreadyDone": {"documentIds": documentIds, "urls": urls, "filenames": filenames}}, 400
                
            newDocumentId = createNewDocument(userId, subjectId, file.filename, url)
            
            filenames.append(file.filename)
            urls.append(url)
            documentIds.append(newDocumentId)
            
        return {"message": "Documents created", "documentIds": documentIds, "urls": urls, "filenames": filenames}, 201

    def put(self, userId, subjectId, documentId):      
        """
        Updates a document.

        Args:
          userId (str): The user's ID.
          subjectId (str): The subject's ID.
          documentId (str): The document's ID.
          name (str): The new name of the document.
          url (str): The new URL of the document.

        Returns:
          dict: A dictionary containing a message indicating the success of the update.

        Examples:
          >>> Document.put(userId, subjectId, documentId, 'newName', 'www.example.com/newName')
          {'message': 'document updated'}
        """
        args = self.parser.parse_args()
        success = updateDocument(userId, subjectId, documentId,  args["name"], args["url"])
        if success:
            return {"message": "document updated"}, 200
        return {"message": "document not found"}, 404

    def delete(self, userId, subjectId, documentId):
        """
        Deletes a document.

        Args:
          userId (str): The user's ID.
          subjectId (str): The subject's ID.
          documentId (str): The document's ID.

        Returns:
          dict: A dictionary containing a message indicating the success of the delete.

        Examples:
          >>> Document.delete(userId, subjectId, documentId)
          {'message': 'document deleted'}
        """
        success = deleteDocument(userId, subjectId, documentId)
        if success:
            return {"message": "document deleted"}, 200
        return {"message": "document not found"}, 404
    
    
    