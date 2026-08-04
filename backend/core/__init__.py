"""Core application infrastructure: configuration, logging, and app factory."""

from backend.core.app import create_app
from backend.core.config import get_settings

__all__ = ["create_app", "get_settings"]
