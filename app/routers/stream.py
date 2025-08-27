from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import cv2, asyncio, time
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
            conf = config_service.get_config().get("stream", {})
            width, height = conf.get("resolution", [640, 480])
            quality = conf.get("quality", 80)
            fps = max(1, min(conf.get("fps", 15), 30))  # 1~30 제한

            # 프레임 캡처
            frame = camera_manager.get_frame(index, (width, height))
            if frame is None:
                await asyncio.sleep(1 / fps)
                continue

            # JPEG 인코딩
            try:
                ret, jpeg = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), quality])
                if not ret:
                    await asyncio.sleep(1 / fps)
                    continue
            except cv2.error as e:
                print(f"Camera {index} JPEG 인코딩 실패: {e}")
                await asyncio.sleep(1 / fps)
                continue

            # 바이너리 전송
            start = time.monotonic()
            await websocket.send_bytes(jpeg.tobytes())

            # FPS 제어 (과도한 전송 방지)
            elapsed = time.monotonic() - start
            delay = max(0, (1 / fps) - elapsed)
            await asyncio.sleep(delay)

    except WebSocketDisconnect:
        print(f"Camera {index} WebSocket disconnected")
    except Exception as e:
        print(f"Camera {index} WebSocket error: {e}")
