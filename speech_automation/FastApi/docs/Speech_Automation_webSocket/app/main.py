import asyncio
import websockets
from utils import speech_to_text, correct_grammar, text_to_speech_bark

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

        await websocket.send("Processing audio... Please wait")

        # Step 2: Convert speech to text
        transcribed_text = speech_to_text(audio_file, model_dir="models/")
        await websocket.send(f"Transcribed Text: {transcribed_text}")

        # Step 3: Correct grammar
        api_key = "##########################################" 
        corrected_text = correct_grammar(api_key, transcribed_text)
        await websocket.send(f"Corrected Text: {corrected_text}")

        # Step 4: Convert corrected text to speech
        output_audio_file = "final_output.wav"
        text_to_speech_bark(corrected_text, output_file=output_audio_file)

        # Step 5: Send the final audio file to client
        with open(output_audio_file, "rb") as audio:
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
