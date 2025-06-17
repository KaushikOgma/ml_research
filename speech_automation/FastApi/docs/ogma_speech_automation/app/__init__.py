# @Author : Rahul Sinha
# @Date : 22 October 2024


# This file ensures the app package is recognized.
from .controller import chat_controller
from .services import grammar_correction, speech_to_text, text_to_speech, websocket_service
from .routes import chat_routes
from .dependencies import auth
