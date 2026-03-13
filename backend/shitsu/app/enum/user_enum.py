import enum


class RoleEnum(str, enum.Enum):
    READER = "reader"
    TRANSLATOR = "translator"
    MODERATOR = "moderator"
    ADMIN = "admin"
