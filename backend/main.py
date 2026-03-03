from fastapi import FastAPI

from backend.src.controller.router import api_router

app = FastAPI()

app.include_router(api_router)
