"""Workflow definition and execution endpoints."""

from uuid import UUID, uuid4

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

router = APIRouter()


class WorkflowStep(BaseModel):
    id: str
    action: str
    params: dict[str, object] = Field(default_factory=dict)


class WorkflowCreate(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    description: str | None = None
    trigger: str = "manual"
    steps: list[WorkflowStep] = Field(default_factory=list)


class Workflow(WorkflowCreate):
    id: UUID
    enabled: bool = True


class RunResponse(BaseModel):
    run_id: UUID
    workflow_id: UUID
    status: str = "queued"


# In-memory store — replace with a database-backed repository.
_WORKFLOWS: dict[UUID, Workflow] = {}


@router.get("", response_model=list[Workflow], summary="List workflows")
async def list_workflows() -> list[Workflow]:
    """Return all workflow definitions."""
    return list(_WORKFLOWS.values())


@router.post("", response_model=Workflow, status_code=status.HTTP_201_CREATED)
async def create_workflow(payload: WorkflowCreate) -> Workflow:
    """Persist a new workflow definition."""
    workflow = Workflow(id=uuid4(), **payload.model_dump())
    _WORKFLOWS[workflow.id] = workflow
    return workflow


@router.post("/{workflow_id}/run", response_model=RunResponse)
async def run_workflow(workflow_id: UUID) -> RunResponse:
    """Enqueue a workflow execution (manual trigger)."""
    if workflow_id not in _WORKFLOWS:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Workflow not found"
        )
    return RunResponse(run_id=uuid4(), workflow_id=workflow_id)
