# resource.py defines the routes and endpoints for the restapi
# resource.py focuses on handling HTTP requests and responses
# Handles the https requests
# It is responsible for managing the HTTP request-response cycle, parsing request data, validating input, and serializing data to send back as responses.
# It typically does not interact directly with the database but instead relies on the model.py file to perform database operations.



# resource.py

from flask import Flask, request, jsonify
from model import User, Topic, Document, Video

app = Flask(__name__)

# Route to create a new user
@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    user = User(id=None, name=data['name'], email=data['email'])
    user_id = save_user(user)
    return jsonify({'id': user_id}), 201

# Route to get all users
@app.route('/users', methods=['GET'])
def get_all_users():
    users = get_all_users_from_db()
    user_dicts = [user.to_dict() for user in users]
    return jsonify({'users': user_dicts})

# Route to create a new topic for a user
@app.route('/users/<user_id>/topics', methods=['POST'])
def create_topic(user_id):
    data = request.get_json()
    user = get_user(user_id)
    topic = Topic(id=None, title=data['title'])
    user.topics.append(topic)
    save_user(user)
    return jsonify({'id': topic.id}), 201

# Route to get all topics for a user
@app.route('/users/<user_id>/topics', methods=['GET'])
def get_user_topics(user_id):
    user = get_user(user_id)
    topic_dicts = [topic.to_dict() for topic in user.topics]
    return jsonify({'topics': topic_dicts})

# Route to create a document for a topic
@app.route('/topics/<topic_id>/documents', methods=['POST'])
def create_document(topic_id):
    data = request.get_json()
    topic = get_topic(topic_id)
    document = Document(id=None, title=data['title'], url=data['url'])
    topic.documents.append(document)
    save_topic(topic)
    return jsonify({'id': document.id}), 201

# Route to create a video for a topic
@app.route('/topics/<topic_id>/videos', methods=['POST'])
def create_video(topic_id):
    data = request.get_json()
    topic = get_topic(topic_id)
    video = Video(id=None, title=data['title'], url=data['url'], summary=data['summary'])
    topic.videos.append(video)
    save_topic(topic)
    return jsonify({'id': video.id}), 201

# ... Other routes to update, delete, or retrieve individual documents, videos, and users.

if __name__ == '__main__':
    app.run(debug=True)