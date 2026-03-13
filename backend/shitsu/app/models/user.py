import uuid

from sqlalchemy import Boolean, String, event
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.shitsu.app.enum.user_enum import RoleEnum
from backend.shitsu.app.models.base_mode import Base


class User(Base):
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    username: Mapped[str] = mapped_column(String(25), unique=True)
    password: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column(String(255), unique=True)
    avatar: Mapped[str] = mapped_column(String(2048))
    is_verified: Mapped[bool] = mapped_column(Boolean, server_default="false")
    role: Mapped[RoleEnum] = mapped_column(default="reader")
    comments: Mapped[list["Comment"]] = relationship(
        "Comment", back_populates="user", cascade="all, delete-orphan"
    )
