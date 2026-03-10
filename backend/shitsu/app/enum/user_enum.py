import enum


class Role(str, enum.Enum):
    READER = "reader"
    TRANSLATOR = "translator"
    MODERATOR = "moderator"
    ADMIN = "admin"
