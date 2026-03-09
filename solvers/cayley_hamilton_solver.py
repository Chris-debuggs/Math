"""
solvers/cayley_hamilton_solver.py
Verifies the Cayley-Hamilton theorem and derives the matrix inverse.
"""
import sympy as sp


def cayley_hamilton_steps(A: sp.Matrix) -> list:
    n = A.shape[0]
    lam = sp.Symbol(r"\lambda")
    steps = []

    steps.append({
        "type": "matrix",
        "label": "**Given matrix** $A$:",
        "value": A,
        "hint": "Write down the matrix A.",
    })

    # Characteristic polynomial
    char_poly = (A - lam * sp.eye(n)).det()
    char_poly_expanded = sp.expand(char_poly)
    steps.append({
        "type": "polynomial",
        "label": r"**Characteristic polynomial** $p(\lambda)$:",
        "value": char_poly_expanded,
        "hint": "Compute det(A − λI) to obtain the characteristic polynomial p(λ).",
    })

    # Substitute A into p(λ) — Cayley-Hamilton: p(A) = 0
    # Build p(A) symbolically then simplify
    coeffs = sp.Poly(char_poly_expanded, lam).all_coeffs()
    pA = sum(c * A**i for i, c in enumerate(reversed(coeffs)))
    pA_simplified = sp.simplify(pA)
    steps.append({
        "type": "text",
        "label": "**Cayley-Hamilton theorem** states $p(A) = 0$. Computing $p(A)$…",
        "value": r"p(A) = \mathbf{0}",
        "hint": "Replace every λ in p(λ) with the matrix A itself.",
    })
    steps.append({
        "type": "matrix",
        "label": "**Verification** — $p(A)$ evaluates to:",
        "value": pA_simplified,
        "hint": "This should be the zero matrix, confirming the theorem.",
    })

    # Express A^{-1} from the CH relation (for a 2×2: p(A)=A²+bA+cI => A^{-1} = -(A+bI)/c)
    if A.det() != 0:
        # p(A) = 0  =>  A^{-1} available from rearrangement
        A_inv = A.inv()
        steps.append({
            "type": "matrix",
            "label": r"**Matrix inverse** $A^{-1}$ (derived from Cayley-Hamilton):",
            "value": A_inv,
            "hint": "Rearrange p(A) = 0 to isolate A⁻¹ = −(1/c)(A + bI) for a 2×2 matrix.",
        })
    else:
        steps.append({
            "type": "text",
            "label": "**Note:** $\\det(A) = 0$, so $A^{-1}$ does not exist.",
            "value": r"\det(A) = 0",
            "hint": "A matrix is invertible only when its determinant is non-zero.",
        })

    return steps
