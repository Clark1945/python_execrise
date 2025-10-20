from fastapi import APIRouter
from starlette.responses import HTMLResponse
from starlette.websockets import WebSocket

router = APIRouter(prefix="/messages", tags=["Message"])

# 一個簡單的 HTML 客戶端（可直接用來測試）
html = """
<!DOCTYPE html>
<html>
    <head>
        <title>FastAPI WebSocket Demo</title>
    </head>
    <body>
        <h1>🛰️ WebSocket Echo Test</h1>
        <input id="msgInput" type="text" placeholder="Type a message...">
        <button onclick="sendMessage()">Send</button>
        <ul id="messages"></ul>
        <script>
            var ws = new WebSocket("ws://localhost:8000/ws");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages');
                var li = document.createElement('li');
                li.textContent = 'Server: ' + event.data;
                messages.appendChild(li);
            };
            function sendMessage() {
                var input = document.getElementById("msgInput");
                ws.send(input.value);
                input.value = '';
            }
        </script>
    </body>
</html>
"""

@router.get("/")
async def get():
    return HTMLResponse(html)

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    # 接受連線
    await websocket.accept()
    await websocket.send_text("Connected to FastAPI WebSocket 🚀")

    try:
        while True:
            data = await websocket.receive_text()
            print(f"📩 Received: {data}")
            await websocket.send_text(f"Echo: {data}")
    except Exception as e:
        print("❌ Connection closed:", e)