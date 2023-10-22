import firebase_admin
from firebase_admin import credentials, firestore
from flask_restful import Resource, reqparse
from flask import jsonify
from .model import *


class Document(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('name')
        self.parser.add_argument('url')

    def get(self, userId, subjectId, documentId=None):
        if documentId is None:
            documents = getAllDocuments(userId, subjectId)
            return jsonify({'documents': documents})
        else:
            subjectData = getDocumentById(userId, subjectId, documentId)
            if subjectData is None:
                return {'message': 'Document not found'}, 404
            return jsonify(subjectData)

    def post(self, userId, subjectId):
        args = self.parser.parse_args()
        newDocumentId = createNewDocument(userId, subjectId, args['name'], args['url'])
        return {'message': 'Document created', 'documentId': newDocumentId}, 201

    def put(self, userId, subjectId, documentId):
        args = self.parser.parse_args()
        success = updateDocument(userId, subjectId, documentId,  args['name'], args['url'])
        if success:
            return {'message': 'document updated'}, 200
        return {'message': 'document not found'}, 404

    def delete(self, userId, subjectId, documentId):
        success = deleteDocument(userId, subjectId, documentId)
        if success:
            return {'message': 'document deleted'}, 200
        return {'message': 'document not found'}, 404
    
    
    