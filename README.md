# FastAPI Backend Services

A production-ready FastAPI backend with PDF processing, AI document classification, and multi-database connectivity.

## Features

- **Modular structure** – routers / services / repositories / schemas / utils
- **Versioned API** – all endpoints under `/api/v1/`
- **JWT authentication** with API-key fallback
- **PDF extraction** – text via `pdfplumber`, image pages via `pytesseract` OCR
- **AI classification** – pluggable provider (mock or OpenAI)
- **DB Playground** – run ad-hoc queries against Teradata, IBM DB2, or SQL Server
- **Comparison engine** – diff classified document data against database records
- **Background tasks** – long-running jobs run off the request path
- **Async endpoints** throughout
- **Pydantic v2 validation** on all inputs / outputs
- **Structured JSON logging**
- **Docker + docker-compose** ready

## Quick Start

### Local (Python 3.11+)

```bash
# 1. Clone and enter the repo
git clone https://github.com/shrikantkingdom/FastAPI && cd FastAPI

# 2. Create a virtual environment
python -m venv .venv && source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Copy env file and customise
cp .env.example .env

# 5. Start the server
uvicorn app.main:app --reload --port 8000
```

### Docker

```bash
docker-compose up --build
```

The API is then available at `http://localhost:8000`.
Interactive docs: `http://localhost:8000/docs`

## API Reference

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/api/v1/health` | – | Health check |
| POST | `/api/v1/auth/login` | – | Obtain JWT token |
| GET | `/api/v1/auth/me` | JWT | Current user info |
| POST | `/api/v1/documents/upload` | JWT | Upload & process PDF |
| POST | `/api/v1/documents/extract-path` | JWT | Extract PDF from path |
| POST | `/api/v1/db/query` | JWT | Run DB query |
| POST | `/api/v1/db/compare` | JWT | Compare classified data vs DB |
| POST | `/api/v1/db/test-connection` | JWT | Test DB connectivity |

## Default credentials (dev only)

| Username | Password | Role |
|----------|----------|------|
| admin | secret | admin |
| user | password | user |

> **Change these in production via environment variables or a real user store.**

## Configuration

All settings are read from environment variables (or a `.env` file).  See `.env.example` for the full list.

| Variable | Default | Description |
|----------|---------|-------------|
| `SECRET_KEY` | *(insecure default)* | JWT signing key |
| `AI_PROVIDER` | `mock` | `mock` or `openai` |
| `OPENAI_API_KEY` | – | Required when `AI_PROVIDER=openai` |
| `LOG_LEVEL` | `INFO` | `DEBUG`, `INFO`, `WARNING`, `ERROR` |

## Running Tests

```bash
pytest tests/ -v
```

## Linting

```bash
black app/ tests/
flake8 app/ tests/
isort app/ tests/
```

## Architecture

```
app/
├── main.py              # Application factory
├── config.py            # Pydantic-settings config
├── dependencies.py      # DI helpers (auth etc.)
├── api/v1/
│   ├── router.py        # Aggregated v1 router
│   └── endpoints/       # One module per feature
├── services/            # Business logic
├── repositories/        # Data-access layer
├── db/connectors/       # DB-specific connectors
├── models/              # Domain models
├── schemas/             # Pydantic request/response schemas
└── utils/               # Logging, security helpers
```

## Adding a New Database Connector

1. Create `app/db/connectors/<mydb>.py` implementing `BaseConnector`.
2. Register it in `app/db/connectors/__init__.py` (`_REGISTRY["mydb"] = MyDBConnector`).
3. Done – the DB playground will automatically support the new type.

## Adding a New AI Provider

1. Create a class inheriting from `AIService` in `app/services/ai_service.py`.
2. Update `get_ai_service()` to return your new class based on a config value.
services
