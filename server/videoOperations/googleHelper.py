import openai
import os
from googleapiclient.discovery import build
from textblob import TextBlob
import json
#import appconfig as config
from pytube import YouTube
from dotenv import load_dotenv
import api.appconfig as config
load_dotenv()
#os.environ["GOOGLE_API_KEY"] = config.GOOGLE_API_KEY


from google.oauth2 import service_account

# Load the credentials from the JSON file
credentials = service_account.Credentials.from_service_account_file(config.CREDENTIALS_PATH, scopes=['https://www.googleapis.com/auth/youtube.force-ssl'])


#youtube = build("youtube", "v3", developerKey=os.getenv("GOOGLE_API_KEY"))
youtube = build("youtube", "v3", credentials=credentials)


def youtubeSearch(query, count=2):
    response = youtube.search().list(
        q=query,
        type="video",
        part="id,snippet",  
        maxResults=count
    ).execute()
    
    results = []
    for result in response.get("items", []):
        if result["id"]["kind"] == "youtube#video":
            videoId = result["id"]["videoId"]
            videoTitle = result["snippet"]["title"]
            
            url = f"https://www.youtube.com/watch?v={videoId}"
            

            sentimentScore = getSentimentOfVideo(videoId)
            if sentimentScore:
                results.append({"name": videoTitle, "watchUrl": url, "sentimentScore": sentimentScore})
            else:
                continue
    return results    
    
    

def getSentimentOfVideo(videoId, commentCount = 12):
    commentList = getCommentsOfVideo(videoId, commentCount)
    if commentList:
        return getSentimentOfComments(commentList)
    else:
        return None
    

def getCommentsOfVideo(videoId, commentCount):
    try:
        comments = youtube.commentThreads().list(
            part="snippet",
            videoId=videoId,
            textFormat="plainText",
        ).execute()
    
        commentList = []
        for comment in comments["items"][:min(commentCount, comments["pageInfo"]["totalResults"], comments["pageInfo"]["resultsPerPage"])]:
            commentText = comment["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
            commentList.append(commentText)
            
        return commentList
    except:
        print(f"Error while retriving comments of video with videoId: {videoId}, video excluded.")   
        return None

    
def getSentimentOfComments(commentList):
    positiveCount = 0
    negativeCount = 0

    for commentText in commentList:
        analysis = TextBlob(commentText)
        sentimentScore = analysis.sentiment.polarity

        if sentimentScore > 0:
            positiveCount += 1
        elif sentimentScore < 0:
            negativeCount += 1

    return positiveCount - negativeCount


def getEmbedUrl(video):
    url = video.get("watchUrl", "")
    yt = YouTube(url)
    return yt.embed_url
    