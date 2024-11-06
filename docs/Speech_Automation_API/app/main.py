from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
import os
from utils import save_audio, speech_to_text, correct_grammar, text_to_speech_bark

app = FastAPI()

# Ensure the models directory exists
if not os.path.exists("models"):
    os.makedirs("models")

# Define the API route for processing voice input
@app.post("/process-audio/")
async def process_audio(file: UploadFile = File(...)):
    # Step 1: Save uploaded audio file
    audio_file = "uploaded_audio.wav"
    with open(audio_file, "wb") as buffer:
        buffer.write(await file.read())

    # Step 2: Convert speech to text
    transcribed_text = speech_to_text(audio_file, model_dir="models/")
    print("Transcribed Text:", transcribed_text)

    # Step 3: Correct grammar and pronunciation
    api_key = "AIzaSyBCW-TszvSeBUqHd2Ap7gpnjaVUG5BAlx0"  # Replace with your actual API key
    corrected_text = correct_grammar(api_key, transcribed_text)
    print("Corrected Text:", corrected_text)

    # Step 4: Convert corrected text to speech
    output_audio_file = "final_output.wav"
    text_to_speech_bark(corrected_text, output_file=output_audio_file)
    print(f"Final speech saved to {output_audio_file}")

    # Return the final processed audio file as a response
    return FileResponse(output_audio_file, media_type="audio/wav", filename="final_output.wav")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)