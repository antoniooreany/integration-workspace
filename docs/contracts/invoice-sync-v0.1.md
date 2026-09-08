# Invoice Sync System Contract — v0.1

**Version:** 0.1
**Status:** Draft
**Date:** 2026-09-08
**Constitution:** [constitution.md](../../.specify/memory/constitution.md)

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
  ]
}
```

P0 consumes the top-level `invoices` list directly. The response is a single
page containing all fixture invoices.

### Simulator Guarantees & Planned Extensions

Current simulator P0 guarantees only authenticated `GET /api/v1/invoices`
returning a top-level `invoices` list and deterministic `simulate_error=500`.

Provider pagination (`page`, `per_page` query parameters) and deterministic
`simulate_error=429` with `Retry-After` are planned P1a simulator extensions
and are not yet required by this canonical v0.1 P0 contract until the simulator
P1a PR is merged.

API P0 has mocked tests for downstream 429 mapping, but no live cross-service
429 dependency is required yet.

---

## 3. API Endpoint

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

---

## 4. Safe API Error Mapping

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

## 5. Explicit Exclusions (v0.1)

The following are explicitly out of scope for this contract version:

- Real Sage API compatibility or any real provider.
- Real API keys, tokens, or production credentials.
- Database schema or persistence details (API-internal concern; P0 has no persistence).
- OAuth, JWT, or user authentication on the public API.
- Dashboard or UI specification.
- Automatic retries or backoff logic (P1).
- Webhooks or push notifications.
- Cloud deployment, Kubernetes, or production infrastructure.
- Scheduled, background, or cron-based sync triggers.
- Live cross-service CI suites (P1).
- Pagination (P1a; requires simulator P1a merge and coordinated planning).

---

## 6. Change Control

Any change to this contract requires:

1. A proposal in the integration workspace (this repository).
2. Coordinated planning with affected service repositories (INV-017).
3. Explicit approval before implementation begins.
4. Linked feature branches in affected service repositories.
5. End-to-end verification before merge.
