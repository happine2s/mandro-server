import asyncio
import base64
import os
import cv2
import threading

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

CAM_MODE = os.getenv("CAM_MODE", "raspberry")

if CAM_MODE == "raspberry":
    from app.camera.capture import open_camera, capture_frame
else:
    from app.camera.mock_capture import open_camera, capture_frame

router = APIRouter(prefix="/ws", tags=["Streaming"])

_cam = open_camera()
_lock = threading.Lock()

@router.websocket("/stream")
async def stream(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            with _lock:
                frame = capture_frame(_cam)

            _, jpg = cv2.imencode(".jpg", frame)
            b64 = base64.b64encode(jpg.tobytes()).decode("utf-8")
            await websocket.send_text(b64)

            await asyncio.sleep(0.1)
    except WebSocketDisconnect:
        print("Client disconnected")
