import firebase_admin
from firebase_admin import credentials, firestore
from flask_restful import Resource, reqparse
from flask import jsonify
from .model import *


class Subject(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("name")
        self.parser.add_argument("id")

    def get(self, userId, subjectId=None):
        if subjectId is None:
            subjects = getAllSubjects(userId)
            return jsonify({"subjects": subjects})
        else:
            subjectData = getSubjectById(userId, subjectId)
            if subjectData is None:
                return {"message": "Subject not found"}, 404
            return jsonify(subjectData)

    def post(self, userId):
        args = self.parser.parse_args()
        newSubjectId = createNewSubject(userId, args["name"])
        return {"message": "Subject created", "subjectId": newSubjectId}, 201

    def put(self, userId, subjectId):
        args = self.parser.parse_args()
        success = updateSubject(userId, subjectId, args["name"])
        if success:
            return {"message": "subject updated"}, 200
        return {"message": "subject not found"}, 404

    def delete(self, subjectId):
        success = deleteSubject(subjectId)
        if success:
            return {"message": "subject deleted"}, 200
        return {"message": "subject not found"}, 404
    
    
from endpoints.videos.model import getAllVideos
class VideoContentGenerator(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        
        
    def post(self, userId, subjectId):
        args = self.parser.parse_args()

        url = generate(userId, subjectId)
        videosForSubject = getAllVideos(userId, subjectId)
        return {"message": "Subject content generated", "subjectId": subjectId, "transcripts":  videosForSubject}, 201


# New endpoint for this too, since idk how otherwise :D
class Conversation(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("botType")
        self.parser.add_argument("userPromp")
        
    # post new conversation entry, add it to the subjects list of messages of the current converation
    def post(self, userId, subjectId):
        args = self.parser.parse_args() # whats passed in the body
        
        
        user = args["userPromp"]
        
        
        if args["botType"] == "documents":
            postDocsPrompt(userId, subjectId, args["userPrompt"])
            
        
        elif args["botType"] is None or args["botType"] == "general":
            # TODO call Thomas logic :D
            # postGeneralPrompt(userId, subjectId, args["userPrompt"])

            pass