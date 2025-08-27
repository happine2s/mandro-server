from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from app.routers import router as api_router
from fastapi.staticfiles import StaticFiles
from app.services import config_service

app = FastAPI(title="Mandro Server")

config_service.load_config()

app.include_router(api_router)

allow_origins = os.getenv("CORS_ALLOW_ORIGINS", "*")
origins = ["*"] if allow_origins == "*" else [o.strip() for o in allow_origins.split(",")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.mount("/css", StaticFiles(directory="app/static/css"), name="css")
app.mount("/js", StaticFiles(directory="app/static/js"), name="js")
