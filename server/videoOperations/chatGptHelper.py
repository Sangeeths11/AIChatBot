import openai
import os
import whisper
from pytube import YouTube

from videoOperations.fileStorageHelper import uploadTranscriptFile
import api.appconfig as config

openai.api_key = os.getenv("OPENAI_API_KEY")

folderName = config.YOUTUBE_AUDIO_DOWNLOAD_PATH
if not os.path.exists(folderName):
    os.makedirs(folderName)


def getCompletion(prompt, model="gpt-4", temperature=0.0):
    """
    Generates a completion for a given prompt.

    Args:
      prompt (str): The prompt to generate a completion for.
      model (str, optional): The model to use for generating the completion. Defaults to "gpt-4".
      temperature (float, optional): The temperature to use for generating the completion. Defaults to 0.0.

    Returns:
      str: The generated completion.

    Examples:
      >>> getCompletion("Hello, my name is")
      "Nice to meet you, my name is"
    """
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model, messages=messages, temperature=temperature,
    )
    return response.choices[0].message["content"]


# pip install -U openai-whisper
def getTranscript(url, transcriptionName):
    """
    Generates a transcript for a given YouTube video URL.

    Args:
      url (str): The URL of the YouTube video.
      transcriptionName (str): The name of the transcript file.

    Returns:
      str: The URL of the transcript file.

    Examples:
      >>> getTranscript("https://www.youtube.com/watch?v=dQw4w9WgXcQ", "rickroll")
      "https://example.com/transcripts/rickroll.txt"
    """
    
    transcriptionPath = getVideoData(url, transcriptionName)
    url = uploadTranscriptFile(transcriptionPath)
    return url
    

    
def extractText(data):
    """
    Extracts text from a given data structure.

    Args:
      data (list or dict): The data structure to extract text from.

    Returns:
      str: The extracted text.

    Examples:
      >>> extractText([{"utf8": "Hello"}, {"utf8": "World"}])
      "Hello World"
    """
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
    
import time

def getVideoData(url, transcriptionName):
    """
    Generates a transcript for a given YouTube video URL.

    Args:
      url (str): The URL of the YouTube video.
      transcriptionName (str): The name of the transcript file.

    Returns:
      str: The file path of the transcript file.

    Examples:
      >>> getVideoData("https://www.youtube.com/watch?v=dQw4w9WgXcQ", "rickroll")
      "server/videoOperations/youtubeAudio/rickroll.txt"
    """
    yt = YouTube(url)  
    text = ""


    # print(yt.caption_tracks())
    
    # for ln in ["en", "a.en", "de"]:
    #     cpt = yt.caption_tracks.get(ln, None)
    #     if cpt is not None:
    #         print(cpt)
    #         text = extractText(cpt.json_captions)
    #         text = text.strip()
    #         break
        
        
    if len(text) == 0:
        # If no captions are available, transcribe using whisper
        audioStreamItag = yt.streams.filter(only_audio=True).order_by(attribute_name="abr").first().itag
        audioFilePath = yt.streams.get_by_itag(audioStreamItag).download(max_retries=5, filename=f"{transcriptionName}.txt",  output_path="server/videoOperations/youtubeAudio")
        print(f"Downloaded audio for {yt.title}")
        
        startTime = time.time()

        print(f"started loading model and transcribing")
        options = whisper.DecodingOptions()
        whisperModel = whisper.load_model("tiny.en")
        result = whisperModel.transcribe(audioFilePath) 
        text = result.get("text", None)
        print(f"transcribing for {yt.title} successful")
        print(f"Transcribing took: {time.time()-startTime}")

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
    