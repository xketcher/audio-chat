from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

app = FastAPI()
connected_clients = set()

@app.websocket("/ws/audio")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_clients.add(websocket)
    try:
        while True:
            data = await websocket.receive_bytes()
            for client in connected_clients:
                if client != websocket:
                    await client.send_bytes(data)
    except WebSocketDisconnect:
        connected_clients.remove(websocket)

# Optional: simple UI to test
@app.get("/")
async def get():
    return HTMLResponse("Group Audio Chat Server Running")
