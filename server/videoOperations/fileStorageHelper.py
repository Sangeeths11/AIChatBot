import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from google.cloud import storage
import api.appconfig as config
from urllib.parse import urlparse
import os
import pathlib
import mimetypes

db = firestore.client()


def uploadTranscriptFile(localTranscriptPath):
    """
    Uploads a transcript file to a Google Cloud Storage bucket.

    Args:
      localTranscriptPath (str): The local path of the transcript file.

    Returns:
      str: The public URL of the uploaded transcript file.

    Examples:
      >>> uploadTranscriptFile('/path/to/transcript.txt')
      'https://storage.googleapis.com/bucket/transcripts/transcript.txt'
    """
    if localTranscriptPath is not None:
        bucket = getBucket()
        fileName = os.path.basename(urlparse(localTranscriptPath).path)
        transcriptBlob = bucket.blob(config.BUCKET_TRANSCRIPTS_PATH + fileName)
        return uploadPublicFile(transcriptBlob, localTranscriptPath, fromFilename=True)
            
def uploadDocumentFile(file):
    """
    Uploads a document file to a Google Cloud Storage bucket.

    Args:
      file (file): The file to upload.

    Returns:
      str: The public URL of the uploaded document file.

    Examples:
      >>> uploadDocumentFile(open('/path/to/document.pdf', 'rb'))
      'https://storage.googleapis.com/bucket/documents/document.pdf'
    """
    if file is not None:
        bucket = getBucket()
        documentBlob = bucket.blob(config.BUCKET_DOCUMENTS_PATH + file.filename)
        return uploadPublicFile(documentBlob, file)

def uploadSubjectImage(file):
    """
    Uploads a subject image to a Google Cloud Storage bucket.

    Args:
      file (file): The file to upload.

    Returns:
      str: The public URL of the uploaded subject image.

    Examples:
      >>> uploadSubjectImage(open('/path/to/subject_image.jpg', 'rb'))
      'https://storage.googleapis.com/bucket/subject_images/subject_image.jpg'
    """
    if file is not None:
        bucket = getBucket()
        subjectImgBlob = bucket.blob(config.BUCKET_SUBJECT_IMAGES_PATH + file.filename)
        return uploadPublicFile(subjectImgBlob, file)
    
def uploadUserImage(file):
    """
    Uploads a user image to a Google Cloud Storage bucket.

    Args:
      file (file): The file to upload.

    Returns:
      str: The public URL of the uploaded user image.

    Examples:
      >>> uploadUserImage(open('/path/to/user_image.jpg', 'rb'))
      'https://storage.googleapis.com/bucket/user_images/user_image.jpg'
    """
    if file is not None:
        bucket = getBucket()
        userImgBlob = bucket.blob(config.BUCKET_USER_IMAGES_PATH + file.filename)
        return uploadPublicFile(userImgBlob, file)

def getMimetype(filePath):
    """
    Gets the mimetype of a file.

    Args:
      filePath (str): The path of the file.

    Returns:
      str: The mimetype of the file.

    Examples:
      >>> getMimetype('/path/to/file.txt')
      'text/plain'
    """
    mimeType, _ = mimetypes.guess_type(filePath)
    if mimeType is None:
        return "application/octet-stream"
    return mimeType
    
def getBucket():
    """
    Gets a Google Cloud Storage bucket.

    Returns:
      google.cloud.storage.bucket.Bucket: The Google Cloud Storage bucket.
    """
    storageClient = storage.Client.from_service_account_json(config.CREDENTIALS_PATH)
    return storageClient.get_bucket(config.BUCKET_NAME)

def uploadPublicFile(blob, file, fromFilename = False):
    """
    Uploads a file to a Google Cloud Storage bucket and makes it public.

    Args:
      blob (google.cloud.storage.blob.Blob): The Google Cloud Storage blob.
      file (file): The file to upload.
      fromFilename (bool): Whether the file is from a filename or not.

    Returns:
      str: The public URL of the uploaded file.

    Examples:
      >>> uploadPublicFile(blob, open('/path/to/file.txt', 'rb'))
      'https://storage.googleapis.com/bucket/file.txt'
    """
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