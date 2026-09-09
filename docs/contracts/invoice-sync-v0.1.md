# Invoice Sync System Contract — v0.1

**Version:** 0.1
**Status:** Draft
**Date:** 2026-09-08
**Constitution:** [constitution.md](../../.specify/memory/constitution.md)

---

## P1a Amendment Notice

This amendment formalizes simulator-specific P1a provider behavior: pagination
query parameters with validation, and deterministic `simulate_error=429`
emission.

The simulator implementation currently exists on:

- **Repository:** `sage-provider-simulator`
- **Branch:** `feature/p1a-pagination-and-429`
- **Commit:** `c62b6e9e4ea3ee26478307bbd78089214ba8786f`

This implementation predates the amendment and is **not yet contract-approved,
PR-approved, merged, or live-E2E-verified** until the coordinated workflow
completes.

---

## 1. Purpose

This is the canonical system-level contract for the P0 invoice synchronization
flow between the provider simulator and the Unified API.

- The **simulator** owns provider response behavior.
- The **API** owns downstream-to-public mapping.
- The **workspace** owns this contract definition.

---

## 2. Provider Endpoint

**Endpoint:** `GET /api/v1/invoices`
**Owner:** `sage-provider-simulator`

### Authentication

| Header | Value | Required |
|---|---|---|
| `X-API-Key` | Configured API key (non-secret test value) | Yes |

### Pagination Query Parameters (P1a — Simulator-Specific)

The following optional query parameters are a simulator-specific P1a extension.
These defaults and the `100` maximum are simulator P1a constraints, not
universal standards for every future provider adapter.

| Parameter | Default | Valid value |
|---|---:|---|
| `page` | `1` | Canonical positive integer, minimum `1` |
| `per_page` | `10` | Canonical integer from `1` through `100` |

### Success Response (200)

```json
{
  "invoices": [
    {
      "id": "string",
      "invoice_number": "string",
      "date": "YYYY-MM-DD",
      "due_date": "YYYY-MM-DD",
      "currency": "string (ISO 4217)",
      "total_amount": "number",
      "status": "string (draft | sent | paid | overdue | void)",
      "contact_name": "string"
    }
  ],
  "pagination": {
    "page": 1,
    "per_page": 10,
    "total_items": 0,
    "total_pages": 0
  }
}
```

P0 consumes the top-level `invoices` list directly. The `pagination` object is
included in P1a successful responses with integer fields `page`, `per_page`,
`total_items`, and `total_pages`.

A request beyond the final page returns `200` with `invoices: []` and accurate
pagination metadata.

### Pagination Validation Errors (400)

Invalid `page` returns exactly:

```json
{"error":"Bad Request","message":"Invalid 'page' parameter: must be an integer >= 1."}
```

Invalid `per_page` returns exactly:

```json
{"error":"Bad Request","message":"Invalid 'per_page' parameter: must be an integer between 1 and 100."}
```

Duplicate `page` returns exactly:

```json
{"error":"Bad Request","message":"Duplicate 'page' query parameter."}
```

Duplicate `per_page` returns exactly:

```json
{"error":"Bad Request","message":"Duplicate 'per_page' query parameter."}
```

### Simulator Guarantees & Planned Extensions

Current simulator P0 guarantees only authenticated `GET /api/v1/invoices`
returning a top-level `invoices` list and deterministic `simulate_error=500`.

P1a extends the simulator with pagination and deterministic
`simulate_error=429` as documented in this amendment.

---

## 3. Provider Error Simulation and Precedence

### Precedence Order

1. **Authentication** is evaluated first. Missing or invalid `X-API-Key`
   returns the existing `401` response before any simulation or pagination
   validation.
2. Following successful authentication, supported `simulate_error=429` and
   `simulate_error=500` **take precedence** over duplicate checks and
   pagination validation.
3. Duplicate parameter checks (`page`, `per_page`) are evaluated next.
4. Pagination parameter validation is evaluated last.

### simulate_error=429 (P1a)

- HTTP `429 Too Many Requests`
- `Content-Type: application/json`
- `Retry-After: 5`
- Exact body:

  ```json
  {"error":"Too Many Requests","message":"Simulated rate limit exceeded. Please retry after 5 seconds."}
  ```

Configurable `Retry-After` behavior is not supported.

### simulate_error=500 (P0)

Existing supported `simulate_error=500` remains unchanged from the original P0
contract behavior.

### Unknown simulate_error Values

Unknown `simulate_error` values currently fall through to ordinary successful
response behavior. This is observed simulator implementation behavior only, not
a system-wide guarantee or new validation requirement.

---

## 4. API Endpoint

**Endpoint:** `POST /api/v1/sync/invoices`
**Owner:** `unified-finance-integration-api`

### Request

No request body in P0. The sync job fetches from the provider using
environment-configured `PROVIDER_BASE_URL` and `PROVIDER_API_KEY`.

### Success Response (200)

```json
{
  "status": "success",
  "fetched_count": 0,
  "invoices": []
}
```

P0 validates and normalizes provider invoices and returns them synchronously
without persistence. P0 does not persist invoices or return a `completed`,
`synced_count`, or `message` envelope.

### API P0 Compatibility

- API P0 remains backward-compatible because `invoices` remains a top-level
  response key.
- API P0 may ignore `pagination` and does not yet traverse subsequent provider
  pages.
- API P0 has mocked coverage for downstream provider `429` → public `503`
  mapping.
- This amendment does not assert live cross-service `429` coverage.

---

## 5. Safe API Error Mapping

The API maps provider failures to safe public responses. The simulator owns
the provider response behavior; the API owns the downstream-to-public mapping.

| Provider Condition | Provider Response | API Public Response | Response Body | API Behavior |
|---|---|---|---|---|
| Valid request | `200` with `invoices` list | `200 OK` | `{"status":"success","fetched_count":...,"invoices":[...]}` | Validate, normalize, and return synchronously without persistence |
| Missing/invalid API key | `401 Unauthorized` | `500 Internal Server Error` | `{"error":"Provider configuration error"}` | Log error; do not expose provider auth details |
| Rate limited | `429 Too Many Requests` with `Retry-After: <seconds>` | `503 Service Unavailable` | `{"error":"Provider temporarily unavailable"}` | Forward only a valid numeric, non-negative `Retry-After` header; log warning |
| Server error | `500 Internal Server Error` | `502 Bad Gateway` | `{"error":"Provider service error"}` | Log full error; report sync failure; do not crash |
| Timeout / connection failure | No response | `503 Service Unavailable` | `{"error":"Provider unavailable"}` | Log timeout/connection details; report sync failure |
| Malformed JSON, missing/non-list `invoices`, or invalid invoice payload | Invalid payload | `502 Bad Gateway` | `{"error":"Invalid provider response"}` | Log validation/parse errors; fail sync with safe error |

### Retry-After Forwarding Rules

- The API forwards `Retry-After` only when the value is a valid non-negative
  integer (seconds).
- Invalid, missing, negative, or non-numeric `Retry-After` values are not
  forwarded; the API returns `503` without `Retry-After` and logs a warning.
- P0 does not implement automatic retry/backoff logic. Retries are P1.
- API P0 implements and tests this mapping using mocked responses; live cross-service 429 testing is deferred until simulator P1a is merged.

---

## 6. Explicit Exclusions (v0.1)

The following are explicitly out of scope for this contract version:

- Real Sage API compatibility or any real provider.
- Real API keys, tokens, or production credentials.
- Database schema or persistence details (API-internal concern; P0 has no persistence).
- OAuth, JWT, or user authentication on the public API.
- Dashboard or UI specification.
- API page traversal / multi-page consumption (API P1).
- Automatic retries or backoff logic (P1).
- Webhooks or push notifications.
- Cloud deployment, Kubernetes, or production infrastructure.
- Scheduled, background, or cron-based sync triggers.
- Live cross-service CI/E2E validation suites (P1).

---

## 7. Change Control

Any change to this contract requires:

1. A proposal in the integration workspace (this repository).
2. Coordinated planning with affected service repositories (INV-017).
3. Explicit approval before implementation begins.
4. Linked feature branches in affected service repositories.
5. End-to-end verification before merge.
