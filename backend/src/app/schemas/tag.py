from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field


class TagReadSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: Annotated[int, Field()]
    name: Annotated[str, Field(max_length=255)]
