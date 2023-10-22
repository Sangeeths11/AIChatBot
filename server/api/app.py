from flask import Flask, jsonify
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from werkzeug.exceptions import HTTPException
from werkzeug.exceptions import default_exceptions
import appconfig as config
import firebase_admin
from firebase_admin import credentials, firestore

app = Flask(__name__)


@app.errorhandler(Exception)
def handle_error(e):
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
api.prefix = '/api'

# import resources
from endpoints.users.resource import User
from endpoints.subjects.resource import Subject
from endpoints.documents.resource import Document
from endpoints.videos.resource import Video

api.add_resource(User, '/users', '/users/<string:userId>')
api.add_resource(Subject, '/users/<string:userId>/subjects', '/users/<string:userId>/subjects/<string:subjectId>')
api.add_resource(Document, '/users/<string:userId>/subjects/<string:subjectId>/documents','/users/<string:userId>/subjects/<string:subjectId>/documents/<string:documentId>')
api.add_resource(Video, '/users/<string:userId>/subjects/<string:subjectId>/videos','/users/<string:userId>/subjects/<string:subjectId>/videos/<string:videoId>')


if __name__ == '__main__':
    app.run()
