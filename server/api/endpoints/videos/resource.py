import firebase_admin
from firebase_admin import credentials, firestore
from flask_restful import Resource, reqparse
from flask import jsonify
from api.endpoints.videos.model import *


class Video(Resource):
    """
    Resource class for video endpoints.
    """
    def __init__(self):
        """
        Initializes the Video class.

        Args:
          self (Video): The Video object.
        """
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("name")
        self.parser.add_argument("url")
        self.parser.add_argument("transcriptUrl")
        self.parser.add_argument("id")
        #self.parser.add_argument("summary")


    def get(self, userId, subjectId, videoId=None):
        """
        Retrieves a video or all videos from the database.

        Args:
          self (Video): The Video object.
          userId (str): The user ID.
          subjectId (str): The subject ID.
          videoId (str, optional): The video ID.

        Returns:
          dict: A dictionary containing the video or videos.

        Examples:
          >>> Video.get(userId, subjectId)
          {'videos': [{'name': 'Video 1', 'url': 'www.example.com/video1', 'transcriptUrl': 'www.example.com/video1/transcript'}, {'name': 'Video 2', 'url': 'www.example.com/video2', 'transcriptUrl': 'www.example.com/video2/transcript'}]}
        """
        if videoId is None:
            videos = getAllVideos(userId, subjectId)
            return jsonify({"videos": videos})
        else:
            videoData = getVideoById(userId, subjectId, videoId)
            if videoData is None:
                return {"message": "video not found"}, 404
            return jsonify(videoData)

    def post(self, userId, subjectId):
        """
        Creates a new video in the database.

        Args:
          self (Video): The Video object.
          userId (str): The user ID.
          subjectId (str): The subject ID.

        Returns:
          dict: A dictionary containing the message and video ID.

        Examples:
          >>> Video.post(userId, subjectId)
          {'message': 'Video created', 'videoId': '12345'}
        """
        args = self.parser.parse_args()
        newVideoId = createNewVideo(userId, subjectId, args["name"], args["url"], args["transcriptUrl"])
        return {"message": "Video created", "videoId": newVideoId}, 201

    def put(self, userId, subjectId, videoId):
        """
        Updates an existing video in the database.

        Args:
          self (Video): The Video object.
          userId (str): The user ID.
          subjectId (str): The subject ID.
          videoId (str): The video ID.

        Returns:
          dict: A dictionary containing the message.

        Examples:
          >>> Video.put(userId, subjectId, videoId)
          {'message': 'video updated'}
        """
        args = self.parser.parse_args()
        success = updateVideo(userId, subjectId, videoId,  args["name"], args["url"], args["transcriptUrl"])
        if success:
            return {"message": "video updated"}, 200
        return {"message": "video not found"}, 404

    def delete(self, userId, subjectId, videoId):
        """
        Deletes an existing video from the database.

        Args:
          self (Video): The Video object.
          userId (str): The user ID.
          subjectId (str): The subject ID.
          videoId (str): The video ID.

        Returns:
          dict: A dictionary containing the message.

        Examples:
          >>> Video.delete(userId, subjectId, videoId)
          {'message': 'video deleted'}
        """
        success = deleteVideo(userId, subjectId, videoId)
        if success:
            return {"message": "video deleted"}, 200
        return {"message": "video not found"}, 404
 