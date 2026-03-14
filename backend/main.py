import time

from fastapi import FastAPI, HTTPException
from .services.schemas import *
from .services.feed_service import build_feed

app = FastAPI()

users = []
posts = []
interactions = []

user_id_seq = 1
post_id_seq = 1
interaction_id_seq = 1

@app.get('/')
def root():
    return {"message": "Running"}


@app.get('/health')
def health():
    return{"status": "ok"}


@app.post("/users", response_model=UserOut)
def create_user(payload: UserCreate):
    """Create a new user, prevent duplicate usernames, and store the result in memory."""
    global user_id_seq

    if any(user["username"] == payload.username for user in users):
        raise HTTPException(status_code=400, detail="Username already exists")

    user = {"id": user_id_seq, "username": payload.username}
    users.append(user)
    user_id_seq += 1
    return user


@app.get('/users', response_model=list[UserOut])
def list_users():
    """Return every user currently stored in the in-memory users list."""
    return users


@app.post("/posts", response_model=PostOut)
def create_post(payload: PostCreate):
    """Create a post for an existing user and save it in the in-memory posts list."""
    global post_id_seq

    if not any(user["id"] == payload.user_id for user in users):
        raise HTTPException(status_code=404, detail="User not found")

    post = {
        "id": post_id_seq,
        "user_id": payload.user_id,
        "content": payload.content,
        "created_at": time.time(),
    }
    posts.append(post)
    post_id_seq += 1
    return post

@app.get('/posts', response_model=list[PostOut])
def list_posts():
    """Return every post currently stored in the in-memory posts list."""
    return posts


@app.post("/interactions", response_model=InteractionOut)
def create_interaction(payload: InteractionCreate):
    """Create an interaction for a valid user and post, then store it in memory."""
    global interaction_id_seq

    if not any(user["id"] == payload.user_id for user in users):
        raise HTTPException(status_code=404, detail="User not found")

    if not any(post["id"] == payload.post_id for post in posts):
        raise HTTPException(status_code=404, detail="Post not found")

    interaction = {
        "id": interaction_id_seq,
        "user_id": payload.user_id,
        "post_id": payload.post_id,
        "event_type": payload.event_type,
    }
    interactions.append(interaction)
    interaction_id_seq += 1
    return interaction
    
@app.get('/interactions', response_model=list[InteractionOut])
def list_interactions():
    """Return every interaction event currently recorded in memory."""
    return interactions



@app.get("/feed/{user_id}", response_model=list[FeedItem])
def get_feed(user_id: int):
    """Build a ranked feed by scoring each post from its views, likes, and comments."""
    return build_feed(user_id, users, posts, interactions)
