import firebase_admin
from firebase_admin import credentials, firestore
from flask_restful import Resource, reqparse
from flask import jsonify, request
from .model import *


class Subject(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("name")
        self.parser.add_argument("id")
        self.parser.add_argument("imageUrl")
        self.parser.add_argument("conversationHistoryDocs")
        self.parser.add_argument("conversationHistoryGeneral")


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
        if "file" not in request.files:
            newSubjectId = createNewSubject(userId, args["name"])
            return {"message": "Subject created", "subjectId": newSubjectId}, 201
        file = request.files["file"]      
        imageUrl = uploadImage(file)
        if not imageUrl:
            return {"message": "Fileupload failed"}, 400
        newSubjectId = createNewSubject(userId, args["name"], imageUrl)
        return {"message": "Subject created", "subjectId": newSubjectId, "imageUrl" : imageUrl}, 201

    def put(self, userId, subjectId):
        args = self.parser.parse_args()
        
        if "file" in request.files:
            file = request.files["file"]      
            imageUrl = uploadImage(file)
        if not imageUrl:
            return {"message": "Fileupload failed"}, 400
        
        success = updateSubject(userId, subjectId, name=args["name"], imageUrl=imageUrl)
        if success:
            return {"message": "subject updated"}, 200
        return {"message": "subject not found"}, 404

    def delete(self, userId, subjectId):
        success = deleteSubject(userId, subjectId)
        if success:
            return {"message": "subject deleted"}, 200
        return {"message": "subject not found"}, 404
    

from endpoints.videos.model import getAllVideos
class VideoContentGenerator(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        
        
    def post(self, userId, subjectId):
        args = self.parser.parse_args()

        # resultId of celery worker
        #generate.apply_async(args=[userId, subjectId])
        generate(userId,subjectId)
        return {"message": "Subject content is being generated", "subjectId": subjectId}, 201


class Conversation(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("botType")
        self.parser.add_argument("userPromp")
        
    def post(self, userId, subjectId):
        args = self.parser.parse_args() 
        
        
        user = args["userPromp"]
        
        
        if args["botType"] == "docs":
            postDocsPrompt(userId, subjectId, args["userPrompt"])
            
        
        elif args["botType"] is None or args["botType"] == "general":
            # TODO call Thomas logic :D
            # postGeneralPrompt(userId, subjectId, args["userPrompt"])

            pass