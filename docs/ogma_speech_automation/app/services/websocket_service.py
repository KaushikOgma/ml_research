# @Author : Rahul Sinha
# @Date : 22 October 2024

from fastapi import WebSocket

class WebSocketManager:
    def __init__(self):
        self.active_connections = []

    async def connect(self, websocket: WebSocket):
        """
        Accept the WebSocket connection and add it to active connections.
        :param websocket: The WebSocket instance.
        """
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        """
        Remove the WebSocket from active connections.
        :param websocket: The WebSocket instance to be removed.
        """
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        """
        Send a personal message to a specific WebSocket client.
        :param message: The message to be sent.
        :param websocket: The WebSocket instance to send the message to.
        """
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        """
        Broadcast a message to all active WebSocket clients.
        :param message: The message to be broadcasted.
        """
        for connection in self.active_connections:
            await connection.send_text(message)
