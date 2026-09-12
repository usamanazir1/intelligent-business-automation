# API Reference

The backend exposes a **versioned REST API** under `/api/v1`. The interactive
Swagger UI is available at `/docs` when the server is running, and the raw
OpenAPI schema at `/openapi.json`.

- Base URL (local): `http://localhost:8000/api/v1`
- Authentication: `Authorization: Bearer <access_token>`
- Content-Type: `application/json`

## Conventions

- All timestamps are UTC, ISO-8601.
- IDs are UUIDs for public resources.
- Errors follow RFC 7807-style objects:

  ```json
  {
    "detail": "Workflow not found"
  }
  ```

- Pagination (when enabled) uses `?page=1&page_size=50` and returns
  `{ "items": [...], "total": N }`.

## Authentication

| Method | Endpoint             | Description                              |
| ------ | -------------------- | ---------------------------------------- |
| POST   | `/auth/login`        | OAuth2 password form → JWT access token  |
| GET    | `/auth/users/me`     | Profile of the authenticated user        |

### `POST /auth/login`

Request body (form-urlencoded):

| Field      | Type   | Description        |
| ---------- | ------ | ------------------ |
| `username` | string | Account username   |
| `password` | string | Account password   |

Response `200`:

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

> Demo account: `admin` / `admin`.

## Health

### `GET /health`

Returns liveness and dependency status. Used by orchestrators and load
balancers.

```json
{
  "status": "ok",
  "version": "0.1.0",
  "database": "not_configured",
  "cache": "not_configured"
}
```

## Dashboard

### `GET /dashboard/summary`

Returns aggregated KPI figures for the operational overview.

```json
{
  "total_workflows": 12,
  "active_automations": 7,
  "tasks_completed_today": 143,
  "success_rate_pct": 98.2,
  "pending_approvals": 3
}
```

## Workflows

### `GET /workflows`

Lists all workflow definitions.

### `POST /workflows`

Creates a workflow definition.

Request:

```json
{
  "name": "Invoice processing",
  "description": "Extract fields, validate, and route invoices",
  "trigger": "scheduled",
  "steps": [
    { "id": "extract", "action": "extract_fields", "params": { "source": "email" } },
    { "id": "validate", "action": "validate", "params": {} }
  ]
}
```

Response `201`: the created workflow including its `id` (UUID) and `enabled`.

### `POST /workflows/{id}/run`

Enqueues a manual run of a workflow.

Response `200`:

```json
{
  "run_id": "3f2e...",
  "workflow_id": "a1b2...",
  "status": "queued"
}
```

### Error responses

| Status | Meaning                                    |
| ------ | ------------------------------------------ |
| 401    | Missing/invalid bearer token              |
| 404    | Referenced resource does not exist        |
| 422    | Request body failed validation            |

## Automations

### `GET /automations`

Lists all automation rules.

### `POST /automations`

Request:

```json
{
  "name": "Nightly invoice sync",
  "event_type": "scheduled",
  "cron": "0 2 * * *",
  "workflow_id": "a1b2c3d4-...",
  "enabled": true
}
```

### `DELETE /automations/{id}`

Deletes an automation rule. Returns `204` on success.

## Versioning & Breaking Changes

- Additive changes (new endpoints, optional fields) are **non-breaking** and
  released in any minor/patch version.
- Breaking changes bump the API major version and introduce a new prefix
  (e.g. `/api/v2`). The previous version remains available for at least one
  release cycle to allow migration.