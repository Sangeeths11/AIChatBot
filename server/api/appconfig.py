from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
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
GOOGLE_API_KEY = "AIzaSyDfEie7hdPPft-0PeTxBHEkzT16l_8rnKA"

# Firebase Firestorage
CREDENTIALS_PATH = "server/credsFirestore.json"

# Celery Config
CELERY_BROKER_URL = "redis://localhost:6379/0"
CELERY_RESULT_BACKEND = "redis://localhost:6379/0"
