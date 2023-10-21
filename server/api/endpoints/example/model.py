# model.py abstracts the database operations
# model.py deals with data management and database interactions
# defines how data is stored structurde and managed in the application
# define data models and business logic
# Classes that represent the structure and behaviour of the applications data entities

# model.py

import firebase_admin
from firebase_admin import credentials, firestore





# User Model
class User:
    def __init__(self, id, name, email):
        self.id = id
        self.name = name
        self.email = email
        self.topics = []

    def to_dict(self):
        return {
            'name': self.name,
            'email': self.email,
            'topics': self.topics
        }
        
    # Function to get all users from the database
    @classmethod
    def get_all_users_from_db(cls):
        users = []

        # Retrieve user data from the database (Firestore in this case)
        # You should implement the code to fetch user data from your database here.
        # It would typically involve querying your database using Firebase Admin SDK.

        return users

# Topic Model
class Topic:
    def __init__(self, id, title):
        self.id = id
        self.title = title
        self.documents = []
        self.videos = []

    def to_dict(self):
        return {
            'title': self.title,
            'documents': self.documents,
            'videos': self.videos
        }

# Document Model
class Document:
    def __init__(self, id, title, url):
        self.id = id
        self.title = title
        self.url = url

    def to_dict(self):
        return {
            'title': self.title,
            'url': self.url
        }

# Video Model
class Video:
    def __init__(self, id, title, url, summary):
        self.id = id
        self.title = title
        self.url = url
        self.summary = summary

    def to_dict(self):
        return {
            'title': self.title,
            'url': self.url,
            'summary': self.summary
        }