from app.controllers.chat_controller import handle_audio, handle_text

def init_routes(sio):
    # Route for processing audio data
    @sio.on("chat_audio")
    async def chat_audio(sid, audio_data):
        print(f"Received audio data from {sid}")
        # Delegate audio processing to the chat_controller
        await handle_audio(sio, sid, audio_data)

    # Route for processing text data
    @sio.on("chat_text")
    async def chat_text(sid, text_data):
        print(f"Received text from {sid}: {text_data}")
        # Delegate text processing to the chat_controller
        await handle_text(sio, sid, text_data)
