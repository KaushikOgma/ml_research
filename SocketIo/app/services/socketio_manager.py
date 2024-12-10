import socketio

class SocketIOManager:
    def __init__(self):
        self.sio = socketio.AsyncServer(async_mode="asgi")
        self.app = socketio.ASGIApp(self.sio)

    async def connect(self, sid, environ):
        """ Handle new socket connection """
        print(f"Client {sid} connected.")
    
    async def disconnect(self, sid):
        """ Handle disconnection """
        print(f"Client {sid} disconnected.")
    
    async def send_personal_message(self, message: str, sid: str):
        """ Send a message to a specific client """
        await self.sio.emit("message", {"data": message}, to=sid)

    async def broadcast(self, message: str):
        """ Send a message to all connected clients """
        await self.sio.emit("message", {"data": message})

    def init_routes(self):
        """ Register routes for socket events (called from chat_routes.py) """
        @self.sio.event
        async def connect(sid, environ):
            await self.connect(sid, environ)

        @self.sio.event
        async def disconnect(sid):
            await self.disconnect(sid)
