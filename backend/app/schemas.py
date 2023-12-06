from pydantic import BaseModel
from pydantic import ConfigDict


class PostBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    title: str


class PostCreate(PostBase):
    content: str


class PostList(PostBase):
    created_at: int
