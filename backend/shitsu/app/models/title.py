import uuid

from slugify import slugify
from sqlalchemy import ForeignKey, Integer, String, Text, event, inspect
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates

from backend.shitsu.app.enum.title_enum import *
from backend.shitsu.app.models.association_tables import (genre_title_table,
                                                          tag_title_table)
from backend.shitsu.app.models.base_mode import Base
from backend.shitsu.app.models.chapter import Chapter
from backend.shitsu.app.models.comment import Comment
from backend.shitsu.app.models.genre import Genre
from backend.shitsu.app.models.publisher import Publisher
from backend.shitsu.app.models.tag import Tag


class Title(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(255))
    slug: Mapped[str] = mapped_column(String(255), unique=True)
    description: Mapped[str] = mapped_column(Text)
    alternative_title: Mapped[str] = mapped_column(
        String(255), nullable=True, unique=True
    )
    cover: Mapped[str] = mapped_column(String(2048))
    release_year: Mapped[int] = mapped_column(Integer)
    type: Mapped[TypeEnum] = mapped_column(default="manga")
    status: Mapped[StatusEnum] = mapped_column(default="ongoing")
    release_format: Mapped[ReleaseEnum] = mapped_column(nullable=True)
    author_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("authors.id"))
    author: Mapped["Author"] = relationship("Author", back_populates="titles")
    publisher_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("publishers.id"))
    publisher: Mapped["Publisher"] = relationship("Publisher", back_populates="titles")
    genres: Mapped[list["Genre"]] = relationship(
        secondary=genre_title_table, back_populates="titles"
    )
    tags: Mapped[list["Tag"]] = relationship(
        secondary=tag_title_table, back_populates="titles"
    )
    comments: Mapped[list["Comment"]] = relationship(
        "Comment", back_populates="title", cascade="all, delete-orphan"
    )
    chapters: Mapped[list["Chapter"]] = relationship(
        "Chapter", back_populates="title", cascade="all, delete-orphan"
    )

    @validates("release_year")
    def validate_release_year(self, key, year):
        if year <= 0:
            raise ValueError("release_year must be positive")
        return year


@event.listens_for(Title, "before_insert")
def generate_slug(mapper, connection, target):
    if target.title:
        target.slug = slugify(target.title)


@event.listens_for(Title, "before_update")
def update_slug(mapper, connection, target):
    field = inspect(target)
    if field.attrs.title.history.has_changes():
        target.slug = slugify(target.title)
