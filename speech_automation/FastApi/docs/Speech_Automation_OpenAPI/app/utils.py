import os
from google.generativeai import GenerativeModel, configure as genai_config
from dotenv import load_dotenv
from pathlib import Path
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()

# Fetch the API keys from environment variables
openai_api_key = os.getenv("OPENAI_API_KEY")
google_api_key = os.getenv("GOOGLE_API_KEY")

# Initialize the OpenAI client
client = OpenAI(api_key=openai_api_key)

# Function to use OpenAI Whisper API for speech-to-text
def openai_speech_to_text(audio_file):
    """
    Transcribes the audio file using OpenAI's Whisper API and returns the transcription.
    :param audio_file: Path to the audio file.
    :return: Transcribed text.
    """
    transcription = client.audio.transcriptions.create(
        model="whisper-1",
        file=open(audio_file, "rb")
    )

    return transcription.text  # Access the 'text' attribute directly


# Function to use Google Gemini API for grammar correction
def correct_grammar(api_key, text):
    """
    Corrects the grammar of the provided text using the Google Gemini API.
    :param api_key: Google Gemini API key.
    :param text: Text to be corrected.
    :return: Corrected text.
    """
    genai_config(api_key=api_key)
    model = GenerativeModel("models/gemini-1.0-pro-latest")

    prompt = '''
    You are a highly knowledgeable language teacher with in-depth expertise in multiple languages. Your role is to correct grammar and ensure fluent, accurate language.
    Correct the following sentence:
    '''
    
    response = model.generate_content(prompt + text)
    return response.text


# Function to use OpenAI for text-to-speech
def openai_text_to_speech(text):
    """
    Converts the provided text to speech using OpenAI's TTS API and streams the audio to a file.
    :param text: Text to be converted into speech.
    :return: Path to the generated audio file.
    """
    speech_file_path = Path(__file__).parent / "speech.mp3"  # Set the output path

    # Generate speech audio from the given text
    response = client.audio.speech.create(
        model="tts-1",
        input=text,
        voice="alloy"
    )

    # Stream the audio to a file
    response.stream_to_file(speech_file_path)

    return speech_file_path