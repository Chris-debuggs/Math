import sympy as sp
import pytest

from generators.eigen_generator import (
    generate_clean_eigen_problem,
)
from generators.calculus_generator import (
    generate_definite_integral_problem,
    generate_jacobian_problem,
    generate_limit_problem,
    generate_linear_ode_problem,
    generate_maxima_minima_problem,
    generate_multiple_integral_problem,
    generate_partial_derivative_problem,
    generate_taylor_problem,
    generate_variable_change_problem,
)
from solvers.cayley_hamilton_solver import cayley_hamilton_steps
from solvers.definite_integral_solver import definite_integral_steps
from solvers.eigen_solver import eigen_steps
from solvers.jacobian_solver import jacobian_steps
from solvers.limit_continuity_solver import limit_steps
from solvers.linear_ode_solver import linear_ode_steps
from solvers.maxima_minima_solver import maxima_minima_steps
from solvers.multiple_integral_solver import multiple_integral_steps
from solvers.partial_derivative_solver import partial_derivative_steps
from solvers.quadratic_form_solver import quadratic_form_steps
from solvers.taylor_maclaurin_solver import taylor_steps
from solvers.variable_change_solver import variable_change_steps


def _fixed_cayley_problem():
    return {"matrix": sp.Matrix([[2, 1], [0, 3]])}


def _fixed_quadratic_problem():
    return {"matrix": sp.Matrix([[3, 1], [1, 2]])}


def _assert_renderable_ast(ast_nodes):
    assert isinstance(ast_nodes, list) and len(ast_nodes) > 0
    assert all(isinstance(node, dict) for node in ast_nodes)
    assert all("type" in node and "value" in node for node in ast_nodes)


@pytest.mark.parametrize(
    ("generator", "solver"),
    [
        (lambda: generate_clean_eigen_problem(2), eigen_steps),
        (lambda: generate_clean_eigen_problem(3), eigen_steps),
        (_fixed_cayley_problem, cayley_hamilton_steps),
        (_fixed_quadratic_problem, quadratic_form_steps),
    ],
)
def test_matrix_solvers_accept_problem_dict(generator, solver):
    prob = generator()
    ast_nodes = solver(prob)
    _assert_renderable_ast(ast_nodes)


@pytest.mark.parametrize(
    ("generator", "solver", "use_matrix"),
    [
        (lambda: generate_clean_eigen_problem(2), eigen_steps, True),
        (lambda: generate_clean_eigen_problem(3), eigen_steps, True),
        (_fixed_cayley_problem, cayley_hamilton_steps, True),
        (_fixed_quadratic_problem, quadratic_form_steps, True),
        (generate_limit_problem, limit_steps, False),
        (generate_partial_derivative_problem, partial_derivative_steps, False),
        (generate_jacobian_problem, jacobian_steps, False),
        (generate_taylor_problem, taylor_steps, False),
        (generate_maxima_minima_problem, maxima_minima_steps, False),
        (generate_definite_integral_problem, definite_integral_steps, False),
        (generate_multiple_integral_problem, multiple_integral_steps, False),
        (generate_variable_change_problem, variable_change_steps, False),
        (generate_linear_ode_problem, linear_ode_steps, False),
    ],
)
def test_all_topics_return_renderable_ast(generator, solver, use_matrix):
    prob = generator()
    solver_input = prob["matrix"] if use_matrix else prob
    ast_nodes = solver(solver_input)
    _assert_renderable_ast(ast_nodes)


def test_cayley_hamilton_verification_node_is_zero_matrix():
    prob = _fixed_cayley_problem()
    ast_nodes = cayley_hamilton_steps(prob)
    verification = next(
        node for node in ast_nodes if node.get("label", "").startswith("**Verification**")
    )
    value = verification["value"]
    assert isinstance(value, sp.MatrixBase)
    assert value == sp.zeros(*value.shape)
