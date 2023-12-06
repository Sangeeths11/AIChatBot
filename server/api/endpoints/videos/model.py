from firebase_admin import firestore

db = firestore.client()

def getVideoById(userId, subjectId, videoId):
    """
    Retrieves a video from the Firebase database.

    Args:
      userId (str): The ID of the user.
      subjectId (str): The ID of the subject.
      videoId (str): The ID of the video.

    Returns:
      dict: A dictionary containing the video data.
      None: If the video does not exist.

    Examples:
      >>> getVideoById('user1', 'subject1', 'video1')
      {'name': 'Video 1', 'url': 'www.example.com/video1', 'transcriptUrl': 'www.example.com/video1/transcript'}
    """
    ref = db.collection("users").document(userId).collection("subjects").document(subjectId).collection("videos").document(videoId)
    data = ref.get()
    if data.exists:
        return data.to_dict()
    else:
        return None

def createNewVideo(userId, subjectId, name, url, transcriptUrl=""):
        """
    Creates a new video in the Firebase database.

    Args:
      userId (str): The ID of the user.
      subjectId (str): The ID of the subject.
      name (str): The name of the video.
      url (str): The URL of the video.
      transcriptUrl (str): The URL of the video transcript.

    Returns:
      str: The ID of the newly created video.

    Examples:
      >>> createNewVideo('user1', 'subject1', 'Video 1', 'www.example.com/video1', 'www.example.com/video1/transcript')
      'video1'
    """
        time, ref = db.collection("users").document(userId).collection("subjects").document(subjectId).collection("videos").add({
            "name": name,
            "url": url,
            "transcriptUrl": transcriptUrl,
            })        
        ref.update({"id": ref.id})
        return ref.id

def updateVideo(userId, subjectId, videoId, name, url, transcriptUrl):
    """
    Updates a video in the Firebase database.

    Args:
      userId (str): The ID of the user.
      subjectId (str): The ID of the subject.
      videoId (str): The ID of the video.
      name (str): The name of the video.
      url (str): The URL of the video.
      transcriptUrl (str): The URL of the video transcript.

    Returns:
      bool: True if the video was successfully updated.

    Examples:
      >>> updateVideo('user1', 'subject1', 'video1', 'Video 1', 'www.example.com/video1', 'www.example.com/video1/transcript')
      True
    """
    print(transcriptUrl)
    ref = db.collection("users").document(userId).collection("subjects").document(subjectId).collection("videos").document(videoId)
    data = {
            "name": name,
            "url": url,
            "transcriptUrl": transcriptUrl
            }
    ref.update(data)
    return True

def deleteVideo(userId, subjectId, videoId):
    """
    Deletes a video from the Firebase database.

    Args:
      userId (str): The ID of the user.
      subjectId (str): The ID of the subject.
      videoId (str): The ID of the video.

    Returns:
      bool: True if the video was successfully deleted.

    Examples:
      >>> deleteVideo('user1', 'subject1', 'video1')
      True
    """
    ref = db.collection("users").document(userId).collection("subjects").document(subjectId).collection("videos").document(videoId)
    ref.delete()
    return True  

def getAllVideos(userId, subjectId):
    """
    Retrieves all videos from the Firebase database.

    Args:
      userId (str): The ID of the user.
      subjectId (str): The ID of the subject.

    Returns:
      list: A list of dictionaries containing the video data.

    Examples:
      >>> getAllVideos('user1', 'subject1')
      [{'name': 'Video 1', 'url': 'www.example.com/video1', 'transcriptUrl': 'www.example.com/video1/transcript'}, {'name': 'Video 2', 'url': 'www.example.com/video2', 'transcriptUrl': 'www.example.com/video2/transcript'}]
    """
    ref =  db.collection("users").document(userId).collection("subjects").document(subjectId).collection("videos")  
    videos = ref.stream()
    return [docs.to_dict() for docs in videos]
    