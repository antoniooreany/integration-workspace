# Unified Finance Integration — Local Demo

A P0 Docker Compose setup that demonstrates a synchronous, stateless
invoice-synchronization flow between two services:

- **simulator** — a Flask-based provider simulator serving fixture invoices
  with X-API-Key authentication.
- **api** — a FastAPI service that fetches, validates, and normalizes invoices
  from the simulator and returns them in the response.

There is no database, no persistence, no migration, and no dashboard data layer.

## Architecture

```text
Developer
  |
  | docker compose --env-file .env up --build
  v
integration-workspace
  |- simulator :5000
  |    |- GET /health
  |    `- GET /api/v1/invoices (X-API-Key)
  |
  `- api :8000
       |- GET /health
       `- POST /api/v1/sync/invoices
            `- GET http://simulator:5000/api/v1/invoices
```

The API reaches the simulator through Docker service DNS:

```text
PROVIDER_BASE_URL=http://simulator:5000
```

## Prerequisites

- Docker Desktop or Docker Engine with Docker Compose v2.
- This workspace and both sibling repositories located under the same parent
  directory:

```text
unified-finance-integration/
|- integration-workspace/
|- unified-finance-integration-api/
`- sage-provider-simulator/
```

## Quick Start

From `integration-workspace`:

```bash
cp .env.example .env
docker compose --env-file .env up --build
```

On Windows PowerShell, use:

```powershell
Copy-Item .env.example .env
docker compose --env-file .env up --build
```

The Compose stack creates two services only:

- API: `http://localhost:8000`
- Simulator: `http://localhost:5000`

Stop the stack:

```bash
docker compose down
```

## Demo Flow

In a separate terminal, verify simulator health:

```bash
curl -i http://localhost:5000/health
```

Verify API health:

```bash
curl -i http://localhost:8000/health
```

Run the P0 synchronization flow:

```bash
curl -i -X POST http://localhost:8000/api/v1/sync/invoices
```

Expected result:

- HTTP `200`
- `status` is `success`
- `fetched_count` reflects the simulator fixture returned for that request
- `invoices` contains normalized invoice objects

You can also inspect API documentation at:

```text
http://localhost:8000/docs
```

## Configuration

| Variable | Purpose | Default |
|---|---|---|
| `PROVIDER_API_KEY` | Shared API key between API and simulator; demo-only, non-secret | `test-api-key-not-a-secret` |
| `PROVIDER_BASE_URL` | Simulator URL used by the API container | `http://simulator:5000` |
| `API_PORT` | Host port mapped to the API | `8000` |
| `SIMULATOR_PORT` | Host port mapped to the simulator | `5000` |

Do not use the provided `PROVIDER_API_KEY` outside this local demo.

## P0 Boundaries

This P0 demo proves a working synchronous API-to-simulator path with Docker
service discovery and health-gated startup.

It does not include:

- MySQL, any other database, persistence, migrations, database volumes, or
  `DATABASE_URL` / `MYSQL_*` configuration.
- Dashboard data persistence or invoice retrieval from storage.
- API pagination traversal.
- Retries or backoff.
- Live cross-service provider `429` to public API `503` E2E verification.
- Workspace-level CI.

Those items remain separately planned P1 or future work. The current simulator
uses deterministic fixture data; the expected invoice count is intentionally
not a fixed acceptance criterion.

## Troubleshooting

If ports `8000` or `5000` are already in use, change `API_PORT` or
`SIMULATOR_PORT` in `.env` and restart the stack.

If the API does not become healthy, inspect service logs:

```bash
docker compose logs simulator
docker compose logs api
```
