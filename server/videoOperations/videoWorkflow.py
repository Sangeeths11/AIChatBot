import os
import json
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import json
import pandas as pd

import videoOperations.chatGptHelper as gpt
import videoOperations.googleHelper as google
import videoOperations.prompts as prompts
from api.endpoints.videos.model import createNewVideo, updateVideo


def videoWorkflow(userId, subjectId, subject):
    queries = generateSearchQuery(subject, count=3)
    videos = []
    for q in queries:
        videos.extend(getVideos(q))
        
    outputJson = {"videos": videos}
    bestVideos = selectBestVideos(subject, json.dumps(outputJson, indent=2))
    
    for v in bestVideos["videos"]:
        v = addEmbedUrl(v)
        videoId = createNewVideo(userId, subjectId, v["name"],v["url"])
        transcriptUrl = transcribeVideo(v["watchUrl"], videoId)
        updateVideo(userId, subjectId, videoId, v["name"],v["url"], transcriptUrl)
    
def generateSearchQuery(subject = "learning", count = 3):
    prompt = prompts.getVideoSearchQuery(subject, count)
    response = gpt.getCompletion(prompt)
    data = json.loads(response)
    videoQueries = [item["query"] for item in data["queries"]]
    return videoQueries    
    
def getVideos(search_query = "How to learn"):
    return google.youtubeSearch(search_query, 2)

def addEmbedUrl(video):
    embedUrl =  google.getEmbedUrl(video)
    video["url"] = embedUrl
    return video
    
# Select the most fitting / best video
def selectBestVideos(subject, videos):
    prompt = prompts.getBestVideosPrompt(subject, videos, count=1)
    with open("server/videoOperations/transcripts/bestVideosPrompt.txt", 'w') as file:
        file.write(prompt)
    response = gpt.getCompletion(prompt)
    with open("server/videoOperations/transcripts/bestVideosCompletion.txt", 'w') as file:
        file.write(response)
    bestVideos = json.loads(response)
    return bestVideos


# Transcription name is the name, with which the file is stored in the cloud
def transcribeVideo(url, transcriptionName):
    return gpt.getTranscript(url, transcriptionName)


def summarizeVideo():
    pass


def generateQuestionsForVideo():
    pass

