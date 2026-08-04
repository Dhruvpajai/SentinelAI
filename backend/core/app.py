"""
FastAPI application factory.

Creates and configures the FastAPI instance with middleware, routes, and lifecycle hooks.
"""

import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api.router import api_router
from backend.core.config import Settings, get_settings
from backend.core.logging import setup_logging

logger = logging.getLogger(__name__)


def create_app(settings: Settings | None = None) -> FastAPI:
    """
    Build and return a configured FastAPI application.

    Args:
        settings: Optional settings override (useful for testing).

    Returns:
        Configured FastAPI application instance.
    """
    settings = settings or get_settings()
    setup_logging(settings)

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        logger.info("%s started (env=%s)", settings.app_name, settings.app_env)
        yield
        logger.info("%s shutting down", settings.app_name)

    app = FastAPI(
        title=settings.app_name,
        description="AI security middleware for prompt and response protection.",
        version="0.1.0",
        debug=settings.debug,
        lifespan=lifespan,
    )

    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Register API routes
    app.include_router(api_router)

    return app
