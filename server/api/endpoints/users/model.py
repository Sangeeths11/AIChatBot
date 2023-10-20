import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase
cred = credentials.Certificate('path/to/your/serviceAccountKey.json')
firebase_admin.initialize_app(cred)

# Initialize Firestore
db = firestore.client()

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