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
    """
    Generates a video workflow for a given subject.

    Args:
      userId (int): The user's ID.
      subjectId (int): The subject's ID.
      subject (str): The subject to generate a video workflow for.

    Returns:
      None

    Side Effects:
      Creates new videos in the database.

    Examples:
      >>> videoWorkflow(1, 2, "math")
    """
    queries = generateSearchQuery(subject, count=3)
    videos = []
    for q in queries:
        videos.extend(getVideos(q))
    outputJson = {"videos": videos}
    bestVideos = selectBestVideos(subject, json.dumps(outputJson, indent=2))

    for v in bestVideos["videos"]:
        v = addEmbedUrl(v)
        videoId = createNewVideo(userId, subjectId, v["name"], v["url"])
        transcriptUrl = transcribeVideo(v["watchUrl"], videoId)
        updateVideo(userId, subjectId, videoId, v["name"], v["url"], transcriptUrl)


def generateSearchQuery(subject="learning", count=3):
    """
    Generates search queries for a given subject.

    Args:
      subject (str): The subject to generate search queries for.
      count (int): The number of search queries to generate.

    Returns:
      list: A list of search queries.

    Examples:
      >>> generateSearchQuery("math", 3)
      ["How to learn math", "Math tutorials", "Math tips"]
    """
    prompt = prompts.getVideoSearchQuery(subject, count)
    response = gpt.getCompletion(prompt)
    data = json.loads(response)
    videoQueries = [item["query"] for item in data["queries"]]
    return videoQueries


def getVideos(search_query="How to learn"):
    """
    Gets videos for a given search query.

    Args:
      search_query (str): The search query to use.

    Returns:
      list: A list of videos.

    Examples:
      >>> getVideos("How to learn math")
      [{"name": "Math Tutorials for Beginners", "watchUrl": "https://www.youtube.com/watch?v=12345"}, ...]
    """
    return google.youtubeSearch(search_query, 2)


def addEmbedUrl(video):
    """
    Adds an embed URL to a video.

    Args:
      video (dict): The video to add an embed URL to.

    Returns:
      dict: The video with an embed URL.

    Examples:
      >>> addEmbedUrl({"name": "Math Tutorials for Beginners", "watchUrl": "https://www.youtube.com/watch?v=12345"})
      {"name": "Math Tutorials for Beginners", "watchUrl": "https://www.youtube.com/watch?v=12345", "url": "https://www.youtube.com/embed/12345"}
    """
    embedUrl = google.getEmbedUrl(video)
    video["url"] = embedUrl
    return video


class TextColor:
    """
    Class for setting text color.
    """
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'  # Reset text color to the default


# Select the most fitting / best video
def selectBestVideos(subject, videos):
    """
    Selects the best videos for a given subject.

    Args:
      subject (str): The subject to select videos for.
      videos (str): A stringified JSON object of videos.

    Returns:
      dict: A dictionary of the best videos.

    Examples:
      >>> selectBestVideos("math", '{"videos": [{"name": "Math Tutorials for Beginners", "watchUrl": "https://www.youtube.com/watch?v=12345"}, ...]}')
      {"videos": [{"name": "Math Tutorials for Beginners", "watchUrl": "https://www.youtube.com/watch?v=12345"}, ...]}
    """
    prompt = prompts.getBestVideosPrompt(subject, videos, count=2)
    with open("server/videoOperations/transcripts/bestVideosPrompt.txt", 'w') as file:
        file.write(prompt)
    response = gpt.getCompletion(prompt)
    with open("server/videoOperations/transcripts/bestVideosCompletion.txt", 'w') as file:
        file.write(response)
    print("selectedVideos: \n " + TextColor.BLUE + response + TextColor.RESET)
    bestVideos = json.loads(response)
    return bestVideos


# Transcription name is the name, with which the file is stored in the cloud
def transcribeVideo(url, transcriptionName):
    """
    Transcribes a video.

    Args:
      url (str): The URL of the video to transcribe.
      transcriptionName (str): The name of the transcription.

    Returns:
      str: The URL of the transcription.

    Examples:
      >>> transcribeVideo("https://www.youtube.com/watch?v=12345", "math_tutorials")
      "https://storage.googleapis.com/transcriptions/math_tutorials.txt"
    """
    return gpt.getTranscript(url, transcriptionName)


def summarizeVideo():
    """
    Summarizes a video.

    Args:
      None

    Returns:
      None

    Side Effects:
      None
    """
    pass


def generateQuestionsForVideo():
    """
    Generates questions for a video.

    Args:
      None

    Returns:
      None

    Side Effects:
      None
    """
    pass
