import uuid

from sqlalchemy import String, event, Boolean, Text, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.shitsu.app.models.title import Title
from backend.shitsu.app.models.user import User
from backend.shitsu.app.models.base_mode import Base


class Comment(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[str] = mapped_column(Text)
    title_id: Mapped[int] = mapped_column(ForeignKey("titles.id"))
    title: Mapped["Title"] = relationship("Title", back_populates="comments")
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship("User", back_populates="comments")
    is_deleted: Mapped[bool] = mapped_column(Boolean, server_default="false")
    likes_count: Mapped[int] = mapped_column(Integer, default=0)
