import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from google.cloud import storage
import appconfig as config
from urllib.parse import urlparse
import os
import pathlib
import mimetypes

db = firestore.client()


def uploadTranscriptFile(localTranscriptPath):
    if localTranscriptPath is not None:
        bucket = getBucket()
        fileName = os.path.basename(urlparse(localTranscriptPath).path)
        transcriptBlob = bucket.blob(config.BUCKET_TRANSCRIPTS_PATH + fileName)
        return uploadPublicFile(transcriptBlob, localTranscriptPath)
            
def uploadDocumentFile(file):
    if file is not None:
        bucket = getBucket()
        documentBlob = bucket.blob(config.BUCKET_DOCUMENTS_PATH + file.filename)
        return uploadPublicFile(documentBlob, file)

def uploadSubjectImage(file):
    if file is not None:
        bucket = getBucket()
        subjectImgBlob = bucket.blob(config.BUCKET_SUBJECT_IMAGES_PATH + file.filename)
        return uploadPublicFile(subjectImgBlob, file)
    
def uploadUserImage(file):
    if file is not None:
        bucket = getBucket()
        userImgBlob = bucket.blob(config.BUCKET_USER_IMAGES_PATH + file.filename)
        return uploadPublicFile(userImgBlob, file)

def getMimetype(filePath):
    mimeType, _ = mimetypes.guess_type(filePath)
    if mimeType is None:
        return "application/octet-stream"
    return mimeType
    
def getBucket():
    storageClient = storage.Client.from_service_account_json(config.CREDENTIALS_PATH)
    return storageClient.get_bucket(config.BUCKET_NAME)

def uploadPublicFile(blob, file, fromFilename = False):
        if fromFilename:
            blob.content_type = getMimetype(file)  
        else:
            blob.content_type = getMimetype(file.filename)  
        if fromFilename == False:
            blob.upload_from_file(file)
        else: 
            blob.upload_from_filename(file)
            try:
                os.remove(file)
                print(f"{file} has been deleted.")
            except Exception as e:
                print(f"An error occurred: {e}")
        
        blob.make_public()
        return blob.public_url


## This does not work yet
# def downloadAllFilesToLocalDirectory(bucketName, localDirectory):
#     storageClient = storage.Client.from_service_account_json(config.CREDENTIALS_PATH)
#     bucket = storageClient.get_bucket(config.BUCKET_NAME)

#     for blob in bucket.list_blobs():
#         destinationBlobPath = f"{localDirectory}/{blob.name}"
#         blob.download_to_filename(destinationBlobPath)
#         print(f"Downloaded {blob.name} to {destinationBlobPath}")