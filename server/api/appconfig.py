import os
import base64
import json
from dotenv import load_dotenv, find_dotenv
import atexit

# Load environment variables
load_dotenv(find_dotenv())

def cleanup_credentials_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"Deleted credentials file: {file_path}")

def get_Firebase_credentials():
    # Get the encoded Firestore credentials from the environment variable
    encoded_creds = os.environ.get('FIRESTORE_CREDENTIALS_BASE64')
    if not encoded_creds:
        raise ValueError("The FIRESTORE_CREDENTIALS_BASE64 environment variable is not set.")
    # Decode the credentials from base64
    decoded_creds = base64.b64decode(encoded_creds).decode('utf-8')
    # Parse the JSON credentials
    creds_json = json.loads(decoded_creds)
    # Write the credentials to a file
    credentials_file_path = 'firebase_credentials.json'
    with open(credentials_file_path, 'w') as creds_file:
        json.dump(creds_json, creds_file)
    # Register the cleanup function
    atexit.register(cleanup_credentials_file, file_path='firebase_credentials.json')

get_Firebase_credentials()

CREDENTIALS_PATH = 'firebase_credentials.json'
# File locations
YOUTUBE_AUDIO_DOWNLOAD_PATH = "server/videoOperations/youtubeAudio"
YOUTUBE_AUDIO_TRANSCRIPS_PATH = "server/videoOperations/transcripts/"


# Chatbots
VECTORSTORE_PATH = "/server/chatbots/vectorstore/"


# Google Cloud Storage
BUCKET_NAME = "aitutor-e6db8.appspot.com"
BUCKET_DOCUMENTS_PATH = "documents/"
BUCKET_TRANSCRIPTS_PATH = "transcripts/"
BUCKET_SUBJECT_IMAGES_PATH = "subjects/images"
BUCKET_USER_IMAGES_PATH = "users/images"


# Google Key
# GOOGLE_API_KEY = "AIzaSyDfEie7hdPPft-0PeTxBHEkzT16l_8rnKA"

# Firebase Firestorage
# CREDENTIALS_PATH = "server/credsFirestore.json"

