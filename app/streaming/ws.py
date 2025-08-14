import asyncio
import base64
import os
import cv2
import threading

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.camera.capture import open_camera, capture_frame
from app.routers.camera import get_camera


router = APIRouter(prefix="/ws", tags=["Streaming"])
_lock = threading.Lock()

@router.websocket("/stream")
async def stream(websocket: WebSocket):
    await websocket.accept()
    await websocket.send_text("connected")

    cam = get_camera()
    if cam is None:
        await websocket.send_text("Camera not initialized.")
        await websocket.close()
        return

    try:
        while True:
            with _lock:
                frame = cam.capture_array()
            _, buffer = cv2.imencode('.jpg', frame)
            jpg_as_text = base64.b64encode(buffer).decode("utf-8")
            await websocket.send_text(jpg_as_text)
            await asyncio.sleep(0.1)  # 10 FPS
    except WebSocketDisconnect:
        print("WebSocket connection closed.")
