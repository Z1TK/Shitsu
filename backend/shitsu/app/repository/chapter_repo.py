from backend.shitsu.app.repository.base_repo import BaseRepository
from backend.shitsu.app.models.chapter import Chapter


class ChapterRepository(BaseRepository[Chapter]):
    model = Chapter
