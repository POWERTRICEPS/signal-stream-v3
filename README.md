# Signal Stream v3

Signal Stream v3 is a backend foundation for a personalized content feed system. The project focuses on the core mechanics behind modern recommendation products: event collection, engagement-driven ranking, caching, and feed generation.

The long-term direction is a distributed, event-driven backend that can ingest user activity at scale, transform behavioral signals into ranking features, and deliver personalized feeds with low latency. The current implementation is intentionally lightweight and serves as an early prototype of that architecture.


## Getting Started

### Prerequisites

- Python 3.11 or newer
- `pip` for dependency installation
- Docker Desktop or Docker Engine with `docker compose`

### Installation

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install project dependencies:

```bash
pip install -r requirements.txt
```

Create and setup `.env` file in the project root:


### Run Infrastructure

Start PostgreSQL, Redis, and Kafka:

```bash
docker compose up -d
```

You can confirm the containers are running with:

```bash
docker compose ps
```

### Run Locally

Start the FastAPI server from the project root:

```bash
uvicorn backend.main:app --reload
```

The application will be available at `http://127.0.0.1:8000`.

### Verify The Service

You can confirm the server is running by opening:

- `http://127.0.0.1:8000/`
- `http://127.0.0.1:8000/health`

Interactive API docs are also available at:

- `http://127.0.0.1:8000/docs`

### Seed Sample Data

With the API running, you can seed users, posts, and interactions:

```bash
python3 scripts/seed_data.py
```

This script talks to the running API over HTTP, and the API writes the resulting data into PostgreSQL.

### Kafka Consumer

A simple consumer script is included for experimenting with the interaction event stream:

```bash
python3 scripts/interaction_consumer.py
```





