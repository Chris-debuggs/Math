"""
solvers/quadratic_form_solver.py
Orthogonal reduction of a real symmetric matrix quadratic form to canonical form.
"""
import sympy as sp

try:
    from sympy.matrices import GramSchmidt
except ImportError:  # pragma: no cover
    from sympy.matrices.dense import GramSchmidt


def quadratic_form_steps(A: sp.Matrix) -> list:
    """
    A must be a real symmetric matrix.
    Returns AST steps: display A, eigenvalues, modal matrix P, canonical form.
    """
    if isinstance(A, dict):
        A = A["matrix"]

    n = A.shape[0]
    lam = sp.Symbol(r"\lambda")
    steps = []

    # Variable names for display
    var_names = ["x", "y", "z"][:n]
    vars_sym = sp.symbols(" ".join(var_names), real=True)
    if n == 2:
        vars_sym = (vars_sym[0], vars_sym[1])
    x_vec = sp.Matrix(list(vars_sym))

    # Step 1 - quadratic form x^T A x
    qf_expr = sp.expand((x_vec.T * A * x_vec)[0, 0])
    steps.append({
        "type": "latex",
        "label": "**Quadratic form** $Q = x^T A x$:",
        "value": sp.latex(qf_expr),
        "hint": "Write the quadratic form Q = x^T A x where A is the symmetric matrix of coefficients.",
    })
    steps.append({
        "type": "matrix",
        "label": "**Symmetric matrix** $A$:",
        "value": A,
        "hint": "Identify the symmetric matrix A associated with the quadratic form.",
    })

    # Step 2 - characteristic polynomial
    char_poly = sp.expand((A - lam * sp.eye(n)).det())
    steps.append({
        "type": "polynomial",
        "label": r"**Characteristic equation** $\det(A - \lambda I) = 0$:",
        "value": char_poly,
        "hint": "Compute det(A - lambda I) = 0 to find eigenvalues.",
    })

    # Step 3 - eigenvalues
    eigenvals = sorted(A.eigenvals().keys(), key=lambda v: float(sp.N(v)))
    steps.append({
        "type": "solution_set",
        "label": "**Eigenvalues:**",
        "value": eigenvals,
        "hint": "Solve the characteristic equation for lambda.",
    })

    # Step 4 - orthonormal eigenvectors (modal matrix)
    eigvecs = []
    for ev in eigenvals:
        null = (A - ev * sp.eye(n)).nullspace()
        eigvecs.extend(sp.Matrix(v) for v in null)

    ortho_vecs = GramSchmidt(eigvecs, orthonormal=True)
    P = sp.Matrix.hstack(*ortho_vecs)
    steps.append({
        "type": "matrix",
        "label": "**Orthonormal modal matrix** $P$ (columns = unit eigenvectors):",
        "value": P,
        "hint": "Orthonormalize the eigenvectors and form the modal matrix P.",
    })

    # Step 5 - canonical form D = P^T A P
    D = sp.simplify(P.T * A * P)
    canon_terms = " + ".join(
        f"{sp.latex(D[i, i])} y_{i + 1}^2" for i in range(n) if D[i, i] != 0
    )
    steps.append({
        "type": "matrix",
        "label": r"**Canonical form** $D = P^T A P$ (diagonal):",
        "value": D,
        "hint": "Apply the orthogonal substitution x = Py to diagonalise the quadratic form.",
    })
    steps.append({
        "type": "latex",
        "label": "**Canonical quadratic form** $Q = y^T D y$:",
        "value": canon_terms,
        "hint": "The canonical form contains only squared terms with eigenvalue coefficients.",
    })

    # Step 6 - nature classification
    signs = [D[i, i] for i in range(n)]
    if all(s > 0 for s in signs):
        nature = "Positive Definite"
    elif all(s < 0 for s in signs):
        nature = "Negative Definite"
    elif all(s >= 0 for s in signs):
        nature = "Positive Semi-Definite"
    elif all(s <= 0 for s in signs):
        nature = "Negative Semi-Definite"
    else:
        nature = "Indefinite"

    steps.append({
        "type": "text",
        "label": f"**Nature of the quadratic form:** {nature}",
        "value": nature,
        "hint": "Check the signs of the eigenvalues: all positive -> Positive Definite, all negative -> Negative Definite, mixed -> Indefinite.",
    })

    return steps
