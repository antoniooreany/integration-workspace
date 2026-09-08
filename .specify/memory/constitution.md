# Project Constitution — Unified Finance Integration

Version: 0.2.0
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
| `integration-workspace` | Compose, contracts, docs | Architecture decisions, canonical system contracts, roadmap, cross-service acceptance criteria, environment config, integration validation |
| `unified-finance-integration-api` | FastAPI, MySQL | Public Unified API, provider client, invoice normalization, downstream-to-public error mapping, API-local Docker/CI |
| `sage-provider-simulator` | Flask | Deterministic local Sage-like provider behavior, fixtures, provider endpoint contracts, error simulations, simulator-local Docker/CI |

## Non-Negotiable Principles

### INV-001: Service Boundary Enforcement

Each repository owns its own application logic. The integration workspace
must not contain FastAPI, Flask, or any runtime service implementation.

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

### INV-016: Repository Ownership

- `integration-workspace` owns architecture decisions, canonical system
  contracts, roadmap, and cross-service acceptance criteria. It contains no
  FastAPI, Flask, or runtime service implementation.
- `unified-finance-integration-api` owns the public Unified API, provider
  client, invoice normalization, downstream-to-public error mapping, and
  API-local Docker/CI.
- `sage-provider-simulator` owns deterministic local Sage-like provider
  behavior, fixtures, provider endpoint contracts, error simulations, and
  simulator-local Docker/CI.

### INV-017: Coordinated Contract Changes

System contract changes require coordinated planning before implementation.
No service repository may unilaterally alter a system-level contract without
an approved coordination plan in the workspace.

### INV-018: Source of Truth

Git history, diffs, and command output are authoritative. Agent summaries,
prior statements, or verbal descriptions are not evidence. Full commit SHA
must always come from `git rev-parse HEAD`.

### INV-019: Explicit Approval Gates

Explicit approval is mandatory before: out-of-scope modifications, commit,
push, PR creation, merge, and local or remote branch deletion. Silence,
acknowledgement, or non-English affirmations ("есть", "ок", "понятно") are
not approval for state-changing actions.

### INV-020: Declared Scope Enforcement

Each feature has a declared file scope. Any source-code, CI, dependency,
formatting, or behavior change outside that scope requires explicit approval
before it is committed or pushed.

### INV-021: CI Failure Reporting

CI failures must be reported before fixes are applied. CI remediation must
use a separate commit. A fix changing runtime code, tests, dependencies,
public behavior, or scope requires a separate approved commit and an updated
review; a separate PR is needed if the original PR is merged or if the change
expands approved scope.

## Traceability

Every requirement (FR-xxx) and invariant (INV-xxx) must trace through:
specification → plan → tasks → tests → contract.

## Applicability

Invariants INV-016 through INV-021 apply prospectively from the merge of
the governance PR that introduced them. They do not retroactively reclassify,
revert, or invalidate work completed before that merge.
