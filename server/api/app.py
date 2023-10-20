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

# import ressources
from endpoints.users.resource import User

api.add_resource(User, '/users', '/users/<string:user_id>')


if __name__ == '__main__':
    app.run()
