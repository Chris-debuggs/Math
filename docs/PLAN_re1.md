# CI Workflow Simplification and Audit Log

## Summary
Refactor GitHub Actions to one reliable Python CI pipeline for this SymPy-based project: run critical flake8 checks plus pytest, remove unnecessary pylint workflow, and document the audit/results in `docs/ci_workflow_audit_2026-03-11.md`.

## Key Changes
1. GitHub workflow cleanup:
- Delete `.github/workflows/pylint.yml`.
- Update `.github/workflows/python-app.yml` to:
1. use `actions/setup-python@v5`
2. pin `python-version: "3.11"`
3. install dependencies via:
   - `python -m pip install --upgrade pip`
   - `pip install -r requirements.txt`
   - `pip install pytest flake8`
4. run only blocking flake8 critical checks:
   - `flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics`
5. run tests with deterministic scope:
   - `pytest -q tests`
- Remove the non-blocking style flake8 invocation (`--exit-zero`), since CI policy is syntax/structural blocking only.

2. Documentation log:
- Add `docs/ci_workflow_audit_2026-03-11.md` containing:
1. workflows reviewed (`python-app.yml`, `pylint.yml`)
2. local cross-check commands executed and outcomes
3. rationale for removing pylint in this repo
4. final CI policy and expected job flow
5. note that optional future optimizations (pip cache, Ruff migration) are deferred.

## Test Plan
1. Local dry run of CI-equivalent commands:
- `python -m flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics`
- `python -m pytest -q tests`
2. GitHub validation:
- Open/update PR and confirm only the unified Python workflow triggers.
- Verify job passes on both `push` and `pull_request` targeting `main`.
3. Regression guard:
- Confirm existing `pytest.ini` behavior is respected by CI (`testpaths = tests`).

## Assumptions
- Project baseline is Python 3.11 and no backward-compatibility matrix is required.
- Lint policy is intentionally minimal and blocking only for fatal/structural issues.
- Pylint removal is permanent for now; advisory lint expansion is deferred.
- Caching and Ruff adoption are explicitly out of scope for this change set.
