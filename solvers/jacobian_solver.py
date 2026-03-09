"""
solvers/jacobian_solver.py
Computes the Jacobian matrix ∂(u,v)/∂(x,y) and checks for functional dependence.
"""
import sympy as sp


def jacobian_steps(prob: dict) -> list:
    """
    prob keys: u, v, variables
    """
    u = prob["u"]
    v = prob["v"]
    x, y = prob["variables"]
    steps = []

    steps.append({
        "type": "latex",
        "label": "**Given functions:**",
        "value": r"u = " + sp.latex(u) + r",\quad v = " + sp.latex(v),
        "hint": "Write down the two functions u(x, y) and v(x, y).",
    })

    # Compute partials
    u_x = sp.diff(u, x)
    u_y = sp.diff(u, y)
    v_x = sp.diff(v, x)
    v_y = sp.diff(v, y)

    steps.append({
        "type": "latex",
        "label": r"**Partial derivatives** of $u$:",
        "value": r"\frac{\partial u}{\partial x} = " + sp.latex(u_x) +
                 r",\quad \frac{\partial u}{\partial y} = " + sp.latex(u_y),
        "hint": "Compute ∂u/∂x and ∂u/∂y.",
    })
    steps.append({
        "type": "latex",
        "label": r"**Partial derivatives** of $v$:",
        "value": r"\frac{\partial v}{\partial x} = " + sp.latex(v_x) +
                 r",\quad \frac{\partial v}{\partial y} = " + sp.latex(v_y),
        "hint": "Compute ∂v/∂x and ∂v/∂y.",
    })

    # Jacobian matrix
    J = sp.Matrix([[u_x, u_y], [v_x, v_y]])
    steps.append({
        "type": "matrix",
        "label": r"**Jacobian matrix** $J = \frac{\partial(u,v)}{\partial(x,y)}$:",
        "value": J,
        "hint": "Arrange the partial derivatives as a 2×2 matrix.",
    })

    # Determinant
    det_J = sp.simplify(J.det())
    steps.append({
        "type": "latex",
        "label": r"**Jacobian determinant** $\det(J)$:",
        "value": r"\det(J) = " + sp.latex(det_J),
        "hint": "Compute the determinant of J. If det(J) = 0, u and v are functionally dependent.",
    })

    # Functional dependence
    if sp.simplify(det_J) == 0:
        conclusion = r"\det(J) = 0 \Rightarrow u \text{ and } v \text{ are \textbf{functionally dependent}.}"
    else:
        conclusion = r"\det(J) \neq 0 \Rightarrow u \text{ and } v \text{ are \textbf{functionally independent}.}"

    steps.append({
        "type": "text",
        "label": "**Conclusion:**",
        "value": conclusion,
        "hint": "A zero Jacobian determinant implies one function can be expressed in terms of the other.",
    })

    return steps
