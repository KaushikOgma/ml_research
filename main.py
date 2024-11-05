from fastapi import FastAPI
from app.routes import chat_routes

app = FastAPI()

# Include WebSocket route
app.include_router(chat_routes.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
