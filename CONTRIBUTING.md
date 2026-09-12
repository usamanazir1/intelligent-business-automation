# Contributing to Intelligent Business Automation & Management System

First off, thank you for taking the time to contribute! The following document outlines the expectations and process for contributing to this project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Workflow](#development-workflow)
- [Coding Standards](#coding-standards)
- [Commit Message Guidelines](#commit-message-guidelines)
- [Style Guides](#style-guides)
- [Project Governance](#project-governance)

## Code of Conduct

This project and everyone participating in it is governed by the [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code. Please report unacceptable behavior to the project maintainers.

## How Can I Contribute?

### Reporting Bugs

Before creating a bug report, please:

1. Search the [issue tracker](https://github.com/your-org/intelligent-business-automation/issues) and open/closed issues to avoid duplicates.
2. Gather as much information as possible: browser/OS versions, steps to reproduce, expected vs. actual behavior, and relevant logs.

**Do not report security vulnerabilities in public issues** — see [SECURITY.md](SECURITY.md).

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating one, explain **why** this feature matters and describe the expected behavior, and, if possible, provide a mockup or a rough technical sketch.

### Your First Code Contribution

Unsure where to begin? Look for issues labeled `good first issue` or `help wanted`. They are intentionally scoped to be approachable.

## Development Workflow

1. **Fork** the repository and create a feature branch from `main`:

   ```bash
   git checkout -b feat/my-feature main
   ```

2. **Set up your local environment** following the instructions in the [README](README.md#getting-started).

3. **Make your changes**, keeping each logical change in a separate commit.

4. **Write tests** for every new behavior. Bug fixes should include a regression test that fails without the fix.

5. **Run the full check suite** locally before pushing (see [Coding Standards](#coding-standards)).

6. **Open a pull request** against `main` using the provided [pull request template](.github/PULL_REQUEST_TEMPLATE.md). Fill in every section — a PR that does not describe the change will be sent back.

### Pull Request Checklist

- [ ] Branch is rebased onto the latest `main`.
- [ ] Tests pass (`pytest` for backend, `npm run test` for frontend).
- [ ] Lint and type checks pass (ruff, mypy, eslint, tsc).
- [ ] New endpoints are documented and covered by tests.
- [ ] Changes are covered by a regression test where applicable.
- [ ] Update `docs/` if behavior is user-visible.
- [ ] No secrets or `.env` files were committed.

## Coding Standards

### Backend (Python)

```bash
cd backend
pip install -r requirements-dev.txt
ruff check app tests          # lint
ruff format --check app tests # formatting
mypy app                      # type checking
pytest --cov=app              # tests + coverage (target >= 80%)
```

- Python 3.11+ only.
- Type hints are mandatory; all public functions must be annotated.
- Follow PEP 8 via `ruff` and use `ruff format` for style.
- Keep functions small and focused; favor composition over inheritance.
- Use Pydantic v2 schemas for all API payloads; never trust raw dicts.

### Frontend (TypeScript / React)

```bash
cd frontend
npm install
npm run lint        # eslint
npm run typecheck   # tsc --noEmit
npm run test        # vitest
```

- Prefer typed components; avoid `any` unless genuinely unavoidable.
- Functional components with hooks only (no class components).
- Follow the existing folder structure (`pages/`, `components/`, `api/`).

### Formatting

Both subsystems use automatic formatters. Run them before committing:

- Backend: `ruff format app tests`
- Frontend: `npx prettier --write src`

## Commit Message Guidelines

We follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`, `revert`.

Examples:

```
feat(workflows): add scheduling trigger for cron workflows
fix(auth): validate refresh token issuer to prevent replay
docs(api): document webhook delivery retry behavior
```

Keep the first line under 72 characters. Reference issue numbers in the footer (`Closes #42`).

## Style Guides

- **Markdown documentation**: LATFM — "look at the files we already have". Match tone and formatting of `README.md` and `docs/`.
- **Docker images**: always pin base image minor versions and use multi-stage builds. Do not run containers as `root` unless strictly necessary.

## Project Governance

- `main` is the only released branch; it must remain green (CI enforced).
- Two approving reviews are required to merge feature PRs.
- Trivial, maintenance-only changes (docs, typo fixes, dependency bumps) may be merged with a single review.
- Significant API changes require an update to `docs/api.md` within the same PR.

Questions? Reach out via a GitHub Discussion. Happy contributing!