from fastapi import APIRouter, Response
import os
from app.camera.capture import open_camera, capture_frame
import threading
import cv2

CAM_MODE = os.getenv("CAM_MODE", "raspberry")

router = APIRouter(prefix="/camera", tags=["Camera"])

_cam = None
_lock = threading.Lock()

@router.get("/status")
def status():
    return {"camera": "ready", "mode": CAM_MODE}

@router.on_event("startup")
def startup():
    global _cam
    if _cam is None:
        _cam = open_camera()

@router.get("/frame")
def get_frame():
    with _lock:
        frame = capture_frame(_cam)
    _, jpg = cv2.imencode(".jpg", frame)
    return Response(content=jpg.tobytes(), media_type="image/jpeg")
