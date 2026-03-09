from typing import Literal
from pydantic import BaseModel, Field

class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=50)

class PostCreate(BaseModel):
    user_id: int
    contents: str = Field(min_length=1, max_length=1000)

class InteractionCreate(BaseModel):
    user_id: int
    post_id: int
    event_type: Literal["view", "like", "comment"]