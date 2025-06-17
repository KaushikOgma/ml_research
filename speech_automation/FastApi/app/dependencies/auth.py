from fastapi import WebSocket, HTTPException

async def websocket_auth(websocket: WebSocket):
    token = websocket.query_params.get("token")
    if token != "valid_token":
        await websocket.close()
        raise HTTPException(status_code=403, detail="Unauthorized")
    return token
