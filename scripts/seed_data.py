import argparse
import json
import random
import urllib.error
import urllib.request


EVENT_TYPES = ["view", "like", "comment"]
POST_TEMPLATES = [
    "Learning FastAPI one route at a time.",
    "Testing feed ranking with some fake engagement.",
    "Building a small social backend for practice.",
    "Posting sample content to seed the app.",
    "Trying a recency plus engagement ranking formula.",
]


def post_json(base_url: str, path: str, payload: dict) -> dict:
    request = urllib.request.Request(
        url=f"{base_url}{path}",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    with urllib.request.urlopen(request) as response:
        return json.loads(response.read().decode("utf-8"))


def create_users(base_url: str, count: int) -> list[dict]:
    users = []
    for index in range(1, count + 1):
        payload = {"username": f"user{index}"}
        users.append(post_json(base_url, "/users", payload))
    return users


def create_posts(base_url: str, users: list[dict], count: int) -> list[dict]:
    posts = []
    for index in range(1, count + 1):
        user = random.choice(users)
        template = random.choice(POST_TEMPLATES)
        payload = {
            "user_id": user["id"],
            "content": f"{template} Sample post #{index}.",
        }
        posts.append(post_json(base_url, "/posts", payload))
    return posts


def create_interactions(base_url: str, users: list[dict], posts: list[dict], count: int) -> list[dict]:
    interactions = []
    for _ in range(count):
        user = random.choice(users)
        post = random.choice(posts)
        payload = {
            "user_id": user["id"],
            "post_id": post["id"],
            "event_type": random.choice(EVENT_TYPES),
        }
        interactions.append(post_json(base_url, "/interactions", payload))
    return interactions


def main() -> None:
    parser = argparse.ArgumentParser(description="Seed the Signal Stream API with fake data.")
    parser.add_argument("--base-url", default="http://127.0.0.1:8000", help="Base URL for the running API.")
    parser.add_argument("--users", type=int, default=10, help="Number of users to create.")
    parser.add_argument("--posts", type=int, default=100, help="Number of posts to create.")
    parser.add_argument("--interactions", type=int, default=1000, help="Number of interactions to create.")
    parser.add_argument("--seed", type=int, default=42, help="Random seed for reproducible fake data.")
    args = parser.parse_args()

    random.seed(args.seed)

    try:
        users = create_users(args.base_url, args.users)
        posts = create_posts(args.base_url, users, args.posts)
        interactions = create_interactions(args.base_url, users, posts, args.interactions)
    except urllib.error.URLError as error:
        raise SystemExit(f"Could not reach the API at {args.base_url}: {error}") from error
    except urllib.error.HTTPError as error:
        details = error.read().decode("utf-8", errors="ignore")
        raise SystemExit(f"API request failed with status {error.code}: {details}") from error

    print(f"Created {len(users)} users")
    print(f"Created {len(posts)} posts")
    print(f"Created {len(interactions)} interactions")


if __name__ == "__main__":
    main()
