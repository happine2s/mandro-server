from fastapi import APIRouter

router = APIRouter(prefix="", tags=["Config"])

@router.get("/config")
def get_config():
    return {"left": -30, "right": 30}
