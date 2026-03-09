"""
generators/eigen_generator.py
Generates eigenvalue problems A = P D P^{-1} with distinct integer eigenvalues.
The unimodular matrix P (det=1) guarantees integer entries in A.
Supports 2×2 and 3×3 matrices.
"""
import random
import sympy as sp


def generate_clean_eigen_problem(dim: int = 2) -> dict:
    """Return a dict with keys: topic, matrix, dim, expected_roots."""
    if dim not in (2, 3):
        raise ValueError("dim must be 2 or 3")

    # Distinct eigenvalues to avoid defective matrices
    eigenvals = random.sample(range(-5, 6), dim)

    # Diagonal matrix of eigenvalues
    D = sp.diag(*eigenvals)

    # Lower-triangular unimodular matrix P (diagonal = 1, below-diag = random ints)
    P = sp.eye(dim)
    for i in range(1, dim):
        for j in range(i):
            P[i, j] = random.randint(-2, 2)

    # A = P D P^{-1}  — integer entries because det(P) = 1
    A = P * D * P.inv()

    return {
        "topic": "eigenvalues",
        "matrix": A,
        "dim": dim,
        "expected_roots": sorted(eigenvals),
    }


def generate_cayley_hamilton_problem(dim: int = 2) -> dict:
    """Return an eigen problem reused for Cayley-Hamilton verification."""
    prob = generate_clean_eigen_problem(dim)
    prob["topic"] = "cayley_hamilton"
    return prob


def generate_quadratic_form_problem() -> dict:
    """
    Generate a 2×2 or 3×3 real symmetric matrix suitable for quadratic form
    reduction.  Built as A = P D P^T where P is orthogonal (approx) — we use
    the eigen-construction trick and then symmetrise to keep integer entries.
    """
    dim = random.choice([2, 3])
    eigenvals = random.sample(range(-4, 6), dim)
    D = sp.diag(*eigenvals)

    # Simple symmetric-friendly integer matrix via S = L + L^T + D_shifted
    # Easier: just pick a symmetric matrix with known-clean determinant.
    # We construct A = Q^T D Q where Q is an integer matrix with det=±1.
    Q = sp.eye(dim)
    for i in range(1, dim):
        for j in range(i):
            Q[i, j] = random.randint(-1, 1)
    A = Q.T * D * Q   # symmetric by construction since D is diagonal

    return {
        "topic": "quadratic_form",
        "matrix": A,
        "dim": dim,
        "expected_eigenvals": sorted(eigenvals),
    }
