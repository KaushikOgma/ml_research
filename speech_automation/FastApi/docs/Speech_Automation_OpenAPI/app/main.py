import asyncio
import websockets
from utils import openai_speech_to_text, correct_grammar, openai_text_to_speech
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Fetch the API key from environment variables
google_api_key = os.getenv("GOOGLE_API_KEY")

async def process_audio(websocket, path):
    try:
        print("Client connected")

        # Step 1: Receive audio file from client
        audio_data = await websocket.recv()
        print("Audio file received")

        # Save the audio data to a file
        audio_file = "uploaded_audio.wav"
        with open(audio_file, "wb") as buffer:
            buffer.write(audio_data)
        print("Audio saved to file")

        # Inform the client that the audio is being processed
        await websocket.send("Processing audio... Please wait")

        # Step 2: Convert speech to text using openai_speech_to_text from utils.py
        transcribed_text = openai_speech_to_text(audio_file)
        await websocket.send(f"Transcribed Text: {transcribed_text}")

        # Step 3: Correct grammar using correct_grammar from utils.py
        corrected_text = correct_grammar(google_api_key, transcribed_text)
        await websocket.send(f"Corrected Text: {corrected_text}")

        # Step 4: Convert corrected text to speech using openai_text_to_speech from utils.py
        # Assuming openai_text_to_speech returns the binary audio data
        speech_audio_path = openai_text_to_speech(corrected_text)

        # Step 5: Send the final audio file to the client
        with open(speech_audio_path, "rb") as audio:
            processed_audio_data = audio.read()
            await websocket.send(processed_audio_data)

        print("Audio processing completed and sent to client")

    except Exception as e:
        print(f"Error occurred: {e}")
        await websocket.close(code=1011, reason="Internal server error")

async def start_server():
    # Serve WebSocket requests
    async with websockets.serve(process_audio, "0.0.0.0", 8000):
        print("WebSocket server started")
        await asyncio.Future()  # Run server forever

if __name__ == "__main__":
    asyncio.run(start_server())
