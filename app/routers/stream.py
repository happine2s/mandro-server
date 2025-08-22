import cv2
import base64
import asyncio
from fastapi import APIRouter, WebSocket
from app.camera.camera_manager import CameraManager
from fastapi.responses import HTMLResponse

router = APIRouter(prefix="", tags=["Stream"])
camera_manager = CameraManager()


@router.get("/", response_class=HTMLResponse)
def get_stream_page():
    with open("app/static/stream.html", "r") as f:
        return HTMLResponse(f.read())

@router.websocket("/ws/stream/{index}")
async def stream_camera(websocket: WebSocket, index: int):
    await websocket.accept()
    try:
        while True:
            frame = camera_manager.get_frame(index)
            ret, jpeg = cv2.imencode('.jpg', frame)
            if not ret:
                continue
            await websocket.send_bytes(jpeg.tobytes())
            await asyncio.sleep(0.01)
    except Exception:
        await websocket.close()

