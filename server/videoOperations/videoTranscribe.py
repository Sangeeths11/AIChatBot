import os
import json
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import json
import pandas as pd


import chatGptHelper as gpt
import googleHelper as google

import prompts


def main():
    gpt.getTranscript("https://www.youtube.com/watch?v=HMOI_lkzW08")
    
    #topic = "dimensionality reduction"
    #videoWorkflow(topic)

    

def videoWorkflow(topic):
    queries = generateSearchQuery(topic, count=3)
    videos = []
    for q in queries:
        videos.extend(getVideos(q))
            
    output_json = {"videos": videos}
    #print(json.dumps(output_json, indent=2))
    
    bestVideos = selectBestVideos(json.dumps(output_json, indent=2))
    print(bestVideos)

    [transcribeVideo(v["url"]) for v in bestVideos["videos"]]
    
    
def generateSearchQuery(topic = "learning", count = 3):
    prompt = prompts.getVideoSearchQuery(topic, count)
    response = gpt.getCompletion(prompt)
    data = json.loads(response)
    videoQueries = [item["query"] for item in data["queries"]]
    return videoQueries    
    
    
def getVideos(search_query = "How to learn"):
    return google.youtubeSearch(search_query, 3)



# Select the most fitting / best video
def selectBestVideos(videos):
    prompt = prompts.getBestVideosPrompt(videos, 3)
    response = gpt.getCompletion(prompt)
    bestVideos = json.loads(response)
    return bestVideos


def transcribeVideo(url):
    return gpt.getTranscript(url)


def summarizeVideo():
    pass


def generateQuestionsForVideo():
    pass


if __name__ == "__main__":
    main()