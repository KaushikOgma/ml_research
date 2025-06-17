# @Author : Rahul Sinha
# @Date : 22 October 2024

from fastapi import APIRouter, WebSocket, Depends
from app.dependencies.auth import websocket_auth
from app.controller.chat_controller import process_audio
from app.services.websocket_service import WebSocketManager

router = APIRouter()

# WebSocketManager for handling connections
websocket_manager = WebSocketManager()

@router.websocket("/chat/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str, auth=Depends(websocket_auth)):
    await websocket_manager.connect(websocket)
    try:
        await process_audio(websocket) 
    except Exception as e:
        print(f"Exception in WebSocket: {e}")
    finally:
        websocket_manager.disconnect(websocket)
