# Deployment

This guide covers deploying the Intelligent Business Automation & Management
System for production. It assumes a Linux host (or cluster) with Docker and
Docker Compose available.

## 1. Prerequisites

- Docker Engine **24+** and Docker Compose **v2**.
- A domain name with DNS pointing at your host (for TLS).
- A reverse proxy capable of TLS termination (examples use Caddy/Nginx).

## 2. Configuration

All runtime configuration happens through environment variables — **nothing is
hard-coded and nothing is committed**.

| Variable       | Component | Purpose                                   | Default            |
| -------------- | --------- | ----------------------------------------- | ------------------ |
| `SECRET_KEY`   | backend   | JWT signing secret (generate with ``openssl rand -hex 32``) | `dev-only-...` |
| `DATABASE_URL` | backend   | PostgreSQL connection string              | local dev target   |
| `REDIS_URL`    | backend   | Redis connection string                   | local dev target   |
| `CORS_ORIGINS` | backend   | Comma-separated allowed origins           | localhost dev urls |

Prepare your environment file from the template:

```bash
cp .env.example .env
# edit .env — especially SECRET_KEY — then:
```

## 3. Docker Compose (single host)

```bash
docker compose up --build -d
docker compose ps
```

What you get:

| Service  | Container   | Ports            |
| -------- | ----------- | ---------------- |
| Frontend | `ibam-frontend` | `3000:80`    |
| Backend  | `ibam-backend`  | `8000:8000` |
| Database | `ibam-db`       | `5432` (local) |
| Cache    | `ibam-redis`    | `6379` (local) |

Because the frontend Nginx proxies `/api/` to the backend, only port **3000**
needs to be reachable from the internet.

## 4. TLS Termination

Terminate TLS at an edge reverse proxy. Example with Nginx:

```nginx
server {
    listen 443 ssl http2;
    server_name automation.example.com;

    ssl_certificate     /etc/letsencrypt/live/automation.example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/automation.example.com/privkey.pem;

    location / {
        proxy_pass http://127.0.0.1:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
server {
    listen 80;
    server_name automation.example.com;
    return 301 https://$host$request_uri;
}
```

Update `CORS_ORIGINS` to your real origin and re-deploy after changing `.env`.

## 5. Hardening Checklist

- [ ] `SECRET_KEY` is a fresh random value, not the default.
- [ ] PostgreSQL credentials are strong and restricted to the API user.
- [ ] Database port `5432` is not exposed to the internet (bind `127.0.0.1`).
- [ ] Redis bound to the Docker network only; `requirepass` set if exposed.
- [ ] Container runs as the non-root `appuser` (already configured).
- [ ] Backup policy in place for the `postgres_data` volume (`pg_dump`).
- [ ] Log rotation configured for container logs.

## 6. Upgrades

1. Pull the latest images / rebuild: `docker compose build --pull`
2. Run database migrations (once Alembic is wired): `docker compose exec backend alembic upgrade head`
3. Rolling restart: `docker compose up -d`

Images are published to GHCR from the `v*` tags. Pin deployments to an exact
image tag; avoid floating `latest` in production.

## 7. Backup & Restore

PostgreSQL:

```bash
docker compose exec db pg_dump -U postgres ibam -F c -f /tmp/ibam.dump
docker compose cp db:/tmp/ibam.dump ./backup-$(date +%F).dump
```

Redis (as configured): append-only file lives on the `redis_data` volume;
include it in periodic volume snapshots.

## 8. Horizontal Scaling (multi-instance)

The API layer is stateless. To scale:

- Run the backend behind a load balancer with a shared PostgreSQL and Redis.
- Ensure Redis is shared (it holds distributed queues/session state).
- Keep the frontend as static assets served by any CDN/Nginx.
- Scale workers via a container scheduler (Kubernetes, Docker Swarm, ECS).

## 9. Monitoring (roadmap)

Configure probes and dashboards after release:

- **Health probe:** `GET /api/v1/health` (already implemented).
- **Metrics:** Prometheus exporter endpoint (planned).
- **Logs:** structured JSON logging consumed by Loki/ELK.

Let's Encrypt `--dry-run` is recommended on first setup to validate domain
propagation before enabling 443 redirects.