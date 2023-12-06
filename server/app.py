# Prepare
# import sys
# sys.path.append('server')

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

# Imports
from flask import Flask, jsonify
from flask_restful import Api
from werkzeug.exceptions import HTTPException
from werkzeug.exceptions import default_exceptions
import api.appconfig as config
import firebase_admin
from firebase_admin import credentials, firestore
from flask import Flask, jsonify
from flask_restful import Api
from flask_cors import CORS

# from celery import Celery

app = Flask(__name__)
CORS(app)

# app.config["CELERY_BROKER_URL"] = config.CELERY_BROKER_URL
# app.config["CELERY_RESULT_BACKEND"] = config.CELERY_RESULT_BACKEND
# app.config["CELERY_INCLUDE"] = ["endpoints.subjects.model"]  

# celery = Celery(
#     app.name,
#     broker=app.config["CELERY_BROKER_URL"],
#     result_backend=app.config["CELERY_RESULT_BACKEND"]
# )
# celery.conf.update(app.config)
# celery -A app.celery worker

def main():
    """
    Initializes the Flask app and adds resources.

    Args:
      None

    Returns:
      None

    Side Effects:
      Initializes Firebase and adds resources to the Flask app.

    Examples:
      >>> main()
    """
    @app.errorhandler(Exception)
    def handle_error(e):
        """
    Handles errors and returns a JSON response.

    Args:
      e (Exception): The exception to handle.

    Returns:
      jsonify: A JSON response with the error message.

    Side Effects:
      None

    Examples:
      >>> handle_error(HTTPException)
      {'error': 'HTTPException'}
    """
        code = 500
        if isinstance(e, HTTPException):
            code = e.code
        return jsonify(error=str(e)), code

    for ex in default_exceptions:
        app.register_error_handler(ex, handle_error)


    # Initialize Firebase
    cred = credentials.Certificate(config.CREDENTIALS_PATH)
    firebase_admin.initialize_app(cred)


    api = Api(app)
    api.prefix = "/api"

    # import resources
    from api.endpoints.register.resource import Register
    from api.endpoints.login.resource import Login

    from api.endpoints.users.resource import User
    from api.endpoints.subjects.resource import Subject
    from api.endpoints.documents.resource import Document
    from api.endpoints.videos.resource import Video
    from api.endpoints.subjects.resource import VideoContentGenerator
    from api.endpoints.chatbots.resource import Chatbot

    api.add_resource(Register, "/register")
    api.add_resource(Login, "/login")
    api.add_resource(User, "/users", "/users/<string:userId>")
    api.add_resource(Subject, "/users/<string:userId>/subjects", "/users/<string:userId>/subjects/<string:subjectId>")
    api.add_resource(Document, "/users/<string:userId>/subjects/<string:subjectId>/documents","/users/<string:userId>/subjects/<string:subjectId>/documents/<string:documentId>")
    api.add_resource(Video, "/users/<string:userId>/subjects/<string:subjectId>/videos","/users/<string:userId>/subjects/<string:subjectId>/videos/<string:videoId>")
    api.add_resource(VideoContentGenerator, "/users/<string:userId>/subjects/<string:subjectId>/generate")
    api.add_resource(Chatbot, "/users/<string:userId>/subjects/<string:subjectId>/chats")

    app.run()

if __name__ == "__main__":
    main()