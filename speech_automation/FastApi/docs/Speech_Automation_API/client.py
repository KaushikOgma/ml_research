import sounddevice as sd
import soundfile as sf
import requests

# Function to record audio from the microphone
def record_audio(duration=5, fs=16000, filename="microphone_input.wav"):
    print("Recording audio...")
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
    sd.wait()  # Wait until the recording is finished
    sf.write(filename, audio, fs)  # Save the audio file
    print(f"Audio recorded and saved to {filename}")

    return filename

# Function to send audio file to the FastAPI server
def send_audio_to_api(audio_file):
    url = "http://127.0.0.1:8000/process-audio/"  # Adjust this if your API runs on another host/port
    files = {"file": open(audio_file, "rb")}
    response = requests.post(url, files=files)
    
    if response.status_code == 200:
        with open("output_audio.wav", "wb") as f:
            f.write(response.content)
        print("Processed audio received and saved as output_audio.wav")
    else:
        print("Failed to process the audio:", response.status_code)

if __name__ == "__main__":
    # Record audio from the microphone
    recorded_audio_file = record_audio(duration=5)

    # Send the recorded audio to the FastAPI server
    send_audio_to_api(recorded_audio_file)
