# Signal Stream v3

Signal Stream v3 is a lightweight FastAPI backend for creating users, publishing posts, recording engagement events, and generating a ranked feed from interaction data. It is designed as a simple foundation for a social feed or recommendation system prototype.

## Overview

The service exposes REST endpoints for:

- Creating and listing users
- Creating and listing posts
- Recording post interactions such as `view`, `like`, and `comment`
- Building a ranked feed using weighted engagement signals

The current implementation uses:

- FastAPI for the HTTP API
- Pydantic for request and response validation
- SQLite for local persistence

## Ranking Logic

Feed ranking is calculated from recorded post interactions using a simple weighted score:

```text
score = views + (likes * 3) + (comments * 5)
```

Posts with higher scores appear earlier in the feed response.


## Request Examples

Create a user:

```json
{
  "username": "alice"
}
```

Create a post:

```json
{
  "user_id": 1,
  "content": "My first post"
}
```

Create an interaction:

```json
{
  "user_id": 1,
  "post_id": 1,
  "event_type": "like"
}
```

## Local Setup

### 1. Create and activate a virtual environment

Windows PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the API

```bash
uvicorn backend.main:app --reload
```

### 4. Open the documentation

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## Data Storage

Application data is stored in a local SQLite database file created automatically at:

`backend/app.db`

This allows users, posts, and interactions to persist across server restarts during local development.



## License

This project is distributed under the terms defined in [LICENSE](/c:/Users/imnot/CODING/project01/signal-stream-v3/LICENSE).
