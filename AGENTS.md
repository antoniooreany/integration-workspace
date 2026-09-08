# Integration Workspace — Agent Configuration

## Reading Order

Before working in this repository, read:

1. `~/.gemini/GEMINI.md`
2. `../GEMINI.md`
3. `../AGENTS.md`
4. `./GEMINI.md`
5. `.specify/memory/constitution.md`
6. Active specification, plan, and task list under `specs/`

## Agent Roles

### Architect Agent

- **Scope:** Cross-service design, API contracts, architecture diagrams.
- **Writes to:** `specs/`, `.specify/`, `contracts/`, `docs/`.
- **Does not write:** Application code, Dockerfiles, CI workflows.

### Orchestration Agent

- **Scope:** Docker Compose, environment configuration, local startup.
- **Writes to:** `compose.yaml`, `.env.example`, `docs/`.
- **Does not write:** Service application code.

### Validation Agent

- **Scope:** Integration tests, contract validation, smoke tests.
- **Writes to:** `tests/`, `scripts/`.
- **Does not write:** Service unit tests or business logic.

## Constraints

- One agent per branch at a time.
- All changes require Pull Request review.
- Never commit to `main` or `develop` directly.
- Never fabricate integrations, test results, or deployments.
- The provider simulator is a local portfolio simulator, not an official Sage API.
- No secrets, tokens, or real credentials in any file.
