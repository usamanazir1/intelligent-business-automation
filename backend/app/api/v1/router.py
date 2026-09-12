"""Aggregation of v1 endpoint routers."""

from fastapi import APIRouter

from app.api.v1.endpoints import auth, automations, dashboard, health, workflows

api_router = APIRouter()

api_router.include_router(health.router, tags=["health"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])
api_router.include_router(workflows.router, prefix="/workflows", tags=["workflows"])
api_router.include_router(
    automations.router, prefix="/automations", tags=["automations"]
)
