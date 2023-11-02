import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from google.cloud import storage
import appconfig as config
from urllib.parse import urlparse
import os

db = firestore.client()


def uploadTranscriptFile(localTranscriptPath):
    if localTranscriptPath is not None:

        storageClient = storage.Client.from_service_account_json(config.CREDENTIALS_PATH)
        bucket = storageClient.get_bucket(config.BUCKET_NAME)
        parsedUrl = urlparse(localTranscriptPath)
        fileName = os.path.basename(parsedUrl.path)
        transcriptBlob = bucket.blob(config.BUCKET_TRANSCRIPTS_PATH + fileName)
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
        documentBlob = bucket.blob(config.BUCKET_DOCUMENTS_PATH + file.filename)
        documentBlob.content_type = "application/pdf"  
        documentBlob.upload_from_file(file)

        documentBlob.make_public()

        documentUrl = documentBlob.public_url
        return documentUrl
    
    
def downloadAllFilesToLocalDirectory(bucketName, localDirectory):
    storageClient = storage.Client.from_service_account_json(config.CREDENTIALS_PATH)
    bucket = storageClient.get_bucket(config.BUCKET_NAME)

    for blob in bucket.list_blobs():
        destinationBlobPath = f"{localDirectory}/{blob.name}"
        blob.download_to_filename(destinationBlobPath)
        print(f"Downloaded {blob.name} to {destinationBlobPath}")

if __name__ == '__main__':
    bucketName = 'YOUR_BUCKET_NAME'
    localDirectory = 'LOCAL_DIRECTORY'
    downloadAllFilesToLocalDirectory(bucketName, localDirectory)