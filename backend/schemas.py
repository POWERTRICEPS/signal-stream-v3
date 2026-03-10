from typing import Literal
from pydantic import BaseModel, Field


# Payload used when creating a new user through the API.
class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=50)


# Payload used when creating a post for an existing user.
class PostCreate(BaseModel):
    user_id: int
    content: str = Field(min_length=1, max_length=1000)


# Public user shape returned by the API.
class UserOut(BaseModel):
    id: int
    username: str


# Public post shape returned by the API.
class PostOut(BaseModel):
    id: int
    user_id: int
    content: str


# Payload used when recording a user action on a post.
class InteractionCreate(BaseModel):
    user_id: int
    post_id: int
    event_type: Literal["view", "like", "comment"]


# Public interaction record returned by the API.
class InteractionOut(BaseModel):
    id: int
    user_id: int
    post_id: int
    event_type: str


# Feed item returned after ranking posts for a user.
class FeedItem(BaseModel):
    id: int
    user_id: int
    content: str
    score: int
    views: int
    likes: int
    comments: int
