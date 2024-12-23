from fastapi import FastAPI
from app.routes import chat_routes
from fastapi.responses import HTMLResponse

app = FastAPI()

# Include WebSocket route
@app.get("/", summary="Home")
async def get_home():
    return HTMLResponse(content="<center><h1>Learning App</h1></center>", status_code=200) 

app.include_router(chat_routes.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
