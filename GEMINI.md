# Integration Workspace — AI Agent Instructions

Read and obey these files in order:

1. `~/.gemini/GEMINI.md` — global engineering rules.
2. Parent `../GEMINI.md` — ecosystem-level boundaries.
3. Parent `../AGENTS.md` — workspace agent orchestration.
4. This file — repository-specific rules.
5. `.specify/memory/constitution.md` — project constitution.
6. Active `specs/<version>/spec.md`, `plan.md`, `tasks.md`.

## Repository Scope

This repository owns **cross-service orchestration** only:

- Architecture diagrams and design decisions.
- Provider API contract (versioned OpenAPI or JSON schema).
- Docker Compose orchestration (`compose.yaml`, `.env.example`).
- Environment configuration conventions.
- Local-development and release-process documentation.
- Integration-level validation and contract tests.

## Prohibited Content

Do NOT place in this repository:

- FastAPI application or business logic (belongs in `unified-finance-integration-api`).
- Flask provider simulator logic (belongs in `sage-provider-simulator`).
- Service-specific unit tests (belong in their respective repositories).
- Real API keys, tokens, passwords, or provider credentials.
- Production deployment manifests or cloud infrastructure.

## Cross-Service API Contract Workflow

1. Update the contract in this repository first.
2. Update affected repository specifications.
3. Add or update contract tests.
4. Implement changes through linked feature branches.
5. Verify the full Compose flow before merge/release.

## Naming and Honesty

- The provider simulator is a **local portfolio simulator**, not an official Sage API.
- Never describe mocks, fixtures, or simulators as production integrations.
- Never fabricate test results, deployments, CI outcomes, or releases.

## Git Workflow

- Follow strict Gitflow: `main`, `develop`, `feature/*`, `release/*`, `hotfix/*`.
- Use Conventional Commits: `docs:`, `feat:`, `fix:`, `chore:`, `ci:`, `test:`.
- Never commit directly to `main` or `develop`.
- All changes go through Pull Requests with review.
