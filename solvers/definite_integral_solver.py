"""
solvers/definite_integral_solver.py
Evaluates I(t) = integral_0^t f(x) dx and demonstrates the Fundamental Theorem
of Calculus / Leibniz rule.
"""
import sympy as sp


def definite_integral_steps(prob: dict) -> list:
    """
    prob keys: integrand, variable, parameter, lower, upper
    """
    integrand = prob["integrand"]
    x = prob["variable"]
    t = prob["parameter"]
    lower = prob["lower"]
    upper = prob["upper"]
    steps = []

    steps.append({
        "type": "latex",
        "label": r"**Evaluate** $I(t) = \int_{" + sp.latex(lower) + r"}^{" + sp.latex(upper) + r"} f(x)\, dx$ **and find** $I'(t)$:",
        "value": r"I(t) = \int_{" + sp.latex(lower) + r"}^{" + sp.latex(upper) +
                 r"} \left(" + sp.latex(integrand) + r"\right)\, dx",
        "hint": "Write down the definite integral I(t) with the moving upper limit.",
    })

    # Leibniz rule with a moving upper limit.
    df_dt = sp.diff(integrand, t)
    boundary_term = sp.simplify(integrand.subs(x, upper) * sp.diff(upper, t))
    integral_term = sp.integrate(df_dt, (x, lower, upper))
    leibniz_rhs = sp.simplify(boundary_term + integral_term)
    steps.append({
        "type": "latex",
        "label": r"**Leibniz rule / Fundamental Theorem:**",
        "value": (
            r"\frac{d}{dt}\left[\int_{"
            + sp.latex(lower)
            + r"}^{"
            + sp.latex(upper)
            + r"} f(x)\, dx\right] = "
            + sp.latex(leibniz_rhs)
        ),
        "hint": "Account for the upper-limit term and any explicit t-dependence in the integrand.",
    })

    steps.append({
        "type": "latex",
        "label": r"**Therefore:**",
        "value": r"I'(t) = " + sp.latex(leibniz_rhs),
        "hint": "The derivative is the simplified Leibniz result.",
    })

    # Evaluate I(t) directly
    I_t = sp.integrate(integrand, (x, lower, upper))
    I_t_simplified = sp.simplify(I_t)
    steps.append({
        "type": "latex",
        "label": r"**Direct evaluation** $I(t)$:",
        "value": r"I(t) = " + sp.latex(I_t_simplified),
        "hint": "Compute the definite integral directly to get the closed-form I(t).",
    })

    I_prime = sp.diff(I_t_simplified, t)
    steps.append({
        "type": "latex",
        "label": r"**Differentiate** $I(t)$ w.r.t. $t$ to verify Leibniz:",
        "value": r"I'(t) = " + sp.latex(sp.simplify(I_prime)),
        "hint": "Differentiate the closed-form I(t) to confirm the Leibniz result.",
    })

    return steps
