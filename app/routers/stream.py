from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import cv2, asyncio
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
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 95]

    try:
        while True:
            frame = camera_manager.get_frame(index)
            ret, jpeg = cv2.imencode('.jpg', frame, encode_param)
            if not ret:
                continue
            await websocket.send_bytes(jpeg.tobytes())
            await asyncio.sleep(0.01)
    except WebSocketDisconnect:
        print(f"Camera {index} WebSocket disconnected")
    except Exception as e:
        print(f"Error in stream_camera({index}):", e)
    finally:
        if not websocket.client_state.name == "DISCONNECTED":
            await websocket.close()
