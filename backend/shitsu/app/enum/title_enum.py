import enum


class TypeEnum(str, enum.Enum):
    MANGA = "manga"
    MANHWA = "manhwa"
    MANHUA = "manhua"
    OEL_MANGA = "oel-manga"


class StatusEnum(str, enum.Enum):
    ONGOING = "ongoing"
    COMPLETED = "completed"
    DISCONTINUED = "discontinued"
    ANNOUNCED = "announced"


class ReleaseEnum(str, enum.Enum):
    YONKOMA = "yonkoma"
    ANTHOLOGY = "anthology"
    DOUJINSHI = "doujinshi"
    COLORED = "colored"
    ONE_SHOT = "one-shot"
    WEB = "web"
    WEBTOON = "webtoon"
