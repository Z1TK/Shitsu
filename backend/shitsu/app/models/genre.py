from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.shitsu.app.models.association_tables import genre_title_table
from backend.shitsu.app.models.base_mode import Base


class Genre(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), unique=True)
    titles: Mapped[list["Title"]] = relationship(
        secondary=genre_title_table, back_populates="genres"
    )
