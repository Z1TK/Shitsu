from backend.shitsu.app.models.genre import Genre
from backend.shitsu.app.models.tag import Tag
from backend.shitsu.app.repository.base_repo import BaseRepository


class TagRepository(BaseRepository[Tag]):
    model = Tag


class GenreRepository(BaseRepository[Genre]):
    model = Genre
