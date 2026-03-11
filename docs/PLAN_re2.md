# CI Workflow Finalization Plan (SymPy Project)

## Summary
Implement a single, reliable Python CI workflow that blocks merges only on real defects: fatal syntax/structure issues and failing tests. Remove redundant/noisy linting and document the decision trail.

## Implementation Changes
1. Replace multi-workflow setup with one workflow:
- Delete `.github/workflows/pylint.yml`.
- Keep `.github/workflows/python-app.yml` as the only Python CI workflow.

2. Update `.github/workflows/python-app.yml`:
- Use `actions/setup-python@v5`.
- Pin `python-version: "3.11"`.
- Ensure triggers are explicitly:
  - `push` on `main`
  - `pull_request` on `main`
- Add explicit repo-root execution context to avoid directory ambiguity:
  - either `defaults.run.working-directory: .`
  - or step-level `working-directory: .` for lint/test steps.
- Install in this order:
  1. `python -m pip install --upgrade pip`
  2. `pip install -r requirements.txt`
  3. `pip install pytest flake8`
- Run only blocking fatal flake8 checks:
  - `flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics`
- Run deterministic tests:
  - `pytest -q tests`
- Remove non-blocking style lint invocation (`--exit-zero`) from CI.

3. Add audit log file:
- Create `docs/ci_workflow_audit_2026-03-11.md`.
- Include:
  - current workflows reviewed
  - local cross-check commands and outcomes
  - why pylint was removed for this codebase
  - final CI policy and expected gate behavior
  - optional future improvements (pip cache, Ruff) marked as deferred.

## Validation Plan
1. Local pre-PR validation:
- `python -m flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics`
- `python -m pytest -q tests`

2. GitHub validation:
- Push branch / open PR.
- Confirm only the unified workflow runs.
- Confirm pass on both `push` and `pull_request` events for `main`.

3. Acceptance criteria:
- CI fails on syntax/structural errors or failing tests.
- CI does not fail on stylistic-only issues.
- Audit markdown exists in `docs/` with rationale and evidence.

## Assumptions
- Python 3.11 is the project baseline.
- Multi-version compatibility matrix is out of scope.
- Pylint removal is intentional and not replaced with another strict linter in this change.
- Caching and Ruff migration are explicitly deferred.
