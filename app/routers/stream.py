from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import cv2, asyncio
from app.camera.camera_manager import CameraManager
from fastapi.responses import HTMLResponse
from app.services import config_service

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
            conf = config_service.get_config()["stream"]
            width, height = conf["resolution"]
            quality = conf["quality"]
            fps = conf["fps"]

            frame = camera_manager.get_frame(index, (width, height))
            ret, jpeg = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), quality])
            if not ret:
                continue

            await websocket.send_bytes(jpeg.tobytes())
            await asyncio.sleep(1 / fps)
    except WebSocketDisconnect:
        print(f"Camera {index} WebSocket disconnected")