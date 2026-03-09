"""
solvers/limit_continuity_solver.py
Step-by-step L'Hôpital / direct substitution limit solver.
"""
import sympy as sp


def limit_steps(prob: dict) -> list:
    """
    prob keys: expr, numerator, denominator, variable, point, expected
    """
    num = prob["numerator"]
    den = prob["denominator"]
    var = prob["variable"]
    pt = prob["point"]
    steps = []

    steps.append({
        "type": "latex",
        "label": "**Evaluate the limit:**",
        "value": r"\lim_{" + sp.latex(var) + r" \to " + sp.latex(pt) + r"} \frac{" +
                 sp.latex(num) + r"}{" + sp.latex(den) + r"}",
        "hint": "Write down the limit expression.",
    })

    # Try direct substitution
    num_val = num.subs(var, pt)
    den_val = den.subs(var, pt)

    steps.append({
        "type": "latex",
        "label": "**Step 1 — Direct substitution** (check for indeterminate form):",
        "value": r"\text{Numerator} = " + sp.latex(num_val) +
                 r",\quad \text{Denominator} = " + sp.latex(den_val),
        "hint": "Substitute the limit point directly. If you get 0/0 or ∞/∞, L'Hôpital applies.",
    })

    if num_val == 0 and den_val == 0:
        # Apply L'Hôpital
        dnum = sp.diff(num, var)
        dden = sp.diff(den, var)
        steps.append({
            "type": "latex",
            "label": r"**Indeterminate form** $\frac{0}{0}$ — apply **L'Hôpital's Rule**:",
            "value": r"\lim_{" + sp.latex(var) + r" \to " + sp.latex(pt) + r"} \frac{" +
                     sp.latex(num) + r"}{" + sp.latex(den) + r"} = \lim \frac{" +
                     sp.latex(dnum) + r"}{" + sp.latex(dden) + r"}",
            "hint": "Differentiate numerator and denominator separately, then re-evaluate.",
        })
        limit_val = sp.limit(num / den, var, pt)
        steps.append({
            "type": "latex",
            "label": "**Result after L'Hôpital:**",
            "value": r"\lim_{" + sp.latex(var) + r" \to " + sp.latex(pt) + r"} \frac{" +
                     sp.latex(num) + r"}{" + sp.latex(den) + r"} = " + sp.latex(limit_val),
            "hint": "Substitute the limit point into the differentiated expression.",
        })
    else:
        limit_val = num_val / den_val if den_val != 0 else sp.oo
        steps.append({
            "type": "latex",
            "label": "**Direct substitution succeeds — limit is:**",
            "value": sp.latex(limit_val),
            "hint": "No indeterminate form; the limit equals the direct substitution value.",
        })

    return steps
