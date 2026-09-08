# Project Constitution — Unified Finance Integration

Version: 0.1.0
Status: Active
Last Updated: 2026-09-08

## Purpose

This constitution defines non-negotiable principles for the Unified Finance
Integration ecosystem. All agents, specifications, plans, and implementations
must comply with these rules.

## Ecosystem Overview

The ecosystem consists of three Git repositories:

| Repository | Technology | Responsibility |
|---|---|---|
| `integration-workspace` | Compose, contracts, docs | Cross-service orchestration, API contracts, architecture, environment config, integration validation |
| `unified-finance-integration-api` | FastAPI, MySQL | Unified API endpoints, sync orchestration, invoice normalization, persistence, Swagger, dashboard |
| `sage-provider-simulator` | Flask | Deterministic provider simulation, fixture invoices, X-API-Key auth, pagination, error scenarios, demo UI |

## Non-Negotiable Principles

### INV-001: Service Boundary Enforcement

Each repository owns its own application logic. The integration workspace
must not contain FastAPI or Flask business logic.

### INV-002: Contract-First Integration

Cross-service API changes must follow the contract workflow:
contract update → spec update → contract tests → linked feature branches → Compose verification.

### INV-003: Honest Naming

The provider simulator is a **local portfolio simulator**. It must never be
described as an official Sage API, production integration, or real provider.

### INV-004: No Secrets in Git

No API keys, tokens, passwords, private URLs, or personal data may be committed.
Use `.env.example` with placeholder values and `.gitignore` for secret files.

### INV-005: Spec-Driven Development

No non-trivial feature may be implemented without an approved specification
(`spec.md`), implementation plan (`plan.md`), task list (`tasks.md`),
acceptance criteria, and explicit out-of-scope items.

### INV-006: Gitflow Discipline

- `main` = release-ready code only.
- `develop` = integration branch.
- `feature/*` = branch from and merge into `develop`.
- `release/*` = branch from `develop`, merge into `main` and `develop`.
- `hotfix/*` = branch from `main` for real post-release defects only.
- Never commit directly to `main` or `develop`.
- All changes go through Pull Requests.

### INV-007: Conventional Commits

All commit messages follow: `<type>(<scope>): <description>`.
Types: `docs`, `feat`, `fix`, `refactor`, `test`, `build`, `ci`, `chore`.

### INV-008: No Fabrication

Never fabricate features, integrations, deployments, measurements, test results,
CI outcomes, releases, work experience, credentials, or production readiness.

### INV-009: Reproducible Local Startup

A new developer must be able to run the entire ecosystem from a clean clone
using documented commands. All setup steps must be explicit in README.

### INV-010: Incremental Delivery

- P0 = complete core value flow (end-to-end invoice sync demo).
- P1 = reliability and usability improvements.
- P2 = optional scalability, advanced infrastructure, or monitoring.
- Do not start P1/P2 while P0 is incomplete or failing.

### INV-011: Test-First for Critical Behavior

Apply TDD (red → green → refactor) to: validation, data transformations,
authentication, API contracts, pagination, state transitions, retries,
error handling, and idempotency — in service repositories.

### INV-012: KISS and YAGNI

No unnecessary dependencies, services, frameworks, abstractions,
infrastructure, or features. Build only what is needed for current acceptance
criteria.

### INV-013: English for Technical Artifacts

All code, identifiers, commit messages, API documentation, README, and
technical project documentation must be in English.

### INV-014: CI as Gate

CI is mandatory. Linting, tests, and build must pass before merge.
A feature is not complete while CI is failing.

### INV-015: Data Integrity

Preserve data integrity using input validation, unique constraints, and
idempotency where relevant. Every external HTTP call must have an explicit
timeout, error handling, and useful logs.

## Traceability

Every requirement (FR-xxx) and invariant (INV-xxx) must trace through:
specification → plan → tasks → tests → contract.
