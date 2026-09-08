# Specification — Unified Finance Integration v0.1.0

**Version:** 0.1.0
**Status:** Draft
**Author:** AI Agent (Architect)
**Date:** 2026-09-08
**Constitution:** [constitution.md](../../.specify/memory/constitution.md)

---

## 1. Overview

The Unified Finance Integration ecosystem provides a local demonstration of
invoice synchronization from a provider simulator to a unified API service.
It consists of three repositories with strict service boundaries, orchestrated
via Docker Compose in the integration workspace.

The P0 goal is an end-to-end value flow: the FastAPI service fetches invoices
from the Flask provider simulator, normalizes them, persists them to MySQL,
and displays them in a dashboard — all running locally via `docker compose up`.

---

## 2. User Stories

### US-001: Developer Local Setup

> As a developer, I want to clone all three repositories and run
> `docker compose up` so that the entire ecosystem starts locally with
> no additional manual steps.

### US-002: Invoice Synchronization

> As a user, I want the Unified API to fetch invoices from the provider
> simulator, normalize them, and store them in the database so that I can
> view consolidated invoice data.

### US-003: Dashboard View

> As a user, I want to view synchronized invoices in a web dashboard
> so that I can verify the integration is working correctly.

### US-004: Provider Authentication

> As a developer, I want the provider simulator to require X-API-Key
> authentication so that the integration demonstrates realistic auth flows.

### US-005: Error Resilience

> As a developer, I want the provider simulator to return predictable
> 429 (rate limit) and 500 (server error) responses so that I can verify
> the Unified API handles errors gracefully.

### US-006: Paginated Retrieval

> As a developer, I want the provider simulator to support pagination
> so that the Unified API correctly handles multi-page responses.

### US-007: Contract Governance

> As a developer, I want a versioned API contract in the integration
> workspace so that cross-service changes follow a documented process.

---

## 3. Functional Requirements

### 3.1 Integration Workspace (this repository)

| ID | Requirement | Priority |
|---|---|---|
| FR-001 | Provide a `compose.yaml` that starts all services (FastAPI, Flask, MySQL) with a single command | P0 |
| FR-002 | Provide `.env.example` with all required environment variables and placeholder values | P0 |
| FR-003 | Own and version the provider API contract (OpenAPI or JSON schema) | P0 |
| FR-004 | Document the contract change workflow | P0 |
| FR-005 | Document local-development setup in README | P0 |
| FR-006 | Provide an architecture diagram | P0 |
| FR-007 | Define integration smoke tests that verify end-to-end flow | P1 |
| FR-008 | Define contract tests that validate provider API compliance | P1 |
| FR-009 | Document release process and Gitflow workflow | P1 |
| FR-010 | Provide health-check configuration for all services in Compose | P0 |

### 3.2 Unified Finance Integration API (FastAPI — separate repository)

| ID | Requirement | Priority |
|---|---|---|
| FR-101 | Expose `/api/v1/invoices` endpoint to list normalized invoices | P0 |
| FR-102 | Implement sync job to fetch invoices from provider simulator | P0 |
| FR-103 | Normalize provider invoice format to unified schema | P0 |
| FR-104 | Persist normalized invoices to MySQL | P0 |
| FR-105 | Serve Swagger/OpenAPI documentation | P0 |
| FR-106 | Serve a web dashboard displaying synchronized invoices | P0 |
| FR-107 | Handle provider 429 responses with retry and backoff | P1 |
| FR-108 | Handle provider 500 responses with clear error handling and logging (retries deferred to P1) | P0 |
| FR-109 | Handle paginated provider responses | P1 |
| FR-110 | Authenticate to provider using X-API-Key from environment | P0 |

### 3.3 Sage Provider Simulator (Flask — separate repository)

| ID | Requirement | Priority |
|---|---|---|
| FR-201 | Serve `/api/v1/invoices` with fixture invoice data | P0 |
| FR-202 | Require X-API-Key authentication on provider API endpoints under `/api/v1/`; the health endpoint and local simulator UI remain public | P0 |
| FR-203 | Support pagination with `page` and `per_page` parameters | P1 |
| FR-204 | Return 429 on predictable conditions (e.g., specific header or rate) | P1 |
| FR-205 | Return 500 on predictable conditions (e.g., specific query parameter) | P0 |
| FR-206 | Serve a small UI showing available fixture data and simulator status | P1 |

---

## 4. Non-Functional Requirements

| ID | Requirement | Priority |
|---|---|---|
| NFR-001 | All services must start within 60 seconds via `docker compose up` | P0 |
| NFR-002 | No real API keys, tokens, or provider credentials in any repository | P0 |
| NFR-003 | All technical documentation and code in English | P0 |
| NFR-004 | The provider simulator must be clearly labeled as a local portfolio simulator | P0 |
| NFR-005 | Deterministic, independent, and fast tests | P1 |
| NFR-006 | CI pipeline for each repository: lint, test, build | P1 |
| NFR-007 | Semantic HTML and basic UX in dashboards | P2 |

---

## 5. Acceptance Criteria

### AC-001: Local Startup (US-001, FR-001, FR-002, NFR-001)

- [ ] `docker compose up` starts FastAPI, Flask, and MySQL.
- [ ] All services are healthy within 60 seconds.
- [ ] `.env.example` contains all required variables with placeholder values.
- [ ] No real credentials are required or present.

### AC-002: End-to-End Invoice Sync (US-002, FR-102, FR-103, FR-104)

- [ ] Triggering a sync job in the FastAPI service fetches invoices from the simulator.
- [ ] Invoices are normalized to the unified schema.
- [ ] Normalized invoices are persisted in MySQL.
- [ ] Subsequent GET `/api/v1/invoices` returns the persisted data.

### AC-003: Dashboard Display (US-003, FR-106)

- [ ] The FastAPI dashboard displays synchronized invoices.
- [ ] The dashboard is accessible via browser at the documented URL.

### AC-004: Provider Authentication (US-004, FR-110, FR-202)

- [ ] The simulator rejects requests to `/api/v1/` without a valid X-API-Key (401).
- [ ] The simulator's health endpoint and UI remain accessible without auth.
- [ ] The FastAPI service sends X-API-Key from environment config.

### AC-005: Basic Error Handling — P0 (US-005, FR-108, FR-205)

- [ ] The simulator returns 500 under predictable conditions.
- [ ] The FastAPI service logs provider 500 errors clearly and does not crash.
- [ ] The sync job reports failure status when a provider 500 occurs.

### AC-005b: P1a Provider Error Simulation — Contract-Drafted / Pending Review (FR-204)

> **Status:** Contract-Drafted / Pending Review. Simulator implementation exists on
> `feature/p1a-pagination-and-429` at `c62b6e9e4ea3ee26478307bbd78089214ba8786f`
> but is not yet merged or live-E2E-verified.

- [ ] Authentication is evaluated first: missing/invalid `X-API-Key` returns
      `401` before any simulation or pagination validation.
- [ ] Following successful authentication, supported `simulate_error=429` and
      `simulate_error=500` take precedence over duplicate checks and pagination
      validation.
- [ ] `simulate_error=429` returns HTTP `429`, `Content-Type: application/json`,
      `Retry-After: 5`, and exact body:
      `{"error":"Too Many Requests","message":"Simulated rate limit exceeded. Please retry after 5 seconds."}`
- [ ] Existing `simulate_error=500` behavior remains unchanged.
- [ ] Unknown `simulate_error` values fall through to ordinary successful
      response (observed simulator behavior, not a system-wide guarantee).
- [ ] API P0 has mocked coverage for downstream provider `429` → public `503`
      mapping; this criterion does not assert live cross-service coverage.

### AC-006: P1a Provider Pagination — Contract-Drafted / Pending Review (US-006, FR-203)

> **Status:** Contract-Drafted / Pending Review. Simulator implementation exists on
> `feature/p1a-pagination-and-429` at `c62b6e9e4ea3ee26478307bbd78089214ba8786f`
> but is not yet merged or live-E2E-verified.

- [ ] `page` defaults to `1`; valid values are canonical positive integers ≥ 1.
- [ ] `per_page` defaults to `10`; valid values are canonical integers from `1`
      through `100`.
- [ ] These defaults and `100` maximum are simulator P1a constraints, not
      universal provider-adapter standards.
- [ ] Successful `200` responses retain top-level `invoices` and include a
      `pagination` object with integer fields `page`, `per_page`, `total_items`,
      and `total_pages`.
- [ ] A request beyond the final page returns `200` with `invoices: []` and
      accurate pagination metadata.
- [ ] Invalid `page` returns `400` with exact body:
      `{"error":"Bad Request","message":"Invalid 'page' parameter: must be an integer >= 1."}`
- [ ] Invalid `per_page` returns `400` with exact body:
      `{"error":"Bad Request","message":"Invalid 'per_page' parameter: must be an integer between 1 and 100."}`
- [ ] Duplicate `page` returns `400` with exact body:
      `{"error":"Bad Request","message":"Duplicate 'page' query parameter."}`
- [ ] Duplicate `per_page` returns `400` with exact body:
      `{"error":"Bad Request","message":"Duplicate 'per_page' query parameter."}`

### AC-006b: P1a API Compatibility — Contract-Drafted / Pending Review

> **Status:** Contract-Drafted / Pending Review.

- [ ] API P0 remains backward-compatible because `invoices` remains a top-level
      response key.
- [ ] API P0 may ignore `pagination` and does not yet traverse subsequent
      provider pages.

### AC-007: Contract Governance (US-007, FR-003, FR-004)

- [ ] A versioned provider API contract exists in `integration-workspace`.
- [ ] The contract change workflow is documented.
- [ ] Contract changes precede implementation changes.

---

## 6. Assumptions

- A-001: Docker and Docker Compose are available on the developer's machine.
- A-002: MySQL runs as a container managed by Compose, not an external service.
- A-003: The provider simulator uses static fixture data, not a database.
- A-004: All services communicate over a Docker bridge network.
- A-005: The provider API contract is owned by the integration workspace.
- A-006: v0.1.0 targets local development only; no cloud deployment.
- A-007: The X-API-Key for the simulator is a non-secret test value.

---

## 7. Out of Scope

- OS-001: Cloud deployment, Kubernetes, or any production infrastructure.
- OS-002: Real Sage API integration or any real provider.
- OS-003: User authentication for the dashboard (no login required).
- OS-004: Multi-tenant or multi-user support.
- OS-005: Database migrations beyond initial schema creation.
- OS-006: Performance optimization or load testing.
- OS-007: Monitoring, alerting, or APM tooling.
- OS-008: Shared database between FastAPI and Flask services.
- OS-009: CD pipeline (no real deployment target exists).
- OS-010: LLM-based features or AI-powered analysis.
- OS-011: Mobile or native application support.

---

## 8. Cross-Service Invariants

These invariants apply across all three repositories (traced to constitution):

| ID | Invariant | Constitution Ref |
|---|---|---|
| CSI-001 | API contract is owned by `integration-workspace`; changes follow the contract workflow | INV-002 |
| CSI-002 | No secrets, tokens, passwords, or real credentials in Git | INV-004 |
| CSI-003 | The provider simulator is always described as a local portfolio simulator | INV-003 |
| CSI-004 | Service boundaries are enforced: no cross-repository business logic | INV-001 |
| CSI-005 | Reproducible local startup from clean clone | INV-009 |
| CSI-006 | All technical artifacts in English | INV-013 |
| CSI-007 | Gitflow discipline with Conventional Commits | INV-006, INV-007 |
| CSI-008 | CI must pass before merge | INV-014 |
| CSI-009 | No fabricated features, test results, or deployments | INV-008 |
| CSI-010 | Incremental delivery: P0 → P1 → P2 | INV-010 |

---

## 9. Risks

| ID | Risk | Mitigation |
|---|---|---|
| R-001 | Contract drift between workspace and service repositories | Contract change workflow (FR-004), contract tests (FR-008) |
| R-002 | Docker networking issues across platforms | Document known issues, test on Windows/macOS/Linux |
| R-003 | Scope creep into real provider integration | Explicit out-of-scope list, constitution invariant INV-003 |
| R-004 | Over-engineering beyond P0 needs | KISS/YAGNI principles (INV-012), P0/P1/P2 gates (INV-010) |

---

## 10. Glossary

| Term | Definition |
|---|---|
| Unified API | The FastAPI service that aggregates and normalizes invoice data |
| Provider Simulator | The Flask service that simulates a Sage-like invoice provider (local portfolio simulator) |
| Integration Workspace | This repository; owns orchestration, contracts, and cross-service concerns |
| Sync Job | A task in the Unified API that fetches and normalizes invoices from the provider |
| Contract | The versioned API specification (OpenAPI/JSON schema) defining provider endpoints |
