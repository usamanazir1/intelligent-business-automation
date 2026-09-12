"""Dashboard aggregation endpoints."""

from fastapi import APIRouter

from pydantic import BaseModel

router = APIRouter()


class DashboardSummary(BaseModel):
    total_workflows: int
    active_automations: int
    tasks_completed_today: int
    success_rate_pct: float
    pending_approvals: int


@router.get(
    "/summary",
    response_model=DashboardSummary,
    summary="Aggregated dashboard KPIs",
)
async def dashboard_summary() -> DashboardSummary:
    """Return aggregated KPI figures.

    TODO: compute from the analytics service once data stores are wired.
    """
    return DashboardSummary(
        total_workflows=12,
        active_automations=7,
        tasks_completed_today=143,
        success_rate_pct=98.2,
        pending_approvals=3,
    )
