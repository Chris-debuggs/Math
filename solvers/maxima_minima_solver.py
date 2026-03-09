"""
solvers/maxima_minima_solver.py
Finds and classifies critical points of f(x,y) using the second-derivative test.
"""
import sympy as sp


def maxima_minima_steps(prob: dict) -> list:
    """
    prob keys: function, variables
    """
    f = prob["function"]
    x, y = prob["variables"]
    steps = []

    steps.append({
        "type": "latex",
        "label": "**Find critical points of** $f(x,y)$:",
        "value": sp.latex(f),
        "hint": "We find where both partial derivatives are zero — these are the critical points.",
    })

    # Partial derivatives
    fx = sp.diff(f, x)
    fy = sp.diff(f, y)
    steps.append({
        "type": "latex",
        "label": r"**Set** $f_x = 0$ **and** $f_y = 0$:",
        "value": r"f_x = " + sp.latex(fx) + r" = 0,\quad f_y = " + sp.latex(fy) + r" = 0",
        "hint": "Differentiate f with respect to x and y, then set each equal to zero.",
    })

    # Solve for critical points
    critical_pts = sp.solve([fx, fy], [x, y], dict=True)
    if not critical_pts:
        steps.append({
            "type": "text",
            "label": "**No real critical points found.**",
            "value": r"\text{No real critical points.}",
            "hint": "Check the system of equations — it may have no real solutions.",
        })
        return steps

    steps.append({
        "type": "text",
        "label": f"**Critical points:** {', '.join(str(pt) for pt in critical_pts)}",
        "value": r"\text{Critical points: } " + ", ".join(
            r"(" + sp.latex(pt[x]) + r", " + sp.latex(pt[y]) + r")" for pt in critical_pts),
        "hint": "Solve the system fₓ = 0 and fᵧ = 0 simultaneously.",
    })

    # Second-order partials
    fxx = sp.diff(f, x, 2)
    fyy = sp.diff(f, y, 2)
    fxy = sp.diff(f, x, y)
    steps.append({
        "type": "latex",
        "label": "**Second-order partial derivatives:**",
        "value": r"f_{xx} = " + sp.latex(fxx) +
                 r",\quad f_{yy} = " + sp.latex(fyy) +
                 r",\quad f_{xy} = " + sp.latex(fxy),
        "hint": "Compute all second-order partials needed for the discriminant test.",
    })

    # Classify each critical point
    for pt in critical_pts:
        A = fxx.subs(list(pt.items()))
        B = fxy.subs(list(pt.items()))
        C = fyy.subs(list(pt.items()))
        D = A * C - B**2

        pt_str = r"(" + sp.latex(pt[x]) + r", " + sp.latex(pt[y]) + r")"
        steps.append({
            "type": "latex",
            "label": f"**At** ${pt_str}$: discriminant $\\Delta = f_{{xx}} f_{{yy}} - (f_{{xy}})^2$",
            "value": r"A = " + sp.latex(A) + r",\quad B = " + sp.latex(B) +
                     r",\quad C = " + sp.latex(C) +
                     r",\quad \Delta = " + sp.latex(D),
            "hint": "Evaluate fₓₓ, fᵧᵧ, fₓᵧ at the critical point and compute Δ = AC − B².",
        })

        if D > 0 and A > 0:
            nature = r"\text{Local \textbf{minimum}}"
        elif D > 0 and A < 0:
            nature = r"\text{Local \textbf{maximum}}"
        elif D < 0:
            nature = r"\text{\textbf{Saddle point}}"
        else:
            nature = r"\text{Test inconclusive}"

        steps.append({
            "type": "latex",
            "label": f"**Classification at** ${pt_str}$:",
            "value": nature,
            "hint": "Δ > 0 and A > 0 → minimum. Δ > 0 and A < 0 → maximum. Δ < 0 → saddle point.",
        })

    return steps
