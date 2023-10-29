import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from google.cloud import storage
import api.appconfig as config


db = firestore.client()


# cloud storage
# store documents there, retrive public url
storage_client = storage.Client.from_service_account_json(config.CREDENTIALS_PATH)
bucket = storage_client.get_bucket(config.BUCKET_NAME)

document_blob = bucket.blob("documents/document_id.pdf")
document_blob.upload_from_filename("server/api/modulbeschreibung.pdf")
document_url = document_blob.public_url


# Firestore
# Store other data in firestore

# Create a new user
update_time, user_ref = db.collection("users").add({
    "firstname": "John",
    "lastname": "Doe",
    "email": "johndoe@example.com",
})

# Create a subject for a user
subject_ref = user_ref.collection("subjects")
updateTime, subjectRef = subject_ref.add({
    "name": "Mathematics",
})

# Store documents and videos in the subject
document_ref = subjectRef.collection("documents")
time, docRef = document_ref.add({
    "url": document_url,
})

video_ref = subjectRef.collection("videos")
time, videoRef = video_ref.add({
    "url": "sample/url",
})


