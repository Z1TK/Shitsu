from fastapi import APIRouter

from backend.shitsu.controller.routers.author import author
from backend.shitsu.controller.routers.genre import genre
from backend.shitsu.controller.routers.publisher import publisher
from backend.shitsu.controller.routers.tag import tag
from backend.shitsu.controller.routers.title import title
from backend.shitsu.controller.routers.user import user

api_router = APIRouter(prefix="/api")

api_router.include_router(author)
api_router.include_router(tag)
api_router.include_router(genre)
api_router.include_router(publisher)
api_router.include_router(title)
api_router.include_router(user)
