"""
solvers/taylor_maclaurin_solver.py
Multivariable Taylor expansion of f(x,y) around a given point to degree 2.
"""
import sympy as sp
from itertools import product


def taylor_steps(prob: dict) -> list:
    """
    prob keys: function, variables, point, order
    """
    f = prob["function"]
    x, y = prob["variables"]
    x0, y0 = prob["point"]
    order = prob["order"]
    steps = []

    kind = "Maclaurin" if (x0 == 0 and y0 == 0) else "Taylor"

    steps.append({
        "type": "latex",
        "label": f"**{kind} expansion** of $f(x,y)$ about $(x_0, y_0) = ({x0}, {y0})$ to degree {order}:",
        "value": sp.latex(f),
        "hint": f"We expand f about the point ({x0}, {y0}) using the multivariable Taylor formula.",
    })

    # Evaluate f at the expansion point
    f0 = f.subs([(x, x0), (y, y0)])
    steps.append({
        "type": "latex",
        "label": f"$f({x0}, {y0})$:",
        "value": sp.latex(f0),
        "hint": "Evaluate f at the expansion point.",
    })

    # First-order partials
    fx = sp.diff(f, x).subs([(x, x0), (y, y0)])
    fy = sp.diff(f, y).subs([(x, x0), (y, y0)])
    steps.append({
        "type": "latex",
        "label": r"**First-order partials** at the point:",
        "value": r"f_x = " + sp.latex(fx) + r",\quad f_y = " + sp.latex(fy),
        "hint": "Compute partial derivatives and evaluate at the expansion point.",
    })

    # Second-order partials
    fxx = sp.diff(f, x, 2).subs([(x, x0), (y, y0)])
    fyy = sp.diff(f, y, 2).subs([(x, x0), (y, y0)])
    fxy = sp.diff(f, x, y).subs([(x, x0), (y, y0)])
    steps.append({
        "type": "latex",
        "label": r"**Second-order partials** at the point:",
        "value": r"f_{xx} = " + sp.latex(fxx) + r",\quad f_{yy} = " + sp.latex(fyy) +
                 r",\quad f_{xy} = " + sp.latex(fxy),
        "hint": "Compute all second-order partial derivatives and evaluate at the expansion point.",
    })

    # Assemble Taylor expansion
    dx = sp.Symbol("h") if x0 == 0 else (x - x0)
    dy = sp.Symbol("k") if y0 == 0 else (y - y0)
    expansion = (f0 + fx * (x - x0) + fy * (y - y0) +
                 sp.Rational(1, 2) * (fxx * (x - x0)**2 +
                                      2 * fxy * (x - x0) * (y - y0) +
                                      fyy * (y - y0)**2))
    expansion_simplified = sp.expand(expansion)
    steps.append({
        "type": "latex",
        "label": f"**{kind} series** (assembled):",
        "value": (r"f(x,y) \approx " + sp.latex(expansion_simplified)),
        "hint": "Substitute the evaluated partials into the Taylor formula.",
    })

    return steps
