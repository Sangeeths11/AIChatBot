import firebase_admin
from firebase_admin import credentials, firestore
from flask_restful import Resource, reqparse
from flask import jsonify
from .model import *


class Video(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('name')
        self.parser.add_argument('url')

    def get(self, userId, subjectId, videoId=None):
        if videoId is None:
            videos = getAllVideos(userId, subjectId)
            return jsonify({'videos': videos})
        else:
            subjectData = getVideoById(userId, subjectId, videoId)
            if subjectData is None:
                return {'message': 'video not found'}, 404
            return jsonify(subjectData)

    def post(self, userId, subjectId):
        args = self.parser.parse_args()
        newVideoId = createNewVideo(userId, subjectId, args['name'], args['url'])
        return {'message': 'Video created', 'videoId': newVideoId}, 201

    def put(self, userId, subjectId, videoId):
        args = self.parser.parse_args()
        success = updateVideo(userId, subjectId, videoId,  args['name'], args['url'])
        if success:
            return {'message': 'video updated'}, 200
        return {'message': 'video not found'}, 404

    def delete(self, userId, subjectId, videoId):
        success = deleteVideo(userId, subjectId, videoId)
        if success:
            return {'message': 'video deleted'}, 200
        return {'message': 'video not found'}, 404
    
    
    