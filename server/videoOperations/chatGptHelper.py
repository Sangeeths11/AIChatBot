import openai
import os
import whisper
from pytube import YouTube
import pprint

import json

import time


from videoOperations.fileStorageHelper import *


os.environ["OPENAI_API_KEY"] = "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"
openai.api_key = os.getenv("OPENAI_API_KEY")

folderName = "youtubeAudio"
if not os.path.exists(folderName):
    os.makedirs(folderName)


def getCompletion(prompt, model="gpt-3.5-turbo", temperature=0.0):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model, messages=messages, temperature=temperature,
    )
    return response.choices[0].message["content"]


# pip install -U openai-whisper
def getTranscript(url, transcriptionName):
    
    transcriptionPath = getVideoData(url, transcriptionName)
    url = uploadTranscriptFile(transcriptionPath,transcriptionName)
    return url
    
    # options = whisper.DecodingOptions()
    # whisperModel = whisper.load_model("tiny.en")
    # result = whisperModel.transcribe(audioFilePath) 
    # text = result.get("text", None)
    
    # with open("transcript.txt", "w") as file:
    #     # save to db
    #     file.write(text)
    
def extractText(data):
    text = ""
    if isinstance(data, list):
        for item in data:
            text += extractText(item)
    elif isinstance(data, dict):
        for key, value in data.items():
            if key == "utf8":
                text += value + " "
            text += extractText(value)
    return text
    
def getVideoData(url, transcriptionName):
    yt = YouTube(url)
    
    # # Download audio
    # audioStreamItag = yt.streams.filter(only_audio=True).order_by(attribute_name="abr").first().itag
    # audioFilePath = yt.streams.get_by_itag(audioStreamItag).download(max_retries=5, filename=transcriptionName,  output_path="youtubeAudio")
    
    # Do it with the captions first
    
    # if the captions dont work, generate the transcript with whisper
     
    
    # Get the available caption tracks (subtitles)
    caption = yt.captions["a.en"]
    text = extractText(caption.json_captions)

    text = text.strip()

    filePath = f"transcripts/{transcriptionName}.txt"
    with open(filePath, "w", encoding="utf-8") as file:
        file.write(text)
        
    return filePath
    
    # post-process with chat-gpt
    
    
    
    # Then write file to cloud storage
    
    
    # return audioFilePath
