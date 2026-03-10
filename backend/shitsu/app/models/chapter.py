import uuid

from sqlalchemy import String, event, Boolean, Text, ForeignKey, Integer, Float, ARRAY
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.shitsu.app.models.base_mode import Base


class Chapter(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    volume: Mapped[int] = mapped_column(Integer)
    number: Mapped[float] = mapped_column(Float)
    pages: Mapped[list[str]] = mapped_column(ARRAY(String))
    title_id: Mapped[int] = mapped_column(ForeignKey("titles.id"))
    title: Mapped["Title"] = relationship("Title", back_populates="chapters")
