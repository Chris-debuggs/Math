"""
generators/calculus_generator.py
Generates clean calculus problems (limits, partial derivatives, Jacobians,
Taylor series, integrals, ODEs) with small-integer coefficients so that SymPy
always produces closed-form answers without ugly radicals.
"""
import random
import sympy as sp

x, y, z, t = sp.symbols("x y z t", real=True)
lam = sp.Symbol("lambda")


# ── helpers ──────────────────────────────────────────────────────────────────

def _rand(lo: int = 1, hi: int = 5) -> int:
    """Non-zero random integer in [lo, hi]."""
    v = random.randint(lo, hi)
    return v if v != 0 else 1


def _rand_coeff(lo: int = -4, hi: int = 4) -> int:
    """Random non-zero coefficient."""
    v = random.choice([i for i in range(lo, hi + 1) if i != 0])
    return v


# ── limit / L'Hôpital ────────────────────────────────────────────────────────

def generate_limit_problem() -> dict:
    """
    Generates a 0/0 indeterminate limit at x=a suitable for L'Hôpital.
    Form: (a·x² + b·x·(x-a)) / ((x-a)·(c·x + d))
    simplified to ensure limit at x=a is finite.
    """
    a = _rand_coeff(1, 4)
    b = _rand_coeff(1, 3)
    c = _rand_coeff(1, 3)
    d = _rand_coeff(1, 3)
    point = random.choice([0, 1, 2])

    # f(x) = sin(b*x) / (c*x)  at x→0  (classic)
    if point == 0:
        numerator = sp.sin(b * x)
        denominator = c * x
        limit_point = sp.Integer(0)
        expected = sp.Rational(b, c)
    else:
        # (x^2 - a^2) / (x - a)  at x→a
        numerator = x**2 - a**2
        denominator = x - a
        limit_point = sp.Integer(a)
        expected = sp.Integer(2 * a)

    return {
        "topic": "limit",
        "expr": numerator / denominator,
        "numerator": numerator,
        "denominator": denominator,
        "variable": x,
        "point": limit_point,
        "expected": expected,
    }


# ── partial derivatives / Euler ──────────────────────────────────────────────

def generate_partial_derivative_problem() -> dict:
    """
    Homogeneous function of degree n: f = a·xⁿ + b·x^(n-1)·y + c·y^n
    Euler's theorem: x·fₓ + y·fᵧ = n·f
    """
    n = random.randint(2, 4)
    a, b, c = _rand_coeff(1, 3), _rand_coeff(1, 3), _rand_coeff(1, 3)
    f = a * x**n + b * x**(n - 1) * y + c * y**n

    return {
        "topic": "partial_derivative",
        "function": f,
        "variables": (x, y),
        "degree": n,
    }


# ── Jacobian ─────────────────────────────────────────────────────────────────

def generate_jacobian_problem() -> dict:
    """
    Two functions u(x,y), v(x,y) with a computable 2×2 Jacobian.
    """
    choice = random.randint(0, 2)
    if choice == 0:
        a, b = _rand_coeff(1, 3), _rand_coeff(1, 3)
        u = a * x**2 + b * x * y
        v = x * y**2 - b * y
    elif choice == 1:
        a = _rand(1, 3)
        u = sp.exp(a * x) * sp.cos(y)
        v = sp.exp(a * x) * sp.sin(y)
    else:
        a, b = _rand_coeff(1, 3), _rand_coeff(1, 3)
        u = a * x + b * y
        v = a * x**2 - b * y**2

    return {
        "topic": "jacobian",
        "u": u,
        "v": v,
        "variables": (x, y),
    }


# ── Taylor / Maclaurin ────────────────────────────────────────────────────────

def generate_taylor_problem() -> dict:
    """
    f(x, y) near (x0, y0) expanded to degree 2.
    Uses polynomial so the expansion terminates cleanly.
    """
    a, b, c, d, e = [_rand_coeff(1, 3) for _ in range(5)]
    f = a * x**2 + b * x * y + c * y**2 + d * x + e * y + _rand_coeff(1, 3)
    x0 = random.choice([0, 1])
    y0 = random.choice([0, 1])

    return {
        "topic": "taylor",
        "function": f,
        "variables": (x, y),
        "point": (x0, y0),
        "order": 2,
    }


# ── Maxima / Minima ───────────────────────────────────────────────────────────

def generate_maxima_minima_problem() -> dict:
    """
    f(x,y) = a·x³ + b·y³ + c·x + d·y + e·x·y  with real critical points.
    We choose coefficients that guarantee the discriminant test is decisive.
    """
    # Simple: f = x^3 + y^3 - 3*a*x - 3*b*y
    a = _rand(1, 3)
    b = _rand(1, 3)
    f = x**3 + y**3 - 3 * a * x - 3 * b * y

    return {
        "topic": "maxima_minima",
        "function": f,
        "variables": (x, y),
    }


# ── Definite integral / Leibniz rule ─────────────────────────────────────────

def generate_definite_integral_problem() -> dict:
    """
    I(t) = ∫₀^t  (a·x + b)·eˢˢ dx   — differentiable under the integral sign.
    Uses Leibniz: I'(t) = integrand at upper limit.
    """
    a = _rand_coeff(1, 3)
    b = _rand_coeff(1, 3)
    integrand = (a * x + b) * sp.exp(x)
    lower = sp.Integer(0)
    upper = t   # parameter

    return {
        "topic": "definite_integral",
        "integrand": integrand,
        "variable": x,
        "parameter": t,
        "lower": lower,
        "upper": upper,
    }


# ── Double / Triple integral ─────────────────────────────────────────────────

def generate_multiple_integral_problem() -> dict:
    """
    ∫₀^a ∫₀^b  f(x,y) dy dx   with integer bounds and polynomial integrand.
    """
    a = _rand(1, 3)
    b = _rand(1, 3)
    p = random.randint(1, 2)
    q = random.randint(1, 2)
    c = _rand_coeff(1, 3)
    f = c * x**p * y**q

    return {
        "topic": "multiple_integral",
        "integrand": f,
        "variables": (x, y),
        "bounds_x": (sp.Integer(0), sp.Integer(a)),
        "bounds_y": (sp.Integer(0), sp.Integer(b)),
    }


# ── Variable change (Cartesian → Polar) ──────────────────────────────────────

def generate_variable_change_problem() -> dict:
    """
    ∫∫ (x² + y²) dA over circle of radius r.
    Transforms to polar: x=r cosθ, y=r sinθ, Jacobian=r.
    """
    radius = _rand(1, 3)
    # Integrand in Cartesian
    integrand_cart = x**2 + y**2   # = r² in polar
    return {
        "topic": "variable_change",
        "integrand_cartesian": integrand_cart,
        "region": f"x² + y² ≤ {radius}²",
        "radius": sp.Integer(radius),
    }


# ── Linear 2nd-order ODE ─────────────────────────────────────────────────────

def generate_linear_ode_problem() -> dict:
    """
    a·y'' + b·y' + c·y = g(x).
    Choose a, b, c so the auxiliary equation has real distinct roots,
    real equal roots, or complex roots with equal probability.
    """
    mode = random.choice(["distinct_real", "equal_real", "complex"])
    if mode == "distinct_real":
        # roots m1, m2 distinct real => (m-m1)(m-m2) = m²-(m1+m2)m+m1*m2
        m1 = random.randint(-3, 3)
        m2 = random.randint(-3, 3)
        while m2 == m1:
            m2 = random.randint(-3, 3)
        a = 1
        b = -(m1 + m2)
        c = m1 * m2
    elif mode == "equal_real":
        m1 = random.randint(-3, 3)
        a = 1
        b = -2 * m1
        c = m1**2
    else:  # complex: roots α ± βi
        alpha = random.randint(-2, 2)
        beta = random.randint(1, 3)
        a = 1
        b = -2 * alpha
        c = alpha**2 + beta**2

    # RHS g(x): simple polynomial or exponential
    rhs_choice = random.choice(["poly", "exp"])
    if rhs_choice == "poly":
        g = _rand_coeff(1, 4) * x + _rand_coeff(1, 4)
    else:
        k = random.choice([1, 2, 3])
        g = _rand_coeff(1, 4) * sp.exp(k * x)

    return {
        "topic": "linear_ode",
        "a": a,
        "b": b,
        "c": c,
        "g": g,
        "variable": x,
        "mode": mode,
    }
