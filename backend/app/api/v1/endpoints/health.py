"""Health and liveness checks."""

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class HealthResponse(BaseModel):
    status: str = "ok"
    version: str
    database: str = "not_configured"
    cache: str = "not_configured"


@router.get("/health", response_model=HealthResponse, summary="Service health")
async def health_check() -> HealthResponse:
    """Return service liveness and dependency connectivity status."""
    return HealthResponse(version=__import__("app").__version__)
