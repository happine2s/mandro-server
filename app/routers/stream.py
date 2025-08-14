from fastapi import APIRouter
from app.streaming import ws

router = APIRouter()
router.include_router(ws.router)
