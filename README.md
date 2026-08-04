# SentinelAI

AI security middleware that detects and blocks malicious prompts before they reach an LLM, and analyzes responses to prevent sensitive information leakage.

## Milestone 1 — Backend Foundation

This milestone provides a production-ready FastAPI backend with configuration, logging, CORS, and SQLAlchemy setup (no models yet).

## Project Structure

```
SentinelAI/
├── backend/
│   ├── api/           # HTTP routes and Pydantic schemas
│   ├── core/          # App factory, config, logging
│   ├── database/      # SQLAlchemy engine and session
│   ├── firewall/      # (future) Prompt/response firewall
│   ├── llm/           # (future) LLM adapter
│   ├── models/        # (future) ORM models
│   ├── services/      # (future) Business logic
│   └── utils/         # Shared helpers
├── tests/
├── logs/
├── frontend/          # (future) Streamlit dashboard
├── training/          # (future) Model training scripts
├── datasets/          # (future) Training data
├── requirements.txt
└── README.md
```

## Prerequisites

- Python 3.10 or higher
- pip

## Setup

1. **Clone the repository** (or navigate to the project directory):

   ```bash
   cd SentinelAI
   ```

2. **Create and activate a virtual environment**:

   ```bash
   python -m venv venv

   # Windows
   venv\Scripts\activate

   # macOS / Linux
   source venv/bin/activate
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**:

   ```bash
   copy .env.example .env   # Windows
   cp .env.example .env     # macOS / Linux
   ```

   Edit `.env` as needed. Defaults work for local development.

## Running the Server

From the project root:

```bash
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at [http://localhost:8000](http://localhost:8000).

Interactive API docs: [http://localhost:8000/docs](http://localhost:8000/docs)

## API Endpoints

| Method | Path     | Response                          |
|--------|----------|-----------------------------------|
| GET    | `/`      | `{"status": "SentinelAI Running"}` |
| POST   | `/health`| `{"status": "healthy"}`            |

### Examples

```bash
curl http://localhost:8000/

curl -X POST http://localhost:8000/health
```

## Configuration

All settings are loaded from environment variables or `.env`:

| Variable        | Default                                      | Description                    |
|-----------------|----------------------------------------------|--------------------------------|
| `APP_NAME`      | `SentinelAI`                                 | Application name               |
| `APP_ENV`       | `development`                                | Environment                    |
| `DEBUG`         | `false`                                      | SQL echo and debug mode        |
| `HOST`          | `0.0.0.0`                                    | Server bind host               |
| `PORT`          | `8000`                                       | Server bind port               |
| `CORS_ORIGINS`  | `http://localhost:3000,http://localhost:8501`| Allowed CORS origins           |
| `DATABASE_URL`  | `sqlite:///./sentinelai.db`                  | SQLAlchemy connection URL      |
| `LOG_LEVEL`     | `INFO`                                       | Logging level                  |
| `LOG_DIR`       | `logs`                                       | Log file directory             |

## Logging

Logs are written to:

- **Console** — stdout
- **File** — `logs/sentinelai.log` (rotating, 5 MB max, 5 backups)

## License

Proprietary — SentinelAI
