"""
solvers/eigen_solver.py
Deterministic walkthrough: characteristic polynomial → eigenvalues → eigenvectors.
Returns a list of AST node dicts renderable by the Streamlit UI.
"""
import sympy as sp


def eigen_steps(A: sp.Matrix) -> list:
    """
    Parameters
    ----------
    A : sympy.Matrix  — square matrix (2×2 or 3×3)

    Returns
    -------
    list of dicts with keys: type, label, value, hint
    """
    n = A.shape[0]
    lam = sp.Symbol(r"\lambda")
    steps = []

    # Step 1 — display the matrix
    steps.append({
        "type": "matrix",
        "label": "**Given matrix** $A$:",
        "value": A,
        "hint": "Write down the matrix A whose eigenvalues we want to find.",
    })

    # Step 2 — characteristic matrix (A - λI)
    char_mat = A - lam * sp.eye(n)
    steps.append({
        "type": "matrix",
        "label": r"**Characteristic matrix** $A - \lambda I$:",
        "value": char_mat,
        "hint": r"Form $A - \lambda I$ by subtracting $\lambda$ from each diagonal entry.",
    })

    # Step 3 — characteristic polynomial
    char_poly = char_mat.det()
    char_poly_expanded = sp.expand(char_poly)
    steps.append({
        "type": "polynomial",
        "label": r"**Characteristic equation** $\det(A - \lambda I) = 0$:",
        "value": char_poly_expanded,
        "hint": "Compute the determinant and set it equal to zero.",
    })

    # Step 4 — factor and find eigenvalues
    factored = sp.factor(char_poly_expanded)
    eigenvals = sorted(sp.solve(char_poly_expanded, lam), key=lambda v: sp.re(v))
    steps.append({
        "type": "factored_poly",
        "label": "**Factored characteristic polynomial:**",
        "value": factored,
        "hint": "Factor the polynomial to read off the roots.",
    })
    steps.append({
        "type": "solution_set",
        "label": "**Eigenvalues** $\\lambda$:",
        "value": eigenvals,
        "hint": "The roots of the characteristic polynomial are the eigenvalues.",
    })

    # Steps 5+ — eigenvectors for each eigenvalue
    lam_sym = sp.Symbol("lambda")
    for ev in eigenvals:
        ev_matrix = A - ev * sp.eye(n)
        steps.append({
            "type": "matrix",
            "label": f"**For** $\\lambda = {sp.latex(ev)}$: row-reduce $(A - \\lambda I)$",
            "value": ev_matrix,
            "hint": f"Substitute λ = {ev} into (A − λI) and perform row reduction.",
        })
        rref_mat, pivots = ev_matrix.rref()
        steps.append({
            "type": "matrix",
            "label": f"**RREF of** $(A - {sp.latex(ev)} I)$:",
            "value": rref_mat,
            "hint": "Row-reduce to echelon form to find the null space.",
        })
        null = ev_matrix.nullspace()
        for i, vec in enumerate(null):
            steps.append({
                "type": "vector",
                "label": f"**Eigenvector** $v_{i+1}$ for $\\lambda = {sp.latex(ev)}$:",
                "value": vec,
                "hint": "The null space vector(s) are the eigenvectors for this eigenvalue.",
            })

    return steps
