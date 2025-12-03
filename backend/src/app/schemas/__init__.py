from .author import (
    AuthorCreateSchema,
    AuthorIdSchema,
    AuthorReadSchema,
    AuthorUpdateSchema,
)
from .genre import GenreReadSchema
from .tag import TagReadSchema
from .publisher import (
    PublisherCreateSchema,
    PublisherIdschema,
    PublisherReadSchema,
    PublisherUpdateSchema,
)
from .title import (
    TitleCreateSchema,
    TitleReadAllSchema,
    TitleReadIDSchema,
    TitleUpdateSchema,
)
from .user import LoginUser, Token, UserRead, RegisterSchema

AuthorIdSchema.model_rebuild()
PublisherIdschema.model_rebuild()
TitleReadIDSchema.model_rebuild()
