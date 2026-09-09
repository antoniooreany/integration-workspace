# Delivery Control Policy

**Version:** 0.2.0
**Status:** Active
**Date:** 2026-09-08
**Constitution:** [constitution.md](../../.specify/memory/constitution.md)

---

## 1. Applicability

This policy applies prospectively from the merge of the governance PR that
introduced it. It does not retroactively reclassify, revert, or invalidate
work completed before that merge.

---

## 2. Delivery Sequence

Every feature delivery follows this sequence. Each numbered step requires
explicit approval unless noted otherwise.

| Step | Action | Approval Required |
|---|---|---|
| 1 | Plan and approved scope | Yes — scope must be explicitly approved |
| 2 | Implementation permission | Yes — explicit go-ahead to write code/docs |
| 3 | Read-only validation and review | No — read-only commands may be batched |
| 4 | Explicit commit approval | Yes — review diff before committing |
| 5 | Explicit push approval | Yes — separate from commit approval |
| 6 | Explicit PR approval | Yes — separate from push approval |
| 7 | Review / CI | Informational — report results, do not auto-fix |
| 8 | Explicit merge approval | Yes — separate from PR approval |
| 9 | Post-merge verification | Informational — report verification results |
| 10 | Optional explicit local/remote branch cleanup approval | Yes — if cleanup is performed |

### Batching Rules

- Read-only commands (e.g., `git status`, `git diff`, `git log`) may be
  batched and executed without individual approval.
- State-changing actions (commit, push, PR, merge, branch deletion) each
  require separate explicit approval.

---

## 3. Approval Semantics

### What Constitutes Approval

Approval is an explicit, unambiguous instruction to perform a specific
state-changing action. Examples:

- "Approve the commit."
- "Push it."
- "Create the PR."
- "Merge."

### What Does NOT Constitute Approval

The following are **not** approval for state-changing actions:

- Silence or no response.
- Acknowledgement: "есть", "ок", "понятно", "got it", "I see", "understood".
- Continuation prompts: "go on", "continue" (unless explicitly tied to a
  specific state-changing action).
- Non-specific affirmations: "looks good" (without naming the action).

When in doubt, ask for explicit confirmation of the specific action.

---

## 4. Declared Scope Enforcement

Each feature has a declared file scope. Any change outside that scope —
including source code, CI configuration, dependencies, formatting, or
behavioral changes — requires explicit approval before it is committed
or pushed (INV-020).

---

## 5. CI Failure Policy

### Reporting First

CI failures must be **reported** before any fix is applied. The agent must
present the failure details and wait for approval before writing any
remediation code.

### CI-Only Fix (Within Approved Scope)

A fix that addresses only CI configuration, linting, or formatting issues
within the originally approved file scope may be a separate approved commit
on the same feature branch.

### Fix Changing Runtime Code, Tests, Dependencies, or Behavior

A fix that changes runtime code, tests, dependencies, public behavior, or
expands the approved scope requires:

1. A separate approved commit.
2. An updated review of the changed diff.
3. A **separate PR** if:
   - The original PR has already been merged; or
   - The fix expands the originally approved scope.

---

## 6. Source of Truth

### Authoritative Sources

- Git history (`git log`, `git show`, `git diff`).
- Command output (`git status`, `git rev-parse`, CI logs).
- File contents on disk.

### Non-Authoritative Sources

- Agent summaries or prior statements.
- Verbal descriptions of what was done.
- Memory or recollection of previous actions.

### Commit SHA Requirement

The full commit SHA must always come from `git rev-parse HEAD` executed
after the commit is created. Shortened hashes, memorized values, or
agent-generated SHAs are not acceptable.

---

## 7. Out-of-Scope Modifications

Any modification outside the declared feature scope requires:

1. Explicit identification of the out-of-scope change.
2. Justification for why it is needed.
3. Explicit approval before it is committed or pushed.

This includes but is not limited to:

- Files not listed in the approved scope.
- Dependency additions or version changes.
- CI/CD configuration changes.
- Formatting or style changes in unrelated files.
- Behavioral changes beyond the approved specification.

---

## 8. Branch Cleanup

Local and remote branch deletion after merge requires explicit approval.
Branch cleanup is optional and must never be performed automatically.
