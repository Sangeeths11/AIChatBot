import openai
import os
from googleapiclient.discovery import build
from textblob import TextBlob
import json


os.environ["GOOGLE_API_KEY"] = "AIzaSyBx3979KBRUd8ZnAlofo4HP-Kf5whLe8IQ"
youtube = build("youtube", "v3", developerKey=os.getenv("GOOGLE_API_KEY"))


def youtubeSearch(query, count=3):
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
            videoLink = f"https://www.youtube.com/watch?v={videoId}"
            sentimentScore = getSentimentOfVideo(videoId)
            if sentimentScore:
                results.append({"title": videoTitle, "url": videoLink, "sentimentScore": sentimentScore})
            else:
                continue
    return results    
    
    

def getSentimentOfVideo(videoId, commentCount = 20):
    commentList = getCommentsOfVideo(videoId, commentCount)
    if commentList:
        return getSentimentOfComments(commentList)
    else:
        return None
    

def getCommentsOfVideo(videoId, commentCount):
    try:
        comments = youtube.commentThreads().list(
            part='snippet',
            videoId=videoId,
            textFormat='plainText',
        ).execute()
        

        commentList = []
        for comment in comments['items'][:min(commentCount, comments["pageInfo"]["totalResults"], comments["pageInfo"]["resultsPerPage"])]:
            commentText = comment['snippet']['topLevelComment']['snippet']['textDisplay']
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