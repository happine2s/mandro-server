from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
from app.routers import router as api_router
from fastapi.staticfiles import StaticFiles

load_dotenv()

app = FastAPI(title="Mandro Server")
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
