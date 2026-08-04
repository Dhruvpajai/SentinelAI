"""Health check endpoint."""

from fastapi import APIRouter

from backend.api.schemas.common import StatusResponse

router = APIRouter(tags=["Health"])


@router.post("/health", response_model=StatusResponse, summary="Health check")
async def health_check() -> StatusResponse:
    """Return service health status."""
    return StatusResponse(status="healthy")
