from fastapi import HTTPException

from backend.shitsu.app.repository.tag_genre_repo import GenreRepository, TagRepository
from backend.shitsu.app.schemas.genre import GenreReadSchema
from backend.shitsu.app.schemas.tag import TagReadSchema
from backend.shitsu.app.logger import log


class GenreService:

    @staticmethod
    async def get_all_genres(page: int, limit: int):
        log.info(f"Fetching all genres: page={page}, limit={limit}")
        genres = await GenreRepository.get_all(page, limit)
        if not genres:
            log.warning("No genres found")
            raise HTTPException(status_code=404, detail="Genres not found")
        log.info(f"Found {len(genres)} genres")
        return [GenreReadSchema.model_validate(genre).model_dump() for genre in genres]


class TagService:

    @staticmethod
    async def get_all_tags(page: int, limit: int):
        log.info(f"Fetching all tags: page={page}, limit={limit}")
        tags = await TagRepository.get_all(page, limit)
        if not tags:
            log.warning("No tags found")
            raise HTTPException(status_code=404, detail="Tags not found")
        log.info(f"Found {len(tags)} tags")
        return [TagReadSchema.model_validate(tag).model_dump() for tag in tags]
