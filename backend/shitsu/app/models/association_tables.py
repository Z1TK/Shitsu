from sqlalchemy import Column, ForeignKey, Table

from backend.shitsu.app.models.base_mode import Base

genre_title_table = Table(
    "genre_title_table",
    Base.metadata,
    Column("genre_id", ForeignKey("genres.id", ondelete="CASCADE"), primary_key=True),
    Column("title_id", ForeignKey("titles.id", ondelete="CASCADE"), primary_key=True),
)

tag_title_table = Table(
    "tag_title_table",
    Base.metadata,
    Column("tag_id", ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True),
    Column("title.id", ForeignKey("titles.id", ondelete="CASCADE"), primary_key=True),
)
