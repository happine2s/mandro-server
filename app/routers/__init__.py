from fastapi import APIRouter
from app.routers import health, stream

router = APIRouter()
router.include_router(health.router)
router.include_router(stream.router)
