import firebase_admin
from firebase_admin import credentials, firestore
from flask_restful import Resource, reqparse
from flask import jsonify
from .model import *


class Subject(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('name')

    def get(self, userId, subjectId=None):
        if subjectId is None:
            subjects = getAllSubjects(userId)
            return jsonify({'subjects': subjects})
        else:
            subjectData = getSubjectById(userId, subjectId)
            if subjectData is None:
                return {'message': 'Subject not found'}, 404
            return jsonify(subjectData)

    def post(self, userId):
        args = self.parser.parse_args()
        newSubjectId = createNewSubject(userId, args['name'])
        return {'message': 'Subject created', 'subjectId': newSubjectId}, 201

    def put(self, subjectId):
        args = self.parser.parse_args()
        success = updateSubject(subjectId, args['name'])
        if success:
            return {'message': 'subject updated'}, 200
        return {'message': 'subject not found'}, 404

    def delete(self, subjectId):
        success = deleteSubject(subjectId)
        if success:
            return {'message': 'subject deleted'}, 200
        return {'message': 'subject not found'}, 404
    
    
    