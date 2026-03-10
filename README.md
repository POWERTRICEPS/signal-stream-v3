# Signal Stream v3

Signal Stream v3 is a backend foundation for a personalized content feed system. The project is centered on the core mechanics behind modern recommendation products: event collection, engagement-driven ranking, and feed generation.

The long-term direction is a distributed, event-driven backend that can ingest user activity at scale, transform behavioral signals into ranking features, and deliver personalized feeds with low latency. The current implementation is intentionally lightweight and serves as an early prototype of that architecture.

## Project Goal

This project is designed to explore how a feed platform can evolve from a simple application backend into a recommendation system with production-style architecture. The core idea is straightforward:

- users create content
- user interactions generate events
- events become ranking signals
- ranking logic produces an ordered feed

That flow is the backbone of systems used in social platforms, media products, and content discovery applications.

## Current Scope

The codebase currently provides a minimal FastAPI service that supports:

- user creation
- post creation
- interaction event capture
- feed ranking based on engagement and recency

At this stage, the service uses in-memory storage and a simple scoring model. That keeps the implementation easy to understand while preserving the system boundaries needed for future expansion.

## Architecture Direction

Signal Stream v3 is being shaped around the architecture of a scalable feed-generation system. The intended model includes:

- event-driven ingestion for user actions such as views, likes, and comments
- downstream feature aggregation for ranking inputs
- machine learning or heuristic ranking layers
- feed-serving infrastructure optimized for relevance and response time
- modular services that can be split and scaled independently

The current prototype represents the earliest version of that pipeline, with application logic separated into API, schemas, and feed-ranking services.

## Ranking Model

Feed ordering is currently determined by a lightweight scoring strategy that combines engagement and freshness. Interactions contribute weighted value, and newer posts receive a recency boost. This provides a simple but practical baseline for testing feed behavior before introducing learned ranking models.

This ranking layer is meant to be replaceable. As the system matures, the same flow can support richer feature engineering, offline training pipelines, online inference, and experimentation frameworks.

## Technology Stack

- FastAPI for the backend service layer
- Pydantic for data validation and schema enforcement
- Python for feed logic and service orchestration

## Getting Started

### Prerequisites

- Python 3.11 or newer
- `pip` for dependency installation


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


