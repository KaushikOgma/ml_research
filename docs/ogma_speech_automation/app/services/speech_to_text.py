# @Author : Rahul Sinha
# @Date : 22 October 2024

import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Fetch API key from environment variables
openai_api_key = os.getenv("OPENAI_API_KEY")

# Initialize the OpenAI client
client = OpenAI(api_key=openai_api_key)

async def openai_speech_to_text(audio_file: str) -> str:
    """
    Transcribes the audio file using OpenAI's Whisper API.
    :param audio_file: Path to the audio file.
    :return: Transcribed text.
    """
    transcription = client.audio.transcriptions.create(
        model="whisper-1",
        file=open(audio_file, "rb")
    )
    return transcription.text
