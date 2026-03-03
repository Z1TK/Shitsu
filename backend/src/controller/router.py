from fastapi import APIRouter

from backend.src.controller.routers.author import author
from backend.src.controller.routers.genre import genre
from backend.src.controller.routers.publisher import publisher
from backend.src.controller.routers.tag import tag
from backend.src.controller.routers.title import title

api_router = APIRouter(prefix="/api")

api_router.include_router(author)
api_router.include_router(tag)
api_router.include_router(genre)
api_router.include_router(publisher)
api_router.include_router(title)
# api_router.include_router(user)
