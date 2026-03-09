"""
solvers/linear_ode_solver.py
Solves ay'' + by' + cy = g(x) step-by-step:
  1. Auxiliary equation
  2. Classification of roots and complementary function
  3. Particular integral (undetermined coefficients)
  4. General solution
"""
import sympy as sp


def linear_ode_steps(prob: dict) -> list:
    """
    prob keys: a, b, c, g, variable, mode
    """
    a_coeff = prob["a"]
    b_coeff = prob["b"]
    c_coeff = prob["c"]
    g = prob["g"]
    x = prob["variable"]
    mode = prob["mode"]
    steps = []

    # Display ODE
    steps.append({
        "type": "latex",
        "label": "**Solve the linear ODE:**",
        "value": (sp.latex(a_coeff) + r"y'' + " + sp.latex(b_coeff) + r"y' + " +
                  sp.latex(c_coeff) + r"y = " + sp.latex(g)),
        "hint": "Write the ODE in standard form ay'' + by' + cy = g(x).",
    })

    # Step 1 — Auxiliary equation
    m = sp.Symbol("m")
    aux = a_coeff * m**2 + b_coeff * m + c_coeff
    steps.append({
        "type": "polynomial",
        "label": r"**Step 1 — Auxiliary (characteristic) equation** $am^2 + bm + c = 0$:",
        "value": sp.expand(aux),
        "hint": "Replace y'' with m², y' with m, and y with 1. Solve for m.",
    })

    roots = sp.solve(aux, m)
    steps.append({
        "type": "latex",
        "label": "**Roots of auxiliary equation:**",
        "value": r"m = " + ",\; ".join(sp.latex(r) for r in roots),
        "hint": "Solve am² + bm + c = 0 using the quadratic formula or factoring.",
    })

    # Step 2 — Complementary function
    y = sp.Function("y")
    c1, c2 = sp.symbols("C_1 C_2")

    if mode == "distinct_real":
        m1, m2 = roots[0], roots[1]
        yc = c1 * sp.exp(m1 * x) + c2 * sp.exp(m2 * x)
        root_type = "Two distinct real roots"
    elif mode == "equal_real":
        m1 = roots[0]
        yc = (c1 + c2 * x) * sp.exp(m1 * x)
        root_type = "Repeated real root"
    else:
        # complex: α ± βi
        alpha = sp.re(roots[0])
        beta = sp.im(roots[0])
        yc = sp.exp(alpha * x) * (c1 * sp.cos(beta * x) + c2 * sp.sin(beta * x))
        root_type = "Complex conjugate roots"

    steps.append({
        "type": "text",
        "label": f"**Root type:** {root_type}",
        "value": r"\text{" + root_type + r"}",
        "hint": "Classify the roots: distinct real → two exponentials, repeated → xe^(mx), complex → e^(αx)(cos βx, sin βx).",
    })
    steps.append({
        "type": "latex",
        "label": r"**Complementary function** $y_c$:",
        "value": r"y_c = " + sp.latex(yc),
        "hint": "Write the complementary function using the appropriate form for the root type.",
    })

    # Step 3 — Particular integral (undetermined coefficients)
    if g == 0:
        yp = sp.Integer(0)
        steps.append({
            "type": "latex",
            "label": r"**Particular integral:** $g(x) = 0$, so $y_p = 0$.",
            "value": r"y_p = 0",
            "hint": "When g(x) = 0, the particular integral is trivially zero.",
        })
    else:
        try:
            yp = sp.dsolve(
                a_coeff * y(x).diff(x, 2) + b_coeff * y(x).diff(x) + c_coeff * y(x) - g,
                y(x), hint="undetermined_coefficients"
            ).rhs - (c1 * sp.exp(roots[0] * x) + c2 * sp.exp(roots[1] * x) if mode == "distinct_real" else sp.Integer(0))
        except Exception:
            # Fallback: use variation of parameters via SymPy dsolve
            try:
                sol = sp.dsolve(
                    a_coeff * y(x).diff(x, 2) + b_coeff * y(x).diff(x) + c_coeff * y(x) - g,
                    y(x)
                )
                # Extract particular part by subtracting complementary
                yp_raw = sol.rhs
                # Replace integration constants with 0 to isolate yp
                yp = yp_raw.subs([(sp.Symbol("C1"), 0), (sp.Symbol("C2"), 0)])
            except Exception:
                yp = sp.Integer(0)

        steps.append({
            "type": "latex",
            "label": r"**Step 3 — Particular integral** (undetermined coefficients):",
            "value": r"y_p = " + sp.latex(sp.simplify(yp)),
            "hint": "Assume a trial solution of the same form as g(x). Substitute into the ODE and match coefficients.",
        })

    # Step 4 — General solution
    y_gen = sp.expand(yc + yp)
    steps.append({
        "type": "latex",
        "label": r"**Step 4 — General solution** $y = y_c + y_p$:",
        "value": r"y = " + sp.latex(y_gen),
        "hint": "The general solution is the sum of the complementary function and the particular integral.",
    })

    return steps
