# Architecture

This document describes the high-level architecture of the Intelligent
Business Automation & Management System (IBAM) and the design decisions that
drive it.

## Overview

IBAM is a **modular, API-first platform** built as a monorepo with two
top-level application components (`backend/` and `frontend/`) plus supporting
infrastructure. The system is designed so that heavy components (workflow
engine, scheduler, analytics) can later be extracted into standalone services
without re-architecting the API contract.

## System Context

```
                     ┌──────────────────────────────┐
                     │  Business Users (Web UI, API) │
                     └──────────────┬───────────────┘
                                    │ HTTPS / REST
                     ┌──────────────▼───────────────┐
                     │        Backend (FastAPI)     │
                     │  ┌────────┐ ┌──────────────┐ │
                     │  │ Auth   │ │ OpenAPI v1    │ │
                     │  └────▲───┘ └──────┬───────┘ │
                     │       │            │         │
                     │  ┌────┴────────────▼───────┐ │
                     │  │ Domain Services          │ │
                     │  │ Workflow · Automation ·  │ │
                     │  │ Insights · Tasks         │ │
                     │  └────────────┬─────────────┘ │
                     └───────────────┼───────────────┘
                                     │
              ┌──────────────────────┼──────────────────────┐
              │                      │                      │
        ┌─────▼────┐         ┌───────▼────┐        ┌────────▼────┐
        │PostgreSQL│         │   Redis    │        │  Storage/   │
        │ (source) │         │(queue/cache)│       │object store │
        └──────────┘         └────────────┘        └─────────────┘
```

## Backend

### Layering

The backend follows a **dependency-inverted layered architecture**:

```
app/
├── api/       → HTTP layer: routers, FastAPI dependencies
│   └── v1/    → Versioned endpoints
├── core/      → Cross-cutting configuration, security, utilities
├── models/    → SQLAlchemy ORM entities (persistence contract)
├── schemas/   → Pydantic DTOs (API contract)
```

Rules:

- **API endpoints** must not contain business logic; they delegate to domain
  services (added per milestone).
- **Schemas** are the only thing crossing the HTTP boundary.
- **Models** are the only thing crossing the database boundary.
- External systems (email, CRM, webhooks) are reached through thin connector
  adapters isolated behind the integration layer.

### Domain Services (planned)

| Service        | Responsibility                                                    |
| -------------- | ----------------------------------------------------------------- |
| Workflow Engine| Executes directed step graphs; supports retries, timeouts, rollback |
| Scheduler      | Cron + event triggers; dispatches to the workflow engine via queue |
| Insights       | Aggregates KPIs; detects anomalies & bottlenecks in processes       |
| Tasks          | Manages to-do queues, assignments, approvals                       |
| Audit          | Append-only event log for governance & compliance                  |

### Database Model

Canonical entities (full migration set to be generated via Alembic):

- `users` — credentials, roles, department
- `workflows` — definitions: steps as JSON, trigger type
- `workflow_runs` — executions, status, timing, logs
- `automations` — rules linking events/cron to workflows
- `tasks` — human-in-the-loop assignments and approvals
- `audit_events` — immutable records of automated actions

## Frontend

- Single-page application built with **React 18 + TypeScript + Vite**.
- UI primitives from **Ant Design**; routing via `react-router`.
- Talks to the backend through a **typed API client** (`src/api/client.ts`)
  that attaches the JWT automatically and redirects to `/login` on 401.
- Uses build-time proxy in dev and Nginx path-based proxy in production, so
  the frontend never needs to know the backend hostname.

## Cross-Cutting Concerns

### Security

- JWT (HS256) with short-lived access tokens; password hashing with bcrypt.
- Strict RBAC enforced both at the API layer (dependencies) and UI (route
  guards) — never trust the client.
- Secrets arrive exclusively via environment variables; `.env` is git-ignored.

### Observability (roadmap)

- Structured JSON logs via `structlog`.
- Prometheus `/metrics` endpoint and OpenTelemetry tracing hooks.
- Sentry integration for error tracking in the frontend and backend.

### Configuration

- Single source of truth in `backend/app/core/config.py` (Pydantic Settings),
  overridable through environment variables documented in `.env.example`.

## Deployment Topology

```
┌─────────┐     ┌─────────┐     ┌─────────┐     ┌─────────┐
│ Nginx   │────▶│ Frontend│────▶│ Backend │────▶│Postgres/│
│ (TLS,   │     │  SPA    │     │ API     │     │  Redis  │
│  origin)│     └─────────┘     └─────────┘     └─────────┘
└─────────┘
```

All four containers are defined in `docker-compose.yml`. The API layer is
stateless by design, so it can be scaled horizontally behind a load balancer
with Redis used for distributed sessions/queues.