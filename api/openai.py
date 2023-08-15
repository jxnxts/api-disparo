
from dotenv import load_dotenv
import os
import openai

load_dotenv()

APIKEY = os.getenv('OPENAI_APIKEY')
openai.api_key = APIKEY


def transcribe_audio(audio):
    f = open(audio)
    transcription = openai.Audio.transcribe("whisper-1", f)
    return transcription['text']