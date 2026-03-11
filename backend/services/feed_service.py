import time

from fastapi import HTTPException


def build_feed(user_id: int, users: list[dict], posts: list[dict], interactions: list[dict]) -> list[dict]:
    """Build a ranked feed by combining engagement counts with a simple recency boost."""
    if not any(user["id"] == user_id for user in users):
        raise HTTPException(status_code=404, detail="User not found")

    ranked_posts = []
    now = time.time()

    for post in posts:
        post_interactions = [item for item in interactions if item["post_id"] == post["id"]]
        views = sum(1 for item in post_interactions if item["event_type"] == "view")
        likes = sum(1 for item in post_interactions if item["event_type"] == "like")
        comments = sum(1 for item in post_interactions if item["event_type"] == "comment")
        engagement_score = views + likes * 3 + comments * 5
        age_in_hours = max(0, (now - post["created_at"]) / 3600)
        recency_score = max(0, int(24 - age_in_hours))
        score = engagement_score + recency_score

        ranked_posts.append(
            {
                "id": post["id"],
                "user_id": post["user_id"],
                "content": post["content"],
                "score": score,
                "created_at": post["created_at"],
                "views": views,
                "likes": likes,
                "comments": comments,
            }
        )

    ranked_posts.sort(key=lambda item: item["score"], reverse=True)
    return ranked_posts


