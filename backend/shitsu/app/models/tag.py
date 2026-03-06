from sqlalchemy import ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.shitsu.app.models.association_tables import tag_title_table
from backend.shitsu.app.models.base_mode import Base


class Tag(Base):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), unique=True)
    titles: Mapped[list["Title"]] = relationship(
        secondary=tag_title_table, back_populates="tags"
    )
