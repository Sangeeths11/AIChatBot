from firebase_admin import firestore

db = firestore.client()

def getVideoById(userId, subjectId, videoId):
    ref = db.collection("users").document(userId).collection("subjects").document(subjectId).collection("videos").document(videoId)
    data = ref.get()
    if data.exists:
        return data.to_dict()
    else:
        return None

def createNewVideo(userId, subjectId, name, url, transcriptUrl=""):
        time, ref = db.collection("users").document(userId).collection("subjects").document(subjectId).collection("videos").add({
            "name": name,
            "url": url,
            "transcriptUrl": transcriptUrl
            })        
        return ref.id

def updateVideo(userId, subjectId, videoId, name, url, transcriptUrl):
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
    ref = db.collection("users").document(userId).collection("subjects").document(subjectId).collection("videos").document(videoId)
    ref.delete()
    return True  

def getAllVideos(userId, subjectId):
    ref =  db.collection("users").document(userId).collection("subjects").document(subjectId).collection("videos")  
    videos = ref.stream()
    return [docs.to_dict() for docs in videos]
    