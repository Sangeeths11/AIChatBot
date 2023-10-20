import openai
import os
import whisper
from pytube import YouTube
import pprint

import json

import time


os.environ["OPENAI_API_KEY"] = "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"
openai.api_key = os.getenv("OPENAI_API_KEY")


def getCompletion(prompt, model="gpt-3.5-turbo", temperature=0.0):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model, messages=messages, temperature=temperature,
    )
    return response.choices[0].message["content"]


# pip install -U openai-whisper
def getTranscript(url):
    start_time = time.time()

    #getAudio("https://youtu.be/HMOI_lkzW08")
    print(f"Time for getAudio:  {time.time() - start_time}")
    
    
    testpath = "youtubeAudio/audioTest.mp3"
    options = whisper.DecodingOptions()
    
    print("Start model load")
    whisper_model = whisper.load_model("tiny.en")
    print("end model load")
    start_time = time.time()
    print("start transcribe")
    result = whisper_model.transcribe(testpath)
    print("end transcribe")
    print(f"Time for getAudio:  {time.time() - start_time}")
    text = result.get('text', None)
    print(text)
    
    with open('transcript.txt', 'w') as file:
        file.write(text)
    
def extract_text(data):
    text = ""
    if isinstance(data, list):
        for item in data:
            text += extract_text(item)
    elif isinstance(data, dict):
        for key, value in data.items():
            if key == 'utf8':
                text += value + ' '
            text += extract_text(value)
    return text


    
def getAudio(url):
    yt = YouTube(url)
    audioStreamItag = yt.streams.filter(only_audio=True).order_by(attribute_name="abr").first().itag
    audio = yt.streams.get_by_itag(audioStreamItag).download(max_retries=5, filename="audioTest.mp3", output_path="youtubeAudio")
    
    # Get the available caption tracks (subtitles)
    caption = yt.captions["a.en"]
    text = extract_text(caption.json_captions)

    text = text.strip()
    # Download the captions to a file
    print(text)


    # If you want to save the captions to a file
    with open('captions.txt', 'w', encoding='utf-8') as file:
        file.write(text)
    
    return audio
