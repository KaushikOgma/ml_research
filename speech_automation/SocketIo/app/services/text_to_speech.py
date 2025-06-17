# app/services/text_to_speech.py
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)

async def openai_text_to_speech(text: str) -> bytes:
    """
    Converts the text to speech using OpenAI's TTS API and returns the audio content as bytes.
    :param text: Text to be converted into speech.
    :return: Audio content in bytes.
    """
    response = client.audio.speech.create(
        model="tts-1",
        input=text,
        voice="alloy"
    )

    audio_bytes = response.read()
    return audio_bytes
