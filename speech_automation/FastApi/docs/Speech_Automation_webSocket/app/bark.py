import replicate
import requests

# Set your Replicate API token directly in the code
REPLICATE_API_TOKEN = "r8_87zWZX1sdJIAIwnLw9Gf11MdaXufyCP3VuDqb"  # Replace with your actual token

def text_to_speech_bark(text):
    # Set the input for the Bark model
    input_data = {
        "text": text,
        "voice": "en_speaker_1"  # Specify voice preset if needed
    }

    # Run the Bark model using Replicate
    try:
        output = replicate.run(
            "suno-ai/bark:b76242b40d67c76ab6742e987628a2a9ac019e11d56ab96c4e91ce03b79b2787",
            input=input_data,
            token=REPLICATE_API_TOKEN  # Pass the API token here
        )

        # The output is a URL to the audio file
        audio_url = output
        print("Audio URL:", audio_url)

        # Optionally, download the audio file
        download_audio(audio_url)
    except Exception as e:
        print(f"An error occurred: {e}")

def download_audio(url):
    response = requests.get(url)

    if response.status_code == 200:
        with open("output_speech.wav", "wb") as audio_file:
            audio_file.write(response.content)
        print("Audio saved to output_speech.wav")
    else:
        print(f"Error downloading audio: Status code {response.status_code}")

def main():
    # User input for text
    text = input("Enter the text you want to convert to speech: ")
    
    # Generate speech
    text_to_speech_bark(text)

if __name__ == "__main__":
    main()
