import openai
import os
import whisper
from pytube import YouTube

from videoOperations.fileStorageHelper import uploadTranscriptFile
import appconfig as config
# from pywin.debugger import configui

os.environ["OPENAI_API_KEY"] =  config.OPENAI_KEY
openai.api_key = os.getenv("OPENAI_API_KEY")

folderName = config.YOUTUBE_AUDIO_DOWNLOAD_PATH
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
    url = uploadTranscriptFile(transcriptionPath)
    return url
    

    
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



    # Get the available caption tracks (subtitles)
    print(f"captions: {yt.captions}")
    language = ""
    captions = yt.caption_tracks
    if "en" in captions:
        language = "en"
    elif "a.en" in captions:
        language = "a.en"
    elif "de" in captions:
        language = "de"
    
    if language != "":
        print(f"Language: {language}")
        caption = yt.captions[language]
        text = extractText(caption.json_captions)
        text = text.strip()
    else:
        # If no captions are available, transcribe using whisper
        audioStreamItag = yt.streams.filter(only_audio=True).order_by(attribute_name="abr").first().itag
        audioFilePath = yt.streams.get_by_itag(audioStreamItag).download(max_retries=5, filename=f"{transcriptionName}.txt",  output_path="server/videoOperations/youtubeAudio")
        print(f"Downloaded audio for {yt.title}")
        options = whisper.DecodingOptions()
        whisperModel = whisper.load_model("tiny.en")
        result = whisperModel.transcribe(audioFilePath) 
        text = result.get("text", None)
        print(f"transcribing for {yt.title} successful")

        try:
            os.remove(audioFilePath)
            print(f"{audioFilePath} has been deleted.")
        except FileNotFoundError:
            print(f"{audioFilePath} does not exist.")
        except Exception as e:
            print(f"An error occurred: {e}")

    filePath = f"{config.YOUTUBE_AUDIO_TRANSCRIPS_PATH}{transcriptionName}.txt"
    with open(filePath, "w") as file:
        file.write(text)
        
    return filePath
    