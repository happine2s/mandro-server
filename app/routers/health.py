from fastapi import APIRouter

router = APIRouter(prefix="", tags=["Health"])

@router.get("/health")
def health():
    return {"status": "ok"}

@router.get("/version")
def version():
    return {"project": "camera", "mode": "V1"}
