from flask import Flask, jsonify
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from werkzeug.exceptions import HTTPException
from werkzeug.exceptions import default_exceptions
import settings

app = Flask(__name__)


@app.errorhandler(Exception)
def handle_error(e):
    code = 500
    if isinstance(e, HTTPException):
        code = e.code
    return jsonify(error=str(e)), code

for ex in default_exceptions:
    app.register_error_handler(ex, handle_error)


# app.config['SQLALCHEMY_DATABASE_URI'] = settings.SQLALCHEMY_DATABASE_URI
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = settings.SQLALCHEMY_TRACK_MODIFICATIONS
# app.config['BUNDLE_ERRORS'] = settings.BUNDLE_ERRORS
# db = SQLAlchemy(app)



api = Api(app)
api.prefix = '/api'

from endpoints.users.resource import User

api.add_resource(User, '/users', '/users/<int:user_id>')
#         api.add_resource(UserAPI, '/user/profile/',resource_class_kwargs=resource_class_kwargs)

if __name__ == '__main__':
    app.run()
