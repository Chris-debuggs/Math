"""
solvers/partial_derivative_solver.py
Computes partial derivatives and verifies Euler's theorem for homogeneous functions.
"""
import sympy as sp


def partial_derivative_steps(prob: dict) -> list:
    """
    prob keys: function, variables (tuple), degree
    """
    f = prob["function"]
    x, y = prob["variables"]
    n = prob["degree"]
    steps = []

    steps.append({
        "type": "latex",
        "label": "**Given function** $f(x, y)$:",
        "value": sp.latex(f),
        "hint": "Write down f(x, y). Check if it is homogeneous of some degree n.",
    })

    # Partial derivatives
    fx = sp.diff(f, x)
    fy = sp.diff(f, y)

    steps.append({
        "type": "latex",
        "label": r"**Partial derivative** $\frac{\partial f}{\partial x}$:",
        "value": sp.latex(fx),
        "hint": "Differentiate f with respect to x, treating y as a constant.",
    })
    steps.append({
        "type": "latex",
        "label": r"**Partial derivative** $\frac{\partial f}{\partial y}$:",
        "value": sp.latex(fy),
        "hint": "Differentiate f with respect to y, treating x as a constant.",
    })

    # Euler's theorem verification: x·fₓ + y·fᵧ = n·f
    lhs = sp.expand(x * fx + y * fy)
    rhs = sp.expand(n * f)
    euler_holds = sp.simplify(lhs - rhs) == 0

    steps.append({
        "type": "latex",
        "label": r"**Euler's theorem check** $x f_x + y f_y = n \cdot f$:",
        "value": sp.latex(x) + r" \cdot " + sp.latex(fx) + r" + " +
                 sp.latex(y) + r" \cdot " + sp.latex(fy) + r" = " + sp.latex(lhs),
        "hint": "Compute x·f_x + y·f_y. For a homogeneous function of degree n, this equals n·f.",
    })
    steps.append({
        "type": "latex",
        "label": f"**Right-hand side** $n \\cdot f = {n} \\cdot f$:",
        "value": sp.latex(rhs),
        "hint": f"The RHS is simply n times f, where n = {n} is the degree of homogeneity.",
    })
    steps.append({
        "type": "text",
        "label": "**Conclusion:**",
        "value": (
            r"\checkmark\; x f_x + y f_y = n f \text{ — Euler's theorem verified.}"
            if euler_holds else
            r"\times\; \text{Euler's theorem does NOT hold for this function.}"
        ),
        "hint": "If LHS = RHS, the function is homogeneous of degree n and Euler's theorem is verified.",
    })

    return steps
