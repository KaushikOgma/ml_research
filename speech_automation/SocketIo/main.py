import uvicorn
from fastapi import FastAPI
import socketio
from app.routes.chat_routes import init_routes
from app.utils.logger import get_logger

# Initialize FastAPI app and Socket.IO server
app = FastAPI()
sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins="*")
sio_app = socketio.ASGIApp(sio, app)
logger = get_logger(__name__)

@app.on_event("startup")
async def startup_event():
    logger.info("FastAPI app is starting...")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("FastAPI app is shutting down...")

# Initialize routes for socket events
init_routes(sio)

if __name__ == "__main__":
    uvicorn.run("main:sio_app", host="0.0.0.0", port=8000, reload=False)
