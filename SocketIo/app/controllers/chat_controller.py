import io
import os
import tempfile
import soundfile as sf
from app.services.speech_to_text import openai_speech_to_text
from app.services.grammar_correction import correct_grammar
from app.services.text_to_speech import openai_text_to_speech

AUDIO_SAVE_DIR = "uploads"
CUSTOM_TEMP_DIR = None  # Set a custom directory if needed
SAVE_AUDIO = False

if CUSTOM_TEMP_DIR:
    os.makedirs(CUSTOM_TEMP_DIR, exist_ok=True)

async def handle_audio(sio, sid, audio_data):
    try:
        await sio.emit("message", {"data": "Processing audio... Please wait"}, to=sid)

        # Load audio from buffer
        with io.BytesIO(audio_data) as audio_buffer:
            audio, sample_rate = sf.read(audio_buffer)
            temp_wav_file = tempfile.NamedTemporaryFile(suffix=".wav", dir=CUSTOM_TEMP_DIR)
            sf.write(temp_wav_file.name, audio, sample_rate, format='WAV')
            temp_wav_file.flush()

            # Save the uploaded audio file if SAVE_AUDIO is enabled
            if SAVE_AUDIO:
                os.makedirs(AUDIO_SAVE_DIR, exist_ok=True)
                uploaded_audio_path = os.path.join(AUDIO_SAVE_DIR, "uploaded_audio.wav")
                with open(uploaded_audio_path, "wb") as f:
                    f.write(audio_data)

        # Convert speech to text
        transcribed_text = await openai_speech_to_text(temp_wav_file.name)
        await sio.emit("message", {"data": f"Transcribed Text: {transcribed_text}"}, to=sid)

        # Perform grammar correction on the transcribed text
        corrected_text = await correct_grammar(transcribed_text)
        await sio.emit("message", {"data": f"Corrected Text: {corrected_text}"}, to=sid)

        # Convert the corrected text back to speech
        audio_response_data = await openai_text_to_speech(corrected_text)
        await sio.emit("audio_response", audio_response_data, to=sid)

        # Save output audio if SAVE_AUDIO is enabled
        if SAVE_AUDIO:
            output_audio_path = os.path.join(AUDIO_SAVE_DIR, "converted_audio.mp3")
            with open(output_audio_path, "wb") as audio_file:
                audio_file.write(audio_response_data)

    except Exception as e:
        print(f"Error occurred: {e}")
        await sio.disconnect(sid)

async def handle_text(sio, sid, text_data):
    try:
        # Correct the grammar of the received text
        corrected_text = await correct_grammar(text_data)
        await sio.emit("message", {"data": f"Corrected Text: {corrected_text}"}, to=sid)

    except Exception as e:
        print(f"Error occurred during text processing: {e}")
        await sio.disconnect(sid)
