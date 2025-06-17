from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from app.controllers.chat_controller import process_audio, process_text
from app.dependencies.auth import websocket_auth
from app.services.websocket_service import WebSocketManager

router = APIRouter()
websocket_manager = WebSocketManager()

# Original endpoint for audio processing
@router.websocket("/chat/audio")
async def websocket_audio_endpoint(websocket: WebSocket, auth=Depends(websocket_auth)):
    await websocket_manager.connect(websocket)
    try:
        await process_audio(websocket)
    except WebSocketDisconnect:
        websocket_manager.disconnect(websocket)
        print(f"Client disconnected")

# New endpoint for text processing (grammar and pronunciation check)
@router.websocket("/chat/text")
async def websocket_text_endpoint(websocket: WebSocket, auth=Depends(websocket_auth)):
    await websocket_manager.connect(websocket)
    try:
        await process_text(websocket) 
    except WebSocketDisconnect:
        websocket_manager.disconnect(websocket)
        print(f"Client disconnected")
