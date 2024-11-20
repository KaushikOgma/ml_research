import socketio
import os
import asyncio
from concurrent.futures import ThreadPoolExecutor

# Initialize Socket.IO client
sio = socketio.Client()

SERVER_URL = "http://127.0.0.1:8000"  # Server address
AUDIO_FILE_PATHS = [f"temp_audio_{i}.wav" for i in range(1, 11)]  # List of paths to the audio files to send
processing_complete = False  # Flag to check if audio processing is complete

# Event Handlers
@sio.event
def connect():
    print("Connected to server")

    # Send sample text data
    sample_text = "Yesterday i gone store buy vagitables."
    print(f"Sending text: {sample_text}")
    sio.emit("chat_text", sample_text)

    # Send audio files concurrently
    asyncio.run(send_audio_files_concurrently())

@sio.event
def disconnect():
    print("Disconnected from server")

@sio.on("message")
def on_message(data):
    print(f"Message from server: {data['data']}")
    # Check if server has completed processing audio
    global processing_complete
    if data["data"].lower().startswith("processing complete"):
        processing_complete = True
        sio.disconnect()

@sio.on("audio_response")
def on_audio_response(audio_data):
    print("Received audio response from server")
    with open("response_audio.mp3", "wb") as audio_file:
        audio_file.write(audio_data)
    print("Audio response saved as 'response_audio.mp3'")

# Function to send audio files concurrently using asyncio and ThreadPoolExecutor
async def send_audio_files_concurrently():
    loop = asyncio.get_event_loop()
    with ThreadPoolExecutor() as executor:
        # Send audio files concurrently
        tasks = []
        for audio_file_path in AUDIO_FILE_PATHS:
            task = loop.run_in_executor(executor, send_audio_file, audio_file_path)
            tasks.append(task)
        # Wait for all tasks to complete
        await asyncio.gather(*tasks)

def send_audio_file(audio_file_path):
    # Check if audio file exists
    if os.path.isfile(audio_file_path):
        with open(audio_file_path, "rb") as audio_file:
            audio_data = audio_file.read()  # Read audio file as bytes
            print(f"Sending audio bytes from file: {audio_file_path}")
            sio.emit("chat_audio", audio_data)
    else:
        print(f"Audio file '{audio_file_path}' not found. Skipping audio transmission.")

# Main function to initiate the connection
def main():
    print(f"Connecting to {SERVER_URL}")
    sio.connect(SERVER_URL)
    
    # Wait until processing is complete before disconnecting
    sio.wait()

if __name__ == "__main__":
    main()
