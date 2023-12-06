import firebase_admin
from firebase_admin import credentials, firestore
from flask_restful import Resource, reqparse
from flask import jsonify, request
from api.endpoints.subjects.model import *
import json

class Subject(Resource):
    """
    Resource for managing subjects.
    """
    def __init__(self):
        """
        Initializes the Subject resource.
        """
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("name")
        self.parser.add_argument("id")
        self.parser.add_argument("imageUrl")
        self.parser.add_argument("conversationHistoryDocsQuestions")
        self.parser.add_argument("conversationHistoryDocsAnswers")

        self.parser.add_argument("conversationHistoryGeneralQuestions")
        self.parser.add_argument("conversationHistoryGeneralAnswers")

    def get(self, userId, subjectId=None):
        """
        Gets a subject by id.

        Args:
          userId (str): The user's id.
          subjectId (str): The subject's id.

        Returns:
          dict: The subject data.

        Examples:
          >>> Subject.get('userId', 'subjectId')
          {'name': 'subjectName', 'id': 'subjectId', 'imageUrl': 'imageUrl', 'conversationHistoryDocsQuestions': [], 'conversationHistoryDocsAnswers': [], 'conversationHistoryGeneralQuestions': [], 'conversationHistoryGeneralAnswers': []}
        """
        if subjectId is None:
            subjects = getAllSubjects(userId)
            return jsonify({"subjects": subjects})
        else:
            subjectData = getSubjectById(userId, subjectId)
            if subjectData is None:
                return {"message": "Subject not found"}, 404
            return jsonify(subjectData)

    def post(self, userId):
        """
        Creates a new subject.

        Args:
          userId (str): The user's id.
          name (str): The subject's name.
          file (file): The subject's image file.

        Returns:
          dict: The subject data.

        Examples:
          >>> Subject.post('userId', 'subjectName', file)
          {'message': 'Subject created', 'subjectId': 'subjectId', 'imageUrl': 'imageUrl'}
        """
        imageUrl = None
        if "file" not in request.files:
            newSubjectId = createNewSubject(userId, request.args.get("name"))
            return {"message": "Subject created", "subjectId": newSubjectId}, 201
        file = request.files["file"]      
        imageUrl = uploadImage(file)
        if not imageUrl:
            return {"message": "Fileupload failed"}, 400
        newSubjectId = createNewSubject(userId, request.args.get("name"), imageUrl)
        return {"message": "Subject created", "subjectId": newSubjectId, "imageUrl" : imageUrl}, 201

    def put(self, userId, subjectId):
        """
        Updates a subject.

        Args:
          userId (str): The user's id.
          subjectId (str): The subject's id.
          file (file): The subject's image file.

        Returns:
          dict: The subject data.

        Examples:
          >>> Subject.put('userId', 'subjectId', file)
          {'message': 'subject updated'}
        """
        imageUrl = None
        if "file" in request.files:
            file = request.files["file"]
            imageUrl = uploadImage(file)
        if not imageUrl:
            return {"message": "Fileupload failed"}, 400

        success = updateSubject(userId, subjectId, imageUrl=imageUrl)
        if success:
            return {"message": "subject updated"}, 200
        return {"message": "subject not found"}, 404

    def delete(self, userId, subjectId):
        """
        Deletes a subject.

        Args:
          userId (str): The user's id.
          subjectId (str): The subject's id.

        Returns:
          dict: The subject data.

        Examples:
          >>> Subject.delete('userId', 'subjectId')
          {'message': 'subject deleted'}
        """
        success = deleteSubject(userId, subjectId)
        if success:
            return {"message": "subject deleted"}, 200
        return {"message": "subject not found"}, 404
    
    
from api.endpoints.videos.model import getAllVideos
class VideoContentGenerator(Resource):
    """
    Resource for generating video content.
    """
    def __init__(self):
        """
        Initializes the VideoContentGenerator resource.
        """
        self.parser = reqparse.RequestParser()
        
        
    def post(self, userId, subjectId):
        """
        Generates video content for a subject.

        Args:
          userId (str): The user's id.
          subjectId (str): The subject's id.

        Returns:
          dict: The subject data.

        Examples:
          >>> VideoContentGenerator.post('userId', 'subjectId')
          {'message': 'Subject content is being generated', 'subjectId': 'subjectId'}
        """
        args = self.parser.parse_args()

        # resultId of celery worker
        #generate.apply_async(args=[userId, subjectId])
        result = generate(userId,subjectId)
        return {"message": "Subject content is being generated", "subjectId": subjectId}, 201

