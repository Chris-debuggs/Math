# CI Workflow Audit - 2026-03-11

## Scope
- Reviewed:
  - `.github/workflows/python-app.yml`
  - `.github/workflows/pylint.yml` (removed in this update)

## Cross-check Commands and Outcomes

### Test gate
- Command:
  - `python -m pytest -q tests --disable-warnings`
- Outcome:
  - Passed locally (`18 passed`).

### Lint gate (fatal-only)
- Command:
  - `python -m flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics`
- Outcome:
  - No fatal lint errors in local validation path.

## Findings
1. The standalone `pylint` workflow produced high-noise findings for this SymPy-heavy codebase and was not aligned with the target CI policy.
2. The main workflow used older action/runtime versions (`setup-python@v3`, Python 3.10) and included a non-blocking style lint step that was outside the desired gate criteria.

## Changes Applied
1. Consolidated CI to one workflow:
   - Deleted `.github/workflows/pylint.yml`.
2. Updated `.github/workflows/python-app.yml`:
   - `actions/setup-python@v5`
   - Python `3.11`
   - Explicit default run directory:
     ```yaml
     defaults:
       run:
         working-directory: .
     ```
   - Dependency install order:
     1. `python -m pip install --upgrade pip`
     2. `pip install -r requirements.txt`
     3. `pip install pytest flake8`
   - Kept only fatal flake8 gate:
     - `flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics`
   - Test command:
     - `pytest -q tests --disable-warnings`
   - Removed non-blocking style lint command (`--exit-zero`).

## Final CI Policy
Repository event (`push`/`pull_request` on `main`)
1. Setup Python 3.11
2. Install dependencies
3. Run fatal flake8 checks
4. Run pytest

Merge is blocked only by structural/runtime-relevant defects (fatal lint or failing tests).

## Deferred Improvements
- Add pip dependency caching in GitHub Actions to reduce runtime.
- Consider migrating lint stack to Ruff in a separate modernization task.
