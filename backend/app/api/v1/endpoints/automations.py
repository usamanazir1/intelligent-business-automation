"""Automation rule endpoints.

Automations represent event-driven or scheduled rules that trigger
workflows, e.g. "when invoice reception emails arrive, run the
invoice-processing workflow".
"""

from uuid import UUID, uuid4

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

router = APIRouter()


class AutomationCreate(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    event_type: str = "scheduled"
    cron: str | None = None
    workflow_id: UUID
    enabled: bool = True


class Automation(AutomationCreate):
    id: UUID


_AUTOMATIONS: dict[UUID, Automation] = {}


@router.get("", response_model=list[Automation], summary="List automations")
async def list_automations() -> list[Automation]:
    """Return all automation rules."""
    return list(_AUTOMATIONS.values())


@router.post("", response_model=Automation, status_code=status.HTTP_201_CREATED)
async def create_automation(payload: AutomationCreate) -> Automation:
    """Persist a new automation rule."""
    automation = Automation(id=uuid4(), **payload.model_dump())
    _AUTOMATIONS[automation.id] = automation
    return automation


@router.delete("/{automation_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_automation(automation_id: UUID) -> None:
    """Delete an automation rule."""
    if automation_id not in _AUTOMATIONS:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Automation not found"
        )
    del _AUTOMATIONS[automation_id]
