"""Root endpoint."""

from fastapi import APIRouter

from backend.api.schemas.common import StatusResponse

router = APIRouter(tags=["Root"])


@router.get("/", response_model=StatusResponse, summary="Service status")
async def get_root() -> StatusResponse:
    """Return a simple status message indicating the service is running."""
    return StatusResponse(status="SentinelAI Running")
