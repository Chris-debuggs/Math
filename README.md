# MA3151 Deterministic CAS Tutoring Engine

## Overview
The **MA3151 Deterministic CAS Tutoring Engine** is an interactive, educational web application built using Python, Streamlit, and SymPy. It acts as an automated, step-by-step math tutor primarily focused on university-level matrices and calculus. The application breaks down complex mathematical problems into an interactive state machine, offering structured pedagogical guidance, theory flashcards, and geometric visualisations to support learning.

## Key Features
- **Deterministic Step-by-Step Solvers**: Uses SymPy, a Python library for symbolic mathematics, to evaluate problems and construct rigorous Abstract Syntax Trees (ASTs) of step-by-step solutions without hallucinations.
- **Interactive UI**: An intuitive Streamlit interface featuring topic selection, step-navigation (Next/Previous step buttons), "Show All" rendering, and state preservation.
- **Visual Intuition Mode**: Displays visual geometric interpretations of problems, such as 2D matrix transformations and eigenvectors plots, as well as 3D surface charts with critical points for maxima/minima (powered by Matplotlib).
- **Concept & Foundation Cards**: Syllabus-aligned theory cards and exam checklists contextually mapped to the active topic to reinforce core concepts and fundamentals.
- **Pedagogical Hint Mode**: An integrated toggle that embeds focused hints underneath solution steps to naturally guide the student to the next logical step.

## Supported Topics
### Unit 1: Matrices
- Eigenvalues & Eigenvectors (2×2 and 3×3)
- Cayley-Hamilton Theorem
- Quadratic Form — Canonical Reduction

### Unit 2: Differential Calculus
- Limits & L'Hôpital's Rule
- Partial Derivatives & Euler's Theorem
- Jacobian & Functional Dependence

### Unit 3: Series Expansions & Applications
- Taylor / Maclaurin Series (2-Variable)
- Maxima & Minima

### Unit 4: Integral Calculus
- Definite Integral & Leibniz Rule
- Double Integrals
- Change of Variables (Polar)

### Unit 5: Ordinary Differential Equations
- Linear 2nd-Order ODE

## Project Structure
- `app.py`: The main Streamlit entry point. Configures the UI layout, sets up the session-state machine, registers topic logic, and renders the pedagogical views.
- `generators/`: Holds independent functions designed to randomly generate "clean" maths problems complete with matrices, polynomials, or required differential definitions.
- `solvers/`: Contains step-by-step deterministic solving algorithms using SymPy. These yield a standardized AST of steps with localized hints, formats, and equations.
- `visualizers/`: Matplotlib plotting scripts built to visualize solutions like linear transformations and 3D function optimization grids.
- `content/`: Holds metadata related to concept cards, bridging the math solutions with theoretical syllabus requirements.
- `tests/`: Automated unit test coverage executing over problem generators, solvers, visuals, and theory card pipelines.
- `docs/`: Project documentation, historical implementation plans, CI/CD audits, and summaries.

## Installation & Usage

1. **Clone the repository:**
   ```bash
   git clone <repository_url>
   cd <repository_name>
   ```

2. **Set up a virtual environment (Recommended):**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On Mac/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   The project requires `streamlit`, `sympy`, and optionally `matplotlib` (for visualizers).
   ```bash
   pip install -r requirements.txt
   ```

4. **Launch the application:**
   ```bash
   streamlit run app.py
   ```
   *The Streamlit application will open in your default browser automatically at `http://localhost:8501/`.*

## Testing & CI
The repository uses standard Python validation tools driven by GitHub Actions CI. You can run checks locally via:

```bash
# Run unit tests utilizing pytest
python -m pytest -q tests

# Verify codebase integrity against critical syntax issues
python -m flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
```
