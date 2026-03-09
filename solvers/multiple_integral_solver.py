"""
solvers/multiple_integral_solver.py
Evaluates a double integral ∫∫ f(x,y) dy dx with constant limits step-by-step.
"""
import sympy as sp


def multiple_integral_steps(prob: dict) -> list:
    """
    prob keys: integrand, variables, bounds_x, bounds_y
    """
    f = prob["integrand"]
    x, y = prob["variables"]
    ax, bx = prob["bounds_x"]
    ay, by = prob["bounds_y"]
    steps = []

    steps.append({
        "type": "latex",
        "label": "**Evaluate the double integral:**",
        "value": r"\int_{" + sp.latex(ax) + r"}^{" + sp.latex(bx) +
                 r"} \int_{" + sp.latex(ay) + r"}^{" + sp.latex(by) +
                 r"} \left(" + sp.latex(f) + r"\right)\, dy\, dx",
        "hint": "We evaluate the iterated integral from the inside out, starting with the y-integral.",
    })

    # Inner integral wrt y
    inner_antideriv = sp.integrate(f, y)
    steps.append({
        "type": "latex",
        "label": r"**Step 1 — Antiderivative** w.r.t. $y$:",
        "value": r"\int \left(" + sp.latex(f) + r"\right)\, dy = " +
                 sp.latex(inner_antideriv),
        "hint": "Integrate f(x, y) with respect to y, treating x as a constant.",
    })

    inner_result = sp.simplify(inner_antideriv.subs(y, by) - inner_antideriv.subs(y, ay))
    steps.append({
        "type": "latex",
        "label": r"**Step 1 — Apply limits** $y \in [" + sp.latex(ay) + r", " + sp.latex(by) + r"]$:",
        "value": r"\left[" + sp.latex(inner_antideriv) + r"\right]_{" +
                 sp.latex(ay) + r"}^{" + sp.latex(by) + r"} = " + sp.latex(inner_result),
        "hint": "Substitute the y-limits into the antiderivative and simplify.",
    })

    # Outer integral wrt x
    outer_antideriv = sp.integrate(inner_result, x)
    steps.append({
        "type": "latex",
        "label": r"**Step 2 — Antiderivative** w.r.t. $x$:",
        "value": r"\int \left(" + sp.latex(inner_result) + r"\right)\, dx = " +
                 sp.latex(outer_antideriv),
        "hint": "Now integrate the result of the y-integral with respect to x.",
    })

    final_result = sp.simplify(outer_antideriv.subs(x, bx) - outer_antideriv.subs(x, ax))
    steps.append({
        "type": "latex",
        "label": r"**Step 2 — Apply limits** $x \in [" + sp.latex(ax) + r", " + sp.latex(bx) + r"]$:",
        "value": r"\left[" + sp.latex(outer_antideriv) + r"\right]_{" +
                 sp.latex(ax) + r"}^{" + sp.latex(bx) + r"} = " + sp.latex(final_result),
        "hint": "Substitute the x-limits into the antiderivative to get the final numerical result.",
    })

    steps.append({
        "type": "latex",
        "label": "**Final answer:**",
        "value": r"\iint f\, dA = " + sp.latex(sp.simplify(final_result)),
        "hint": "The double integral evaluates to this number.",
    })

    return steps
