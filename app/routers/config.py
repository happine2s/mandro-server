from fastapi import APIRouter, Body

router = APIRouter(prefix="", tags=["Config"])

config_data = {
    "left": 30,
    "right": 30
}

@router.get("/config")
def get_config():
    return config_data

@router.post("/config")
def update_config(payload: dict = Body(...)):
    left = payload.get("left")
    right = payload.get("right")

    if left is not None:
        config_data["left"] = left
    if right is not None:
        config_data["right"] = right

    return {"message": "좌우 보정값이 수정되었습니다.", "config": config_data}
