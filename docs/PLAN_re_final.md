# Final CI Simplification Plan (with Refinements)

## Summary
Adopt one Python CI workflow that blocks only on runtime-relevant defects, with explicit repo-root execution and cleaner test logs.

## Key Changes
1. Consolidate workflows:
- Remove `.github/workflows/pylint.yml`.
- Keep a single workflow: `.github/workflows/python-app.yml`.

2. Update `.github/workflows/python-app.yml`:
- `actions/setup-python@v5`
- `python-version: "3.11"`
- Triggers:
  - `push` on `main`
  - `pull_request` on `main`
- Add explicit default run directory:
  ```yaml
  defaults:
    run:
      working-directory: .
  ```
- Dependency install order:
  1. `python -m pip install --upgrade pip`
  2. `pip install -r requirements.txt`
  3. `pip install pytest flake8`
- Keep only fatal flake8 gate:
  - `flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics`
- Run deterministic tests with quieter logs:
  - `pytest -q tests --disable-warnings`
- Remove non-blocking style lint step (`--exit-zero`).

3. Add CI audit log:
- Create `docs/ci_workflow_audit_2026-03-11.md` documenting:
  - reviewed workflows and local cross-check results,
  - rationale for removing pylint,
  - final CI gate design,
  - deferred improvements (pip cache, Ruff).

## Validation Plan
1. Local CI-equivalent checks:
- `python -m flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics`
- `python -m pytest -q tests --disable-warnings`
2. PR validation:
- Confirm only unified workflow runs.
- Confirm passing status on both `push` and `pull_request` to `main`.

## Assumptions
- Python 3.11 is the sole supported CI baseline.
- Warning suppression is acceptable for CI readability; warning triage is deferred.
- Multi-version matrix and broader lint/style enforcement remain out of scope.
