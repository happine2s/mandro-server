from fastapi import APIRouter, Response, HTTPException
import threading
import cv2

from app.camera.manager import get_camera, capture_frame

router = APIRouter(prefix="/camera", tags=["Camera"])
_lock = threading.Lock()

@router.get("/{index}/frame")
def get_frame(index: int):
    try:
        with _lock:
            frame = capture_frame(index)
        _, jpg = cv2.imencode(".jpg", frame)
        return Response(content=jpg.tobytes(), media_type="image/jpeg")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Camera {index} error: {str(e)}")
