from fastapi import APIRouter, Body, Form
from app.services import config_service

router = APIRouter(prefix="", tags=["Config"])

@router.get("/config")
def get_config():
    return config_service.get_config()


@router.post("/config")
def update_config(
    gap: int = Form(...),

    cam0_order: int = Form(...),
    cam0_rotation: int = Form(...),

    cam1_order: int = Form(...),
    cam1_rotation: int = Form(...),

    stream_width: int = Form(...),
    stream_height: int = Form(...),
    stream_quality: int = Form(...),
    stream_fps: int = Form(...)
):
    cam0 = {"order": cam0_order, "rotation": cam0_rotation}
    cam1 = {"order": cam1_order, "rotation": cam1_rotation}
    stream = {
        "resolution": [stream_width, stream_height],
        "quality": stream_quality,
        "fps": stream_fps
    }
    new_config = config_service.update_config(gap, cam0, cam1, stream)
    return {"message": "카메라 설정이 수정되었습니다.", "config": new_config}
