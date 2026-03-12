# New Things Done - README

Date: 2026-03-12

## Summary
This update added two major capabilities to the MA3151 deterministic tutor:
1. Concept support (syllabus-aligned theory cards)
2. Visualization support (matrix transformations and multivariable surfaces)

## Files Added
- `content/__init__.py`
- `content/concept_cards.py`
- `visualizers/__init__.py`
- `visualizers/plots.py`
- `tests/test_concept_and_visuals.py`

## Files Updated
- `app.py`
- `requirements.txt`

## Detailed Changes

### 1) Concept Cards
- Added topic-wise concept metadata for core syllabus areas.
- Added exam-oriented checklists per topic.
- Added related foundation prompts for theory-heavy parts (vector space, rank-nullity, linear transformation properties, curvature basics).
- Implemented helper APIs:
  - `get_topic_card(topic_key)`
  - `get_foundation_cards(topic_key)`

### 2) Visualization Utilities
- Added 2D linear transformation visualization:
  - Plots original unit square and transformed square.
  - Shows basis vectors `e1`, `e2` and transformed vectors `A*e1`, `A*e2`.
- Added 3D maxima/minima visualization:
  - Plots surface `z = f(x,y)`.
  - Marks critical points from solving `f_x = 0`, `f_y = 0`.

### 3) Streamlit Integration (`app.py`)
- Added sidebar toggles:
  - `Concept Cards`
  - `Visualize`
- Added concept card rendering block above step-by-step solution.
- Added visual intuition block for:
  - Matrix topics (`eigenvalues`, `eigenvalues_3x3`, `cayley_hamilton`, `quadratic_form`)
  - `maxima_minima`
- Added graceful fallback when `matplotlib` is unavailable:
  - Visualization toggle is disabled.
  - A sidebar note is shown to install `matplotlib`.

### 4) Dependency Update
- Added to `requirements.txt`:
  - `matplotlib>=3.8`

### 5) Test Coverage
- Added new tests for:
  - Concept card schema/availability
  - Foundation card mapping
  - Plot object creation for both visualizers
- Visualization tests use optional import behavior (skip if `matplotlib` is not installed).

## Verification Performed
- `python -m pytest -q tests` -> `20 passed, 2 skipped`
- `python -m flake8 . --jobs 1 --count --select=E9,F63,F7,F82 --show-source --statistics` -> `0`

## Notes
- Existing deterministic solver behavior and step rendering flow were preserved.
- Visual features are additive and do not affect solver correctness.

