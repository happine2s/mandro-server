from pydantic import BaseModel
from fastapi import APIRouter, Body, Form

router = APIRouter(prefix="", tags=["Config"])

config_data = {
    "left": 60,
    "right": 60,
    "distorted": False
}

class ConfigPayload(BaseModel):
    left: int
    right: int
    distorted: bool

@router.get("/config")
def get_config():
    return config_data

@router.post("/config")
def update_config(
    left: int = Form(...),
    right: int = Form(...),
    distorted: bool = Form(...)
):
    config_data["left"] = left
    config_data["right"] = right
    config_data["distorted"] = distorted

    return {"message": "좌우 보정값이 수정되었습니다.", "config": config_data}
