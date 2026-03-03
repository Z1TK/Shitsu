import uuid

from slugify import slugify
from sqlalchemy import String, Text, event, inspect
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.src.app.models.base_mode import Base


class Publisher(Base):
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String(255), unique=True)
    slug: Mapped[str] = mapped_column(String(255), unique=True)
    another_name: Mapped[str] = mapped_column(String(255), unique=True, nullable=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    image: Mapped[str] = mapped_column(String(2048), nullable=True)
    titles: Mapped[list["Title"]] = relationship(
        "Title", back_populates="publisher", cascade="all, delete-orphan"
    )


@event.listens_for(Publisher, "before_insert")
def generate_slug(mapper, connection, target):
    if target.name:
        target.slug = slugify(target.name)


@event.listens_for(Publisher, "before_update")
def update_slug(mapper, connection, target):
    field = inspect(target)
    if field.attrs.name.history.has_changes():
        target.slug = slugify(target.name)
