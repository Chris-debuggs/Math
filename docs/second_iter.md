# MA3151 CAS Tutor - Integration and Test Update

Date: 2026-03-10

## What was fixed

1. Matrix-topic wiring in `app.py`:
   - `_load_problem(...)` now passes `prob["matrix"]` to matrix-based solvers.
   - Non-matrix solvers still receive the full `prob` dictionary.

2. Solver input hardening:
   - `eigen_steps(...)`, `cayley_hamilton_steps(...)`, and `quadratic_form_steps(...)`
     now accept either:
     - a raw `sympy.Matrix`, or
     - a problem dictionary containing a `"matrix"` key.

3. Cayley-Hamilton solver bug fix:
   - Replaced matrix polynomial accumulation using `sum(...)` (which can trigger
     `int + Matrix` type errors) with explicit matrix accumulation from `sp.zeros(n)`.

## Tests added

File: `tests/test_topic_integration.py`

Coverage:
- Regression test for matrix solvers accepting problem dictionaries.
- End-to-end generator-to-solver checks for all registered topics.
- Verification that the Cayley-Hamilton `p(A)` node evaluates to the zero matrix.

## Pytest configuration

File: `pytest.ini`

Purpose:
- Restrict discovery to the `tests/` folder.
- Exclude temp pytest cache-like directories in project root.
- Disable cache provider plugin to avoid local cache permission issues.

## Result

Current test status:
- `18 passed`

Suggested run command:

```powershell
& "C:\Users\cnevi\miniconda3\envs\math\python.exe" -m pytest
```
