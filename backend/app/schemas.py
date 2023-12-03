from pydantic import BaseModel


class PostCreate(BaseModel):
    title: str
    content: str


class PostList(BaseModel):
    title: str
    created_at: str
