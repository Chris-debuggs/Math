"""
solvers/variable_change_solver.py
Change of variables: Cartesian → polar, showing Jacobian = r and evaluation.
"""
import sympy as sp


def variable_change_steps(prob: dict) -> list:
    """
    prob keys: integrand_cartesian, region, radius
    """
    f_cart = prob["integrand_cartesian"]
    region = prob["region"]
    R = prob["radius"]
    steps = []

    x, y = sp.symbols("x y", real=True)
    r, theta = sp.symbols("r theta", positive=True)

    steps.append({
        "type": "latex",
        "label": r"**Evaluate** $\iint_D f(x,y)\, dA$ **over** $D: " + region + r"$",
        "value": r"\iint_D \left(" + sp.latex(f_cart) + r"\right)\, dA",
        "hint": "Identify the domain D and notice it is a circular region — polar coordinates will simplify it.",
    })

    # Polar substitution
    steps.append({
        "type": "latex",
        "label": r"**Polar substitution:** $x = r\cos\theta,\; y = r\sin\theta$",
        "value": r"x = r\cos\theta, \quad y = r\sin\theta",
        "hint": "For circular regions, substitute x = r cos θ and y = r sin θ.",
    })

    # Jacobian
    steps.append({
        "type": "latex",
        "label": r"**Jacobian** $\left|\frac{\partial(x,y)}{\partial(r,\theta)}\right| = r$",
        "value": r"\frac{\partial(x,y)}{\partial(r,\theta)} = \begin{vmatrix} \cos\theta & -r\sin\theta \\ \sin\theta & r\cos\theta \end{vmatrix} = r",
        "hint": "The Jacobian of the polar transformation is r. This replaces dA with r dr dθ.",
    })

    # Convert integrand: x² + y² → r²
    f_polar = f_cart.subs([(x, r * sp.cos(theta)), (y, r * sp.sin(theta))])
    f_polar_simplified = sp.trigsimp(sp.expand(f_polar))
    steps.append({
        "type": "latex",
        "label": r"**Integrand in polar form** $f(r\cos\theta, r\sin\theta)$:",
        "value": sp.latex(f_polar_simplified),
        "hint": "Substitute x = r cos θ and y = r sin θ into the integrand using cos²θ + sin²θ = 1.",
    })

    # New limits
    steps.append({
        "type": "latex",
        "label": f"**New limits:** $r \\in [0, {sp.latex(R)}]$, $\\theta \\in [0, 2\\pi]$",
        "value": r"r \in [0," + sp.latex(R) + r"],\quad \theta \in [0, 2\pi]",
        "hint": "The circle x² + y² ≤ R² becomes r ∈ [0, R] and θ ∈ [0, 2π] in polar coordinates.",
    })

    # Polar iterated integral
    steps.append({
        "type": "latex",
        "label": r"**Polar iterated integral:**",
        "value": r"\int_0^{2\pi} \int_0^{" + sp.latex(R) + r"} \left(" +
                 sp.latex(f_polar_simplified) + r"\right) \cdot r\, dr\, d\theta",
        "hint": "Write the integral with the Jacobian factor r included.",
    })

    # Evaluate
    integrand_polar = f_polar_simplified * r
    inner = sp.integrate(integrand_polar, (r, 0, R))
    inner_simplified = sp.simplify(inner)
    steps.append({
        "type": "latex",
        "label": r"**Inner integral** w.r.t. $r$:",
        "value": r"\int_0^{" + sp.latex(R) + r"} \left(" + sp.latex(f_polar_simplified) +
                 r"\right) r\, dr = " + sp.latex(inner_simplified),
        "hint": "Integrate with respect to r first.",
    })

    outer = sp.integrate(inner_simplified, (theta, 0, 2 * sp.pi))
    result = sp.simplify(outer)
    steps.append({
        "type": "latex",
        "label": r"**Outer integral** w.r.t. $\theta$ — **final answer:**",
        "value": r"\int_0^{2\pi} \left(" + sp.latex(inner_simplified) +
                 r"\right)\, d\theta = " + sp.latex(result),
        "hint": "Integrate with respect to θ from 0 to 2π to get the final result.",
    })

    return steps
