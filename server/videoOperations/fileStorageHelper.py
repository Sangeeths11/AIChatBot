import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from google.cloud import storage
import api.appconfig as config
from urllib.parse import urlparse
import os

db = firestore.client()


def uploadTranscriptFile(localTranscriptPath):
    if localTranscriptPath is not None:

        storageClient = storage.Client.from_service_account_json(config.CREDENTIALS_PATH)
        bucket = storageClient.get_bucket(config.BUCKET_NAME)
        parsedUrl = urlparse(localTranscriptPath)
        fileName = os.path.basename(parsedUrl.path)
        transcriptBlob = bucket.blob(f"transcripts/{fileName}")
        transcriptBlob.upload_from_filename(localTranscriptPath)
        transcriptBlob.content_type = 'text/html'  # For example, if it's an HTML file
        transcriptBlob.make_public()
        
        transcriptUrl = transcriptBlob.public_url
        
    # Delete local file after uploading        
        try:
            os.remove(localTranscriptPath)
            print(f"{localTranscriptPath} has been deleted.")
        except Exception as e:
            print(f"An error occurred: {e}")
            
        return transcriptUrl
    
    

def uploadDocumentFile(file):
    if file is not None:
        storageClient = storage.Client.from_service_account_json(config.CREDENTIALS_PATH)
        bucket = storageClient.get_bucket(config.BUCKET_NAME)
        documentBlob = bucket.blob(f"documents/{file.filename}")
        documentBlob.content_type = "application/pdf"  # For example, if it's a PDF file
        documentBlob.upload_from_file(file)

        documentBlob.make_public()

        documentUrl = documentBlob.public_url
        return documentUrl