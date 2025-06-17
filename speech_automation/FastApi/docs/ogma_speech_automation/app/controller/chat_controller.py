# @Author : Rahul Sinha
# @Date : 22 October 2024

from fastapi import WebSocket
from app.services.speech_to_text import openai_speech_to_text
from app.services.grammar_correction import correct_grammar
from app.services.text_to_speech import openai_text_to_speech
from app.services.websocket_service import WebSocketManager

websocket_manager = WebSocketManager()

async def process_audio(websocket: WebSocket):
    try:
        print("Client connected")

        # Step 1: Receive audio file from client
        audio_data = await websocket.receive_bytes()
        print("Audio file received")

        # Save the audio data to a file
        audio_file = "uploaded_audio.wav"
        with open(audio_file, "wb") as buffer:
            buffer.write(audio_data)
        print("Audio saved to file")

        # Inform the client that the audio is being processed
        await websocket.send_text("Processing audio... Please wait")

        # Step 2: Convert speech to text
        transcribed_text = await openai_speech_to_text(audio_file)
        await websocket.send_text(f"Transcribed Text: {transcribed_text}")

        # Step 3: Correct grammar
        corrected_text = await correct_grammar(transcribed_text)
        await websocket.send_text(f"Corrected Text: {corrected_text}")

        # Step 4: Convert corrected text to speech
        speech_audio_path = await openai_text_to_speech(corrected_text)

        # Step 5: Send the final audio file to the client
        with open(speech_audio_path, "rb") as audio:
            processed_audio_data = audio.read()
            await websocket.send_bytes(processed_audio_data)

        print("Audio processing completed and sent to client")

    except Exception as e:
        print(f"Error occurred: {e}")
        await websocket.close(code=1011, reason="Internal server error")
