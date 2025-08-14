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

_cam = None
_lock = threading.Lock()

@router.websocket("/stream")
async def stream(websocket: WebSocket):
    await websocket.accept()
    await websocket.send_text("connected")
