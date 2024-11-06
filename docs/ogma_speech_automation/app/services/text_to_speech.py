# @Author : Rahul Sinha
# @Date : 22 October 2024

from pathlib import Path
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

# Fetch API key from environment variables
openai_api_key = os.getenv("OPENAI_API_KEY")

# Initialize the OpenAI client
client = OpenAI(api_key=openai_api_key)

async def openai_text_to_speech(text: str) -> str:
    """
    Converts the text to speech using OpenAI's TTS API.
    :param text: Text to be converted into speech.
    :return: Path to the generated audio file.
    """
    speech_file_path = Path(__file__).parent / "speech.mp3"

    response = client.audio.speech.create(
        model="tts-1",
        input=text,
        voice="alloy"
    )

    # Save the speech to a file
    response.stream_to_file(speech_file_path)
    
    return str(speech_file_path)
