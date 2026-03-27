from contextlib import asynccontextmanager
import time
import json

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from .database import Base, engine, get_db
from .services.feed_service import build_feed
from .services.models import Interaction, Post, User
from .services.schemas import FeedItem, InteractionCreate, InteractionOut, PostCreate, PostOut, UserCreate, UserOut
from .redis_client import redis_client
from .kafka_producer import publish_interaction_event

@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(lifespan=lifespan)

@app.get('/')
def root():
    return {"message": "Running"}


@app.get('/health')
def health():
    return{"status": "ok"}


@app.post("/users", response_model=UserOut)
def create_user(payload: UserCreate, db: Session = Depends(get_db)):
    """Create a new user and persist it in the database."""
    existing_user = db.query(User).filter(User.username == payload.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    user = User(username=payload.username)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@app.get('/users', response_model=list[UserOut])
def list_users(db: Session = Depends(get_db)):
    """Return every user currently stored in the database."""
    return db.query(User).order_by(User.id).all()


@app.post("/posts", response_model=PostOut)
def create_post(payload: PostCreate, db: Session = Depends(get_db)):
    """Create a post for an existing user and persist it in the database."""
    if db.get(User, payload.user_id) is None:
        raise HTTPException(status_code=404, detail="User not found")

    post = Post(user_id=payload.user_id, content=payload.content, created_at=time.time())
    db.add(post)
    db.commit()
    db.refresh(post)
    return post

@app.get('/posts', response_model=list[PostOut])
def list_posts(db: Session = Depends(get_db)):
    """Return every post currently stored in the database."""
    return db.query(Post).order_by(Post.id).all()


@app.post("/interactions", response_model=InteractionOut)
def create_interaction(payload: InteractionCreate, db: Session = Depends(get_db)):
    """Create an interaction for a valid user and post, then persist it in the database."""
    if db.get(User, payload.user_id) is None:
        raise HTTPException(status_code=404, detail="User not found")

    if db.get(Post, payload.post_id) is None:
        raise HTTPException(status_code=404, detail="Post not found")

    interaction = Interaction(
        user_id=payload.user_id,
        post_id=payload.post_id,
        event_type=payload.event_type,
    )
    db.add(interaction)
    db.commit()
    db.refresh(interaction)

    publish_interaction_event(
        {
            "interaction_id": interaction.id,
            "user_id": interaction.user_id,
            "post_id": interaction.post_id,
            "event_type": interaction.event_type,
            "created_at": time.time(),
        }
    )
    
    return interaction
    
@app.get('/interactions', response_model=list[InteractionOut])
def list_interactions(db: Session = Depends(get_db)):
    """Return every interaction event currently recorded in the database."""
    return db.query(Interaction).order_by(Interaction.id).all()



@app.get("/feed/{user_id}", response_model=list[FeedItem])
def get_feed(user_id: int, db: Session = Depends(get_db)):
    """Return a cached feed when available, otherwise build and cache it."""

    feed_key = f"feed:{user_id}"
    cached_feed = redis_client.get(feed_key)

    if cached_feed:
        print("cache hit")
        return json.loads(cached_feed)
    
    print("cache miss")
    feed = build_feed(user_id, db)
    redis_client.setex(feed_key, 60, json.dumps(feed))
    print("feed cached")
    return feed 