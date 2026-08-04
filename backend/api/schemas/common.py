"""Shared API response schemas."""

from pydantic import BaseModel, Field


class StatusResponse(BaseModel):
    """Standard status response payload."""

    status: str = Field(..., description="Human-readable status message")
