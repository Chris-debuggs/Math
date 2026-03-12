"""Matplotlib-based visuals for linear transformations and multivariable extrema."""

from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
import sympy as sp


def plot_linear_transformation_2d(A: sp.Matrix) -> plt.Figure:
    """Plot the action of a 2x2 matrix on basis vectors and the unit square."""
    if isinstance(A, dict):
        A = A["matrix"]
    if A.shape != (2, 2):
        raise ValueError("Linear transformation plot currently supports only 2x2 matrices.")

    matrix = np.array(A.tolist(), dtype=float)
    origin = np.array([[0.0], [0.0]])
    e1 = np.array([[1.0], [0.0]])
    e2 = np.array([[0.0], [1.0]])
    te1 = matrix @ e1
    te2 = matrix @ e2

    square = np.array(
        [[0.0, 0.0], [1.0, 0.0], [1.0, 1.0], [0.0, 1.0], [0.0, 0.0]],
        dtype=float,
    )
    transformed_square = (matrix @ square.T).T

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.plot(square[:, 0], square[:, 1], "o-", linewidth=2.0, label="Original unit square")
    ax.plot(
        transformed_square[:, 0],
        transformed_square[:, 1],
        "o-",
        linewidth=2.0,
        label="Transformed square",
    )

    ax.quiver(
        origin[0], origin[1], e1[0], e1[1],
        angles="xy", scale_units="xy", scale=1, color="tab:blue", label="e1",
    )
    ax.quiver(
        origin[0], origin[1], e2[0], e2[1],
        angles="xy", scale_units="xy", scale=1, color="tab:orange", label="e2",
    )
    ax.quiver(
        origin[0], origin[1], te1[0], te1[1],
        angles="xy", scale_units="xy", scale=1, color="tab:green", label="A*e1",
    )
    ax.quiver(
        origin[0], origin[1], te2[0], te2[1],
        angles="xy", scale_units="xy", scale=1, color="tab:red", label="A*e2",
    )

    points = np.vstack([square, transformed_square])
    extent = float(max(2.0, np.max(np.abs(points)) + 0.5))
    ax.set_xlim(-extent, extent)
    ax.set_ylim(-extent, extent)
    ax.set_aspect("equal")
    ax.grid(alpha=0.3)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title("2D Linear Transformation")
    ax.legend(loc="upper left")
    fig.tight_layout()
    return fig


def plot_maxima_surface(
    f: sp.Expr,
    variables: tuple,
    span: float = 3.0,
    samples: int = 70,
) -> plt.Figure:
    """Plot z = f(x,y) and mark real critical points from first-order conditions."""
    x, y = variables
    f_num = sp.lambdify((x, y), f, "numpy")

    xs = np.linspace(-span, span, samples)
    ys = np.linspace(-span, span, samples)
    X, Y = np.meshgrid(xs, ys)
    Z = np.asarray(f_num(X, Y), dtype=float)

    fig = plt.figure(figsize=(8, 5.5))
    ax = fig.add_subplot(111, projection="3d")
    ax.plot_surface(X, Y, Z, cmap="viridis", alpha=0.85, linewidth=0)

    fx = sp.diff(f, x)
    fy = sp.diff(f, y)
    critical_points = sp.solve([fx, fy], [x, y], dict=True)
    for point in critical_points:
        px = point[x]
        py = point[y]
        if not (sp.im(px) == 0 and sp.im(py) == 0):
            continue
        px_float = float(sp.N(px))
        py_float = float(sp.N(py))
        pz_float = float(sp.N(f.subs({x: px, y: py})))
        ax.scatter(px_float, py_float, pz_float, c="red", s=45)

    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("f(x, y)")
    ax.set_title("Surface and critical points")
    fig.tight_layout()
    return fig

