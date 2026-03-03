from backend.src.app.models.genre import Genre
from backend.src.app.models.tag import Tag
from backend.src.app.repository.base_repo import BaseRepository


class TagRepository(BaseRepository[Tag]):
    model = Tag


class GenreRepository(BaseRepository[Genre]):
    model = Genre
