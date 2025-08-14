from fastapi import APIRouter, Body, Form

router = APIRouter(prefix="", tags=["Config"])

config_data = {
    "gap": 76,
    "distorted": False
}

@router.get("/config")
def get_config():
    return config_data

@router.post("/config")
def update_config(
    gap: int = Form(...),
    distorted: bool = Form(...)
):
    config_data["gap"] = gap
    config_data["distorted"] = distorted

    return {"message": "좌우 보정값이 수정되었습니다.", "config": config_data}
