import time
from collections import defaultdict

from fastapi import HTTPException
from sqlalchemy.orm import Session

from .models import Interaction, Post, User

from backend.redis_client import redis_client


def build_feed(user_id: int, db: Session) -> list[dict]:
    """Build a ranked feed by combining engagement counts with a simple recency boost."""
    if db.get(User, user_id) is None:
        raise HTTPException(status_code=404, detail="User not found")

    ranked_posts = []
    now = time.time()
    posts = db.query(Post).all()

    for post in posts:
        metrics_key = f"post_metrics:{post.id}"
        metrics = redis_client.hgetall(metrics_key)

        views = int(metrics.get("views", 0))
        likes = int(metrics.get("likes", 0))
        comments = int(metrics.get("comments", 0))

        engagement_score = views + (likes * 3) + (comments * 5)
        age_in_hours = max(0, (now - post.created_at) / 3600)
        recency_score = max(0, int(24 - age_in_hours))
        score = engagement_score + recency_score
       
        ranked_posts.append(
            {
                "id": post.id,
                "user_id": post.user_id,
                "content": post.content,
                "score": score,
                "created_at": post.created_at,
                "views": views,
                "likes": likes,
                "comments": comments,
            }
        )

    ranked_posts.sort(key=lambda item: item["score"], reverse=True)
    return ranked_posts

