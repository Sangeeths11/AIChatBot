import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from google.cloud import storage
import api.appconfig as config
import os

db = firestore.client()


def uploadTranscriptFile(transcriptionPath):
    if transcriptionPath is not None:

        storageClient = storage.Client.from_service_account_json(config.CREDENTIALS_PATH)
        bucket = storageClient.get_bucket(config.BUCKET_NAME)

        transcriptBlob = bucket.blob(transcriptionPath)
        transcriptBlob.upload_from_filename(transcriptionPath)
        transcriptUrl = transcriptBlob.public_url
        
    # Delete local file after uploading        
        try:
            os.remove(transcriptionPath)
            print(f"{transcriptionPath} has been deleted.")
        except Exception as e:
            print(f"An error occurred: {e}")
            
        return transcriptUrl
    
    
    
def uploadDocumentFile(documentPath):
    if documentPath is not None:

        storageClient = storage.Client.from_service_account_json(config.CREDENTIALS_PATH)
        bucket = storageClient.get_bucket(config.BUCKET_NAME)

        documentBlob = bucket.blob(documentPath)
        documentBlob.upload_from_filename(documentPath)
        documentUrl = documentBlob.public_url
        return documentUrl