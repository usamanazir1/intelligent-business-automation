# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| latest  | :white_check_mark: |
| older   | :x:                |

We currently maintain a single, continuously released line. Security fixes land on the latest release and are immediately back-ported to Docker images tagged with `latest`.

## Reporting a Vulnerability

Please **do not** open a public GitHub issue for security-sensitive reports.

Instead, contact the maintainers privately via email at **security@example.com** (replace with your real address before publishing this repository). You can expect:

1. **Acknowledgement** within 48 hours of a confirmed report.
2. A **detailed assessment** and remediation timeline within 7 days.
3. Coordination on a coordinated disclosure date before any public patch release.

If you believe the issue is critical (remote code execution, authentication bypass, or data exfiltration), please clearly mark it as **CRITICAL** in the subject line.

## Scope

Included in scope:

- The FastAPI backend in `backend/` and its dependencies.
- The React frontend in `frontend/` and its dependencies.
- Docker images, compose files, and CI/CD workflows in this repository.

Out of scope:

- Third-party, publicly disclosed CVEs in dependencies — please report those upstream.

## Security Best Practices We Follow

- Secrets are never stored in the repository or committed to version control.
- JWT access tokens are short-lived; refresh tokens are stored hashed.
- All passwords are hashed with bcrypt (or Argon2id on configured deployments).
- Row-level authorization is enforced in the API layer, not just the UI.
- Dependency upgrades and automated secret scanning run in CI on every pull request.