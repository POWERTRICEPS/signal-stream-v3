# Signal-stream-v3

A distributed backend system that generates personalized content feeds using event-driven architecture and machine learning ranking.

This project simulates how platforms such as **TikTok, Instagram, and Twitter** build ranked feeds from engagement signals (views, likes, comments, dwell time). User interactions are streamed through **Kafka** for asynchronous analytics, feature generation, and model retraining.

Core stack: **FastAPI, PostgreSQL, Redis, Kafka, Docker, and AWS**.

## Key Features

- Personalized feed ranking from real-time engagement signals
- Event-driven architecture powered by Kafka
- Redis-backed low-latency feed and feature access
- Feature pipeline for ranking model training
- Dockerized services for local and cloud deployment
- AWS-ready deployment path

## Architecture (Target)

```text
Users
  |
  v
FastAPI API Gateway
  |-------------------------------> PostgreSQL (users, posts, durable interactions)
  |-------------------------------> Redis (feed cache + online features)
  |
  |  (write interactions)
  v
Kafka topic: user_interactions
  |
  v
Consumer / Feature Pipeline
  |-------------------------------> Redis (feature updates, cache refresh)
  |-------------------------------> PostgreSQL (aggregates, history)
  |
  v
Kafka topic: training_events
  |
  v
Offline retraining jobs -> new ranking model version

Read path for feed:
Users -> FastAPI -> Ranking Service -> Redis/PostgreSQL -> ranked feed response
```

## Kafka Topics

- `user_interactions`: raw engagement events (view, like, comment, share, dwell)
- `feature_updates`: nearline feature aggregates for serving
- `training_events`: model training dataset stream
- `dead_letter` (recommended): malformed or failed-to-process events

## Build Roadmap

- Phase 1: Feed API + PostgreSQL + Redis cache
- Phase 2: Interaction ingestion to Kafka + consumer processing
- Phase 3: Baseline ranker (heuristic recency + popularity)
- Phase 4: ML ranking model + scheduled retraining pipeline
- Phase 5: Observability (latency, Kafka lag, cache hit rate, ranking quality)

## Getting Started

### Prerequisites

- Docker
- Docker Compose
- Git

### 1. Clone the repository

```bash
git clone https://github.com/yourname/signal-stream-v3.git
cd signal-stream-v3
```

### 2. Start the system

```bash
docker-compose up --build
```

### 3. Open API docs

```text
http://localhost:8000/docs
```










