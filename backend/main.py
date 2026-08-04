"""
SentinelAI FastAPI application entry point.

Run with:
    uvicorn backend.main:app --reload
"""

from backend.core.app import create_app

app = create_app()
