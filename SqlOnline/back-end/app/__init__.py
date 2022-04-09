from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.db import AppDB


app = FastAPI()
api = APIRouter(
    prefix="/api/v1",
    tags=["api_v1"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/assets", StaticFiles(directory="static/assets"), name="assets")

db_file = "app.db"
app_db = AppDB(db_file)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


from app import routes
from app import api_routes

app.include_router(api)
