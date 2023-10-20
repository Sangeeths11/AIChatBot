import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from google.cloud import storage

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)


db = firestore.client()



# cloud storage
# store documents there, retrive public url
storage_client = storage.Client.from_service_account_json("serviceAccountKey.json")
bucket = storage_client.get_bucket("aitutor-e6db8.appspot.com")

document_blob = bucket.blob("documents/document_id.pdf")
document_blob.upload_from_filename("modulbeschreibung.pdf")
document_url = document_blob.public_url


# Firestore
# Store other data in firestore

# Create a new user
user_ref = db.collection("users").document("user_id")
user_ref.set({
    "firstname": "John",
    "lastname": "Doe",
    "email": "johndoe@example.com",
})

# Create a subject for a user
subject_ref = user_ref.collection("subjects").document("subject_id")
subject_ref.set({
    "name": "Mathematics",
})

# Store documents and videos in the subject
document_ref = subject_ref.collection("documents").document("document_id")
document_ref.set({
    "url": document_url,
})

video_ref = subject_ref.collection("videos").document("video_id")
video_ref.set({
    "url": "sample/url",
})


