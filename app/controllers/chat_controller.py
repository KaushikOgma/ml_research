# @Author : Rahul Sinha
# @Date : 22 October 2024

import os
import io
import tempfile
import soundfile as sf
from fastapi import WebSocket
from app.services.speech_to_text import openai_speech_to_text
from app.services.grammar_correction import correct_grammar
from app.services.text_to_speech import openai_text_to_speech
from app.services.websocket_service import WebSocketManager
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
AUDIO_SAVE_DIR = os.getenv("AUDIO_SAVE_DIR", "uploads")
CUSTOM_TEMP_DIR = os.getenv("CUSTOM_TEMP_DIR", None) 
SAVE_AUDIO = os.getenv("SAVE_AUDIO", "False").lower() == "true"
websocket_manager = WebSocketManager()

# Ensure the custom temp directory exists if specified
if CUSTOM_TEMP_DIR:
    os.makedirs(CUSTOM_TEMP_DIR, exist_ok=True)

async def process_audio(websocket: WebSocket):
    try:
        print("Client connected for audio processing")
        await websocket.send_text("You can start sending audio data.")

        while True:
            # Step 1: Receive audio file from client
            audio_data = await websocket.receive_bytes()
            print("Audio file received")

            # Inform the client that the audio is being processed
            await websocket.send_text("Processing audio... Please wait")

            # Convert byte data to WAV format and store it in a temporary file within the custom directory
            with io.BytesIO(audio_data) as audio_buffer:
                audio, sample_rate = sf.read(audio_buffer)
                
                # Use the custom temporary directory if set, else use the default system temp directory
                temp_wav_file = tempfile.NamedTemporaryFile(suffix=".wav", dir=CUSTOM_TEMP_DIR)
                sf.write(temp_wav_file.name, audio, sample_rate, format='WAV')
                temp_wav_file.flush()

                # Save uploaded audio if SAVE_AUDIO is enabled
                if SAVE_AUDIO:
                    os.makedirs(AUDIO_SAVE_DIR, exist_ok=True)
                    uploaded_audio_path = os.path.join(AUDIO_SAVE_DIR, "uploaded_audio.wav")
                    with open(uploaded_audio_path, "wb") as f:
                        f.write(audio_data)
                    print(f"Uploaded audio saved to: {uploaded_audio_path}")
            
            # Step 2: Convert speech to text
            transcribed_text = await openai_speech_to_text(temp_wav_file.name)
            await websocket.send_text(f"Transcribed Text: {transcribed_text}")

            # Step 3: Correct grammar
            corrected_text = await correct_grammar(transcribed_text)
            await websocket.send_text(f"Corrected Text: {corrected_text}")

            # Step 4: Convert corrected text to speech
            audio_response_data = await openai_text_to_speech(corrected_text)
            
            # Save output audio if SAVE_AUDIO is enabled
            if SAVE_AUDIO:
                os.makedirs(AUDIO_SAVE_DIR, exist_ok=True)
                output_audio_path = os.path.join(AUDIO_SAVE_DIR, "converted_audio.mp3")
                with open(output_audio_path, "wb") as audio_file:
                    audio_file.write(audio_response_data)
                print(f"Converted audio saved to: {output_audio_path}")
            
            # Send final audio to client
            await websocket.send_bytes(audio_response_data)
            print("Audio processing completed and sent to client")

    except Exception as e:
        print(f"Error occurred: {e}")
        await websocket.close(code=1011, reason="Internal server error")

async def process_text(websocket: WebSocket):
    try:
        print("Client connected for text processing")
        await websocket.send_text("You can start sending text data.")

        while True:
            # Step 1: Receive text input from client
            text_data = await websocket.receive_text()
            print("Text received for processing")

            # Step 2: Perform grammar correction
            corrected_text = await correct_grammar(text_data)
            await websocket.send_text(f"Corrected Text: {corrected_text}")

            print("Text processing completed and feedback sent to client")

    except Exception as e:
        print(f"Error occurred during text processing: {e}")
        await websocket.close(code=1011, reason="Internal server error")
