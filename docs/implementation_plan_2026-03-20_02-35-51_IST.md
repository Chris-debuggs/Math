# Implementation Plan - Streamlit Warning and DeltaGenerator Fixes

Date-Time (IST): 2026-03-20 02:35:51 IST
Branch: feat-fixes

## Issue Summary
Users are seeing:
1. Streamlit deprecation warnings for `use_container_width`.
2. Unexpected `DeltaGenerator` object/protobuf helper output rendered in the app in some topics.

## Root Cause
- Deprecated parameter usage remains in `app.py` for `st.pyplot` and `st.button`.
- In `_render_node`, a conditional expression evaluates Streamlit calls inline (`st.latex(...) if ... else st.markdown(...)`), which can leak return objects in Streamlit's display pipeline.

## Intended Changes
- Replace all `use_container_width=True` with `width="stretch"` in `app.py`.
- Refactor `_render_node` text branch to explicit `if/else` statements.
- Keep UI behavior and layout otherwise unchanged.

## Validation Plan
- Run: `conda run -n math python -m pytest -q tests`
- Run a quick Streamlit smoke check and inspect startup/output logs for:
  - absence of `use_container_width` deprecation messages
  - absence of rendered/printed `DeltaGenerator` output

## Commit Strategy
1. `fix(streamlit-api): replace deprecated use_container_width with width=stretch`
2. `fix(renderer): prevent DeltaGenerator output from text-node conditional rendering`
3. `docs(plan): add dated implementation plan for streamlit warning/render fixes`
4. `docs(report): add dated implementation report with validation results`
