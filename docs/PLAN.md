# Workflow Audit and Cleanup Plan

## Summary
- Cross-check outcome on March 11, 2026:
1. `pytest` passes for this repo (`18 passed`).
2. The `python-app.yml` flake8 **critical-only** gate (`E9,F63,F7,F82`) is compatible with the codebase.
3. The separate `pylint.yml` workflow is currently not viable as a required CI gate (many failures, including true/false-positive static-analysis noise for SymPy-heavy code).
- Decision locks from you:
1. Drop `pylint` workflow.
2. Keep flake8 as syntax-critical gate (not style-blocking).

## Implementation Changes
1. Consolidate CI to one workflow by removing `.github/workflows/pylint.yml` (unnecessary + duplicate signal).
2. Update `.github/workflows/python-app.yml`:
   - Switch `actions/setup-python` from `v3` to `v5`.
   - Keep one Python version (`3.11`) to match active project/runtime baseline.
   - Install runtime deps from `requirements.txt`, plus CI-only deps (`pytest`, `flake8`).
   - Keep only the blocking flake8 critical check:
     `flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics`
   - Remove the non-blocking style-report command (`--exit-zero`) since you selected syntax-only gating.
   - Run tests as `pytest -q tests` for explicit scope and stable discovery.
3. Add CI audit log in `docs/`:
   - File: `docs/ci_workflow_audit_2026-03-11.md`
   - Include: workflows reviewed, commands used for validation, pass/fail findings, removed items, and final CI policy decisions.

## Public Interface / Behavior Impact
- No app runtime API changes.
- CI behavior changes:
1. Pylint no longer runs on push.
2. Main CI gate remains tests + critical lint.
3. CI dependency on deprecated action versions is removed.

## Test and Validation Plan
1. Local equivalence checks after edits:
   - `python -m flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics`
   - `python -m pytest -q tests`
2. GitHub validation:
   - Open PR and confirm only updated Python workflow runs.
   - Confirm green status on `push`/`pull_request` for `main`.
3. Documentation verification:
   - Ensure log file exists under `docs/` and records outcomes/decisions clearly.

## Assumptions and Defaults
1. Pylint is removed rather than retained as advisory.
2. Flake8 remains critical-only (syntax/undefined-name class issues), not style-enforcing.
3. Single-version CI (`3.11`) is sufficient for current project scope.
