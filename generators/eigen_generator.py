"""
generators/eigen_generator.py
Generates eigenvalue problems A = P D P^{-1} with distinct integer eigenvalues.
The unimodular matrix P (det=1) guarantees integer entries in A.
Supports 2x2 and 3x3 matrices.
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

    # A = P D P^{-1}  - integer entries because det(P) = 1
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
    Generate a 2x2 or 3x3 real symmetric matrix suitable for quadratic form
    reduction. Built as A = Q^T D Q with an integer matrix Q and diagonal D.
    """
    dim = random.choice([2, 3])
    eigenvals = random.sample(range(-4, 6), dim)
    D = sp.diag(*eigenvals)

    # Simple symmetric-friendly integer matrix via A = Q^T D Q.
    Q = sp.eye(dim)
    for i in range(1, dim):
        for j in range(i):
            Q[i, j] = random.randint(-1, 1)
    A = Q.T * D * Q   # symmetric by construction since D is diagonal

    actual_eigenvals = sorted(
        A.eigenvals().keys(),
        key=lambda v: float(sp.N(v)),
    )

    return {
        "topic": "quadratic_form",
        "matrix": A,
        "dim": dim,
        "expected_eigenvals": actual_eigenvals,
    }
