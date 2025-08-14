from fastapi import APIRouter
from app.routers import health, camera

router = APIRouter()
router.include_router(health.router)
router.include_router(camera.router)