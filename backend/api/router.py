"""Aggregates all API route modules into a single router."""

from fastapi import APIRouter

from backend.api.routes import analyze, health, root

api_router = APIRouter()
api_router.include_router(root.router)
api_router.include_router(health.router)
api_router.include_router(analyze.router)
