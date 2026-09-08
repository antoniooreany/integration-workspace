# Service Ownership Matrix

**Version:** 0.2.0
**Status:** Active
**Date:** 2026-09-08
**Constitution:** [constitution.md](../../.specify/memory/constitution.md)

---

## Principle

The integration workspace governs architecture decisions and canonical system
contracts but does not host runtime service logic (no FastAPI, Flask, or
application code).

---

## Ownership Matrix

| Concern | Owner | Consumers | Change-Control Trigger |
|---|---|---|---|
| **Public API endpoints** (`/api/v1/*`) | `unified-finance-integration-api` | External callers, dashboard | Spec update in API repo; workspace contract if schema changes |
| **Provider API endpoints** (`GET /api/v1/invoices`) | `sage-provider-simulator` | `unified-finance-integration-api` | Workspace contract update before simulator implementation |
| **Invoice schema / normalization** | `unified-finance-integration-api` (normalized schema); `sage-provider-simulator` (provider-side schema) | Both services consume the workspace system contract | Workspace contract update required for shared field changes |
| **Pagination** (`page`, `per_page`) | `sage-provider-simulator` (provider behavior); `unified-finance-integration-api` (consumer traversal) | Cross-service | Workspace contract extension; coordinated planning required |
| **401 Unauthorized semantics** | `sage-provider-simulator` (enforcement); `unified-finance-integration-api` (mapping to public error) | Cross-service | Workspace contract defines expected behavior |
| **429 Rate Limit + Retry-After** | `sage-provider-simulator` (emission); `unified-finance-integration-api` (forwarding/backoff) | Cross-service | Workspace contract defines Retry-After semantics |
| **500 Server Error** | `sage-provider-simulator` (deterministic triggers); `unified-finance-integration-api` (safe mapping) | Cross-service | Workspace contract defines trigger conditions |
| **Fixtures** | `sage-provider-simulator` | `unified-finance-integration-api` (integration testing) | Simulator-local; no cross-repo approval unless fixture schema changes |
| **Environment configuration** | `integration-workspace` (`.env.example`, conventions); each service (service-specific vars) | All services | Workspace update if adding cross-service variables |
| **Docker / CI** | Each service owns its own `Dockerfile` and CI workflow | Service-local | No cross-repo trigger unless Docker network or port changes |
| **Canonical system contracts** | `integration-workspace` | Both service repositories | Coordinated planning before any implementation (INV-017) |
| **Architecture decisions / ADRs** | `integration-workspace` | All repositories | Workspace-only; informational for services |
| **Integration verification** | `integration-workspace` (smoke tests, contract tests) | All services via Compose | Workspace-local; triggered after service changes |
| **Secrets management** | All repositories (each enforces INV-004) | None | Any repository; zero tolerance (INV-004) |
| **Roadmap and cross-service acceptance criteria** | `integration-workspace` | All repositories | Workspace spec/plan update |

---

## Ownership Boundaries

- **Simulator owns provider response behavior:** HTTP status codes, response
  bodies, headers (including `Retry-After`), authentication enforcement, and
  error simulation triggers.

- **API owns downstream-to-public mapping:** How provider responses are
  transformed into public API responses, including error mapping, status code
  translation, and safe user-facing messages.

- **Workspace owns the system-level contract:** The canonical definition of
  what the provider exposes and what the API expects. Neither service may
  unilaterally change this contract without coordinated planning (INV-017).
