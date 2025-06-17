import sounddevice as sd
import soundfile as sf
import websockets
import asyncio
from playsound import playsound
import base64

# Function to record audio from the microphone
def record_audio(duration=5, fs=16000, filename="microphone_input.wav"):
    print("Recording audio...")
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
    sd.wait()  # Wait until the recording is finished
    sf.write(filename, audio, fs)  # Save the audio file
    print(f"Audio recorded and saved to {filename}")
    return filename

# Function to save binary audio data to a text file
def save_audio_to_textfile(audio_data, text_filename="audio_data.txt"):
    # Convert binary data to base64 encoded string
    encoded_data = base64.b64encode(audio_data).decode('utf-8')

    # Write the encoded data to a text file
    with open(text_filename, "w") as text_file:
        text_file.write(encoded_data)
    print(f"Audio binary data saved to {text_filename}")

# Function to load audio binary data from a text file
def load_audio_from_textfile(text_filename="audio_data.txt"):
    # Read the encoded string from the text file
    with open(text_filename, "r") as text_file:
        encoded_data = text_file.read()

    # Decode the base64 string back to binary data
    audio_data = base64.b64decode(encoded_data)
    print(f"Audio binary data loaded from {text_filename}")
    return audio_data

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

            # Save the binary data to a text file
            save_audio_to_textfile(audio_data, text_filename="audio_data.txt")

            # Step 2: Receive messages from the server (transcribed text, corrected text, and audio)
            while True:
                message = await websocket.recv()

                # Handle text messages (transcribed text, corrected text)
                if isinstance(message, str):
                    if "Transcribed Text" in message:
                        print(f"Server: {message}")  # Display the transcribed text
                    elif "Corrected Text" in message:
                        print(f"Server: {message}")  # Display the corrected text
                    elif "Text-to-speech conversion done" in message:
                        print("Text-to-speech processing complete. Audio will play soon.")
                else:
                    # Handle audio data (binary)
                    with open("output_audio.wav", "wb") as f:
                        f.write(message)
                    print("Processed audio received and saved as output_audio.wav")

                    # Save the processed audio binary data to a text file
                    save_audio_to_textfile(message, text_filename="processed_audio_data.txt")

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
