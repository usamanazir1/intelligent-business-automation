"""Workflow and automation schemas."""

from uuid import UUID

from pydantic import BaseModel, Field


class WorkflowStep(BaseModel):
    id: str
    action: str
    params: dict[str, object] = Field(default_factory=dict)


class WorkflowCreate(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    description: str | None = None
    trigger: str = "manual"
    steps: list[WorkflowStep] = Field(default_factory=list)


class WorkflowRead(WorkflowCreate):
    id: UUID
    enabled: bool = True

    model_config = {"from_attributes": True}


class WorkflowRun(BaseModel):
    workflow_id: UUID
    inputs: dict[str, object] = Field(default_factory=dict)


class AutomationCreate(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    event_type: str = "scheduled"
    cron: str | None = None
    workflow_id: UUID
    enabled: bool = True


class AutomationRead(AutomationCreate):
    id: UUID

    model_config = {"from_attributes": True}
