from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Text, event, String, inspect
from sqlalchemy.dialects.postgresql import UUID
from slugify import slugify
import uuid

from .title import Title
from ..db import Base


class Author(Base):
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String(255), unique=True)
    slug: Mapped[str] = mapped_column(String(255), unique=True)
    pseudunym: Mapped[str] = mapped_column(String(255), unique=True, nullable=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    image: Mapped[str] = mapped_column(String(2048), nullable=True)
    titles: Mapped[list["Title"]] = relationship(
        "Title", back_populates="author", cascade="all, delete-orphan"
    )


@event.listens_for(Author, "before_insert")
def generate_slug(mapper, connection, target):
    if target.name:
        target.slug = slugify(target.name)


@event.listens_for(Author, "before_update")
def update_slug(mapper, connection, target):
    field = inspect(target)
    if field.attrs.name.history.has_changes():
        target.slug = slugify(target.name)
