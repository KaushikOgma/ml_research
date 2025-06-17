import sounddevice as sd
import soundfile as sf
import requests
import websockets
import asyncio
from playsound import playsound

# Function to record audio from the microphone
def record_audio(duration=5, fs=16000, filename="microphone_input.wav"):
    print("Recording audio...")
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
    sd.wait()  # Wait until the recording is finished
    sf.write(filename, audio, fs)  # Save the audio file
    print(f"Audio recorded and saved to {filename}")
    return filename

# Function to handle WebSocket connection and process audio
async def send_audio_to_websocket(audio_file):
    uri = "ws://127.0.0.1:8000"  # Replace with your server WebSocket URL
    try:
        async with websockets.connect(uri, ping_interval=None) as websocket:
            print(f"Connected to WebSocket at {uri}")

            # Step 1: Send audio file to server
            with open(audio_file, "rb") as audio:
                audio_data = audio.read()
                await websocket.send(audio_data)
                print("Audio file sent to server")

            # Step 2: Receive messages from the server (transcribed text, corrected text, and audio)
            while True:
                message = await websocket.recv()

                # Handle text messages (transcribed text, corrected text)
                if isinstance(message, str):
                    if "Transcribed Text" in message:
                        print(message)  # Display the transcribed text
                    elif "Corrected Text" in message:
                        print(message)  # Display the corrected text
                    elif "Text-to-speech conversion done" in message:
                        print("Text-to-speech processing complete. Audio will play soon.")
                else:
                    # Handle audio data
                    with open("output_audio.wav", "wb") as f:
                        f.write(message)
                    print("Processed audio received and saved as output_audio.wav")

                    # Play the audio file
                    playsound("output_audio.wav")
                    print("Playing corrected speech audio")
                    break

    except Exception as e:
        print(f"Connection closed with error: {e}")

if __name__ == "__main__":
    # Record audio from the microphone
    recorded_audio_file = record_audio(duration=5)

    # Send the recorded audio to the WebSocket server
    asyncio.run(send_audio_to_websocket(recorded_audio_file))
