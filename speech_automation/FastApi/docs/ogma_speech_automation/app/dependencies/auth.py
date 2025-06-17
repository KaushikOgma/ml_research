# @Author : Rahul Sinha
# @Date : 22 October 2024

from fastapi import WebSocket, Depends, HTTPException

async def websocket_auth(websocket: WebSocket):
    token = websocket.query_params.get("token")
    if token != "valid_token":  
        await websocket.close()
        raise HTTPException(status_code=403, detail="Unauthorized")
