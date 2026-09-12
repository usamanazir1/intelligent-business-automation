# Intelligent Business Automation & Management System

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18-61DAFB.svg)](https://react.dev/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5-3178C6.svg)](https://www.typescriptlang.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A modern, cloud-native platform that helps organizations **automate repetitive business processes**, **manage workflows**, and **gain real-time operational intelligence** through a unified dashboard. Think of it as a lightweight, self-hosted alternative to enterprise RPA + BPM suites.

## Table of Contents

- [Features](#features)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Getting Started](#getting-started)
- [Project Structure](#project-structure)
- [API Documentation](#api-documentation)
- [Testing](#testing)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Workflow Automation Engine** — Design, schedule, and execute rule-based and event-driven business workflows.
- **Intelligent Insights Dashboard** — Real-time KPIs, process throughput, bottleneck detection, and trend analysis.
- **Task & Queue Management** — Prioritize, assign, and track tasks across teams with status transparency.
- **Document & Data Pipelines** — Automate ingestion, transformation, and routing of structured and unstructured data.
- **Role-Based Access Control (RBAC)** — Fine-grained permissions for users, departments, and automation scopes.
- **Audit Logging** — Full traceability of every automated action for compliance and governance.
- **Modular Integration** — Pluggable connectors for email, CRMs, ERPs, and webhooks (REST-first).
- **Self-Hosted & Containerized** — Deploy on-premises or in the cloud with Docker out of the box.

> **Status:** This repository is a professional project skeleton. Core scaffolding, CI/CD, and documentation are included; modules listed above are incrementally implemented behind a versioned REST API.

## Architecture

The system uses a **clean, layered microservices-ready architecture**:

```
┌──────────────────────────── Antd · React · TypeScript ───────────────────────────┐
│                              Frontend (SPA)                                      │
└────────────────────────────────────┬────────────────────────────────────────────┘
                                     │  HTTPS / REST (JSON)
┌────────────────────────────────────▼────────────────────────────────────────────┐
│                          API Gateway / BFF                                      │
│                    FastAPI · OpenAPI · JWT Auth                                 │
├──────────────────────────────────────────────────────────────────────────────────┤
│  Workflow Engine    │  Automation Scheduler   │  Dashboard/Analytics            │
│  Rule Evaluator     │  Task & Queue Mgmt      │  Insights & Reporting           │
└────────────────────────────────────┬────────────────────────────────────────────┘
                                     │  SQLAlchemy ORM
                           ┌─────────▼─────────┬──────────────┐
                           │   PostgreSQL      │   Redis      │
                           │  (primary store)  │  (queues/cache) │
                           └───────────────────┴──────────────┘
```

See [docs/architecture.md](docs/architecture.md) for the detailed design.

## Tech Stack

| Layer   | Technology                                                  |
| ------- | ----------------------------------------------------------- |
| Backend | Python 3.11+, FastAPI, Pydantic v2, SQLAlchemy 2.x, Alembic |
| Frontend| React 18, TypeScript, Vite, Ant Design                      |
| Data    | PostgreSQL 16, Redis 7                                      |
| Auth    | JWT (OAuth2 Password flow), role-based access control       |
| Ops     | Docker, Docker Compose, GitHub Actions CI/CD                |
| Tests   | pytest, pytest-cov, httpx (backend) · Vitest (frontend)     |

## Getting Started

### Prerequisites

- Python 3.11+
- Node.js 18+ and npm
- Docker & Docker Compose (optional, for containerized setup)

### 1. Clone the Repository

```bash
git clone https://github.com/your-org/intelligent-business-automation.git
cd intelligent-business-automation
```

### 2. Run the Backend

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate          # Windows
source .venv/bin/activate       # macOS / Linux
pip install -r requirements-dev.txt
cp .env.example .env            # then edit as needed
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`, with interactive docs at `http://localhost:8000/docs`.

### 3. Run the Frontend

```bash
cd frontend
npm install
cp .env.example .env.local      # set VITE_API_BASE_URL
npm run dev
```

The app will be available at `http://localhost:5173`.

### 4. Run Everything with Docker (recommended)

```bash
docker compose up --build
```

- Frontend: `http://localhost:3000`
- Backend API: `http://localhost:8000`
- API Docs: `http://localhost:8000/docs`
- PostgreSQL: `localhost:5432`
- Redis: `localhost:6379`

## Project Structure

```
.
├── backend/                  # FastAPI application
│   ├── app/
│   │   ├── api/              # Versioned REST API endpoints
│   │   ├── core/             # Configuration, security, dependencies
│   │   ├── models/           # SQLAlchemy ORM models
│   │   ├── schemas/          # Pydantic request/response models
│   │   └── main.py           # Application entrypoint
│   ├── tests/                # pytest test suite
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/                 # React + TypeScript SPA
│   ├── src/
│   │   ├── api/              # Typed API client
│   │   ├── components/       # Reusable UI components
│   │   ├── pages/            # Route-level views
│   │   └── ...
│   └── Dockerfile
├── docs/                     # Architecture, API, and deployment docs
├── .github/                  # CI/CD workflows and community templates
├── docker-compose.yml        # Local full-stack environment
└── ...
```

See [docs/architecture.md](docs/architecture.md) for a full breakdown.

## API Documentation

The backend exposes a self-documenting OpenAPI/Swagger interface at `http://localhost:8000/docs` (JSON schema at `/openapi.json`).

Key versioned endpoints live under `/api/v1`:

| Method | Endpoint                        | Description                       |
| ------ | ------------------------------- | --------------------------------- |
| GET    | `/api/v1/health`                | Liveness & dependency checks      |
| POST   | `/api/v1/auth/login`            | Obtain a JWT access token         |
| GET    | `/api/v1/users/me`              | Current authenticated user        |
| GET    | `/api/v1/dashboard/summary`     | Aggregated KPI dashboard data     |
| GET    | `/api/v1/workflows`             | List workflow definitions         |
| POST   | `/api/v1/workflows`             | Create a workflow definition      |
| POST   | `/api/v1/workflows/{id}/run`    | Trigger a workflow execution      |
| POST   | `/api/v1/automations`           | Create an automation rule         |

Refer to [docs/api.md](docs/api.md) and the in-browser Swagger UI for complete contracts.

## Testing

```bash
# Backend (pytest + coverage)
cd backend
pytest --cov=app --cov-report=term-missing

# Frontend (Vitest)
cd frontend
npm run test
```

## Deployment

Production build and deployment instructions — including reverse proxy setup (Nginx), TLS, managed PostgreSQL, and horizontal scaling of the stateless API layer — are documented in [docs/deployment.md](docs/deployment.md).

The `main` branch is continuously validated by GitHub Actions CI and publishes container images on tagged releases.

## Contributing

Contributions are welcome! Please read our [Contributing Guidelines](CONTRIBUTING.md), follow the [Code of Conduct](CODE_OF_CONDUCT.md), and review the [Security Policy](SECURITY.md) before submitting changes.

## Roadmap

- [ ] Workflow designer UI (visual drag-and-drop builder)
- [ ] Integration marketplace (email, Slack, CRM connectors)
- [ ] ML-assisted process anomaly detection
- [ ] Multi-tenant support with isolated namespaces
- [ ] Native mobile notifications

Suggestions and feature requests are tracked via [GitHub Issues](https://github.com/your-org/intelligent-business-automation/issues).

## License

This project is licensed under the [MIT License](LICENSE).