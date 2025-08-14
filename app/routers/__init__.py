from fastapi import APIRouter
from app.routers import health, camera, stream

router = APIRouter()
router.include_router(health.router)
router.include_router(camera.router)
router.include_router(stream.router)
