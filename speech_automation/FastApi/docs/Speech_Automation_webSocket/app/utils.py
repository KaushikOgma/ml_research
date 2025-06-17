import sounddevice as sd
import numpy as np
import soundfile as sf
import torch
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline, AutoModelForTextToWaveform
import os
from google.generativeai import GenerativeModel, configure as genai_config
from scipy.io.wavfile import write as write_wav
from playsound import playsound

# Function to save recorded audio to a file
def save_audio(audio, filename="temp_audio.wav", fs=16000):
    sf.write(filename, audio, fs)
    print(f"Audio saved to {filename}")

# Load Whisper model and convert speech to text
def speech_to_text(audio_file, model_dir="models/", model_id="openai/whisper-large-v3"):
    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

    # Construct model save paths
    model_name = model_id.split("/")[-1]
    model_path = os.path.join(model_dir, model_name)
    model_file = os.path.join(model_path, "pytorch_model.bin")
    processor_dir = os.path.join(model_path, "preprocessor_config.json")

    # Download model if necessary
    if not (os.path.exists(model_file) and os.path.exists(processor_dir)):
        print(f"Model files not found. Downloading the model to {model_path}...")
        os.makedirs(model_path, exist_ok=True)
        model = AutoModelForSpeechSeq2Seq.from_pretrained(model_id, torch_dtype=torch_dtype, cache_dir=model_path)
        processor = AutoProcessor.from_pretrained(model_id, cache_dir=model_path)
    else:
        print(f"Model files found at {model_path}. Loading from disk...")
        model = AutoModelForSpeechSeq2Seq.from_pretrained(model_path, torch_dtype=torch_dtype)
        processor = AutoProcessor.from_pretrained(model_path)

    # Create speech-to-text pipeline
    pipe = pipeline("automatic-speech-recognition", model=model, tokenizer=processor.tokenizer, feature_extractor=processor.feature_extractor, device=device)
    result = pipe(audio_file)
    return result["text"]

# Grammar correction using Google Gemini API
def correct_grammar(api_key, text):
    genai_config(api_key=api_key)
    model = GenerativeModel("models/gemini-1.0-pro-latest")

    prompt = '''
    You are a highly knowledgeable language teacher with in-depth expertise in multiple languages. Your role is to correct grammar and ensure fluent, accurate language...
    '''
    response = model.generate_content(prompt + text)
    return response.text

# Convert corrected text to speech using Bark model
def text_to_speech_bark(text, output_file="speech.wav", voice_preset=None):
    processor = AutoProcessor.from_pretrained("suno/bark")
    model = AutoModelForTextToWaveform.from_pretrained("suno/bark")

    inputs = processor(text, return_tensors="pt", voice_preset=voice_preset)

    with torch.no_grad():
        audio_array = model.generate(input_ids=inputs["input_ids"], attention_mask=inputs["attention_mask"]).cpu().numpy().squeeze()

    write_wav(output_file, 24000, audio_array)
    print(f"Speech saved to {output_file}")