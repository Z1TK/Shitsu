import uuid

from sqlalchemy import String, event
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from backend.shitsu.app.models.base_mode import Base


class User(Base):
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    username: Mapped[str] = mapped_column(String(25), unique=True)
    password: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column(String(255), unique=True)
    avatar: Mapped[str] = mapped_column(String(2048))
