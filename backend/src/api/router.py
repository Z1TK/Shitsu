from fastapi import APIRouter

from .routers import *

api_router = APIRouter(prefix="/api")

api_router.include_router(author)
api_router.include_router(tag)
api_router.include_router(genre)
api_router.include_router(publisher)
api_router.include_router(title)
api_router.include_router(user)