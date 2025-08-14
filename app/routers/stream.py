import cv2
import base64
import asyncio
from fastapi import APIRouter, WebSocket
from app.camera.camera_manager import CameraManager

router = APIRouter(prefix="", tags=["Stream"])
camera_manager = CameraManager()

@router.websocket("/ws/stream/{index}")
async def stream_camera(websocket: WebSocket, index: int):
    await websocket.accept()
    try:
        while True:
            frame = camera_manager.get_frame(index)
            _, jpeg = cv2.imencode('.jpg', frame)
            encoded = base64.b64encode(jpeg.tobytes()).decode('utf-8')
            await websocket.send_text(encoded)
            await asyncio.sleep(0.03)
    except Exception:
        await websocket.close()
