"""
solvers/definite_integral_solver.py
Evaluates I(t) = ∫_{lower}^{upper} f(x,t) dx and demonstrates Leibniz rule.
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
        "label": r"**Evaluate** $I(t) = \int_{\alpha}^{\beta} f(x,t)\, dx$ **and find** $I'(t)$:",
        "value": r"I(t) = \int_{" + sp.latex(lower) + r"}^{" + sp.latex(upper) +
                 r"} \left(" + sp.latex(integrand) + r"\right)\, dx",
        "hint": "Write down the integral I(t) whose derivative we want to find using Leibniz rule.",
    })

    # Leibniz rule: dI/dt = d/dt ∫ f dx = ∫ ∂f/∂t dx  (for constant limits wrt t)
    df_dt = sp.diff(integrand, t)
    steps.append({
        "type": "latex",
        "label": r"**Leibniz Rule:** $I'(t) = \int \frac{\partial f}{\partial t}\, dx$",
        "value": r"\frac{d}{dt}\left[" + sp.latex(integrand) + r"\right] = " + sp.latex(df_dt),
        "hint": "Differentiate f(x,t) partially with respect to t (treating x as a constant).",
    })

    steps.append({
        "type": "latex",
        "label": r"**Therefore:**",
        "value": r"I'(t) = \int_{" + sp.latex(lower) + r"}^{" + sp.latex(upper) +
                 r"} \left(" + sp.latex(df_dt) + r"\right)\, dx",
        "hint": "Place the differentiated integrand back under the integral sign.",
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
