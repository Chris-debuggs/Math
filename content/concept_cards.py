"""Syllabus-aligned concept cards for quick theory revision."""

from __future__ import annotations

from typing import Dict, List


TopicCard = Dict[str, object]
FoundationCard = Dict[str, str]


TOPIC_CONCEPTS: Dict[str, TopicCard] = {
    "eigenvalues": {
        "title": "Matrices: Characteristic Equation and Eigen Structure",
        "syllabus": "20MA203 - Linear Algebra",
        "core_idea": "Eigenvectors keep their direction under a linear map; eigenvalues scale them.",
        "exam_checklist": [
            "Form det(A - lambda I) = 0",
            "Solve for all eigenvalues",
            "Compute null space of (A - lambda I) for eigenvectors",
            "State algebraic and geometric multiplicity when needed",
        ],
        "tech_link": "Used in PCA, spectral clustering, and system stability models.",
    },
    "eigenvalues_3x3": {
        "title": "Matrices: Characteristic Equation and Eigen Structure (3x3)",
        "syllabus": "20MA203 - Linear Algebra",
        "core_idea": "Same rules as 2x2, but pay attention to repeated roots and eigenspace dimension.",
        "exam_checklist": [
            "Expand det(A - lambda I) carefully",
            "Factor or solve cubic characteristic polynomial",
            "Find basis vectors for each eigenspace",
            "Check if matrix is diagonalizable",
        ],
        "tech_link": "Useful for 3D transformations and coupled state-transition systems.",
    },
    "cayley_hamilton": {
        "title": "Matrix Polynomial Identities",
        "syllabus": "20MA203 - Linear Algebra",
        "core_idea": "Every square matrix satisfies its own characteristic polynomial.",
        "exam_checklist": [
            "Find p(lambda) from det(A - lambda I)",
            "Substitute A into p(lambda) to get p(A)",
            "Verify p(A) = 0",
            "Rearrange p(A) to compute A inverse when det(A) is non-zero",
        ],
        "tech_link": "Reduces high matrix powers in recurrence and control computations.",
    },
    "quadratic_form": {
        "title": "Quadratic Form to Canonical Form",
        "syllabus": "20MA203 - Linear Algebra",
        "core_idea": "Orthogonal diagonalization removes cross terms and exposes signs of curvature.",
        "exam_checklist": [
            "Represent Q as x^T A x with symmetric A",
            "Find orthonormal eigenvectors of A",
            "Construct orthogonal matrix P",
            "Compute D = P^T A P and classify definiteness",
        ],
        "tech_link": "Shows up in optimization, covariance ellipsoids, and least-squares geometry.",
    },
    "partial_derivative": {
        "title": "Functions of Several Variables: Partial and Total Change",
        "syllabus": "20MA203 - Differential Calculus",
        "core_idea": "Partial derivatives isolate one variable's effect while others are held constant.",
        "exam_checklist": [
            "Differentiate with respect to each variable",
            "Apply chain rule for composite maps",
            "Check homogeneity before applying Euler theorem",
            "Interpret gradient as direction of steepest increase",
        ],
        "tech_link": "Backpropagation in neural networks repeatedly applies chain-rule structure.",
    },
    "jacobian": {
        "title": "Jacobian and Functional Dependence",
        "syllabus": "20MA203 - Differential Calculus",
        "core_idea": "The Jacobian determinant tracks local area scaling; a nonzero determinant indicates local invertibility.",
        "exam_checklist": [
            "Build Jacobian matrix from first partial derivatives",
            "Compute determinant and simplify",
            "Use determinant test for local invertibility or possible dependence",
            "Use Jacobian in coordinate substitutions for integrals",
        ],
        "tech_link": "Used in coordinate transforms, robotics kinematics, and generative models.",
    },
    "taylor": {
        "title": "Multivariable Taylor Expansion",
        "syllabus": "20MA203 - Differential Calculus",
        "core_idea": "Taylor series gives a local polynomial model around a point.",
        "exam_checklist": [
            "Compute derivatives up to requested order",
            "Evaluate derivatives at expansion point",
            "Assemble terms with factorial factors",
            "State truncation order clearly",
        ],
        "tech_link": "Core approximation tool in numerical optimization and error analysis.",
    },
    "maxima_minima": {
        "title": "Maxima/Minima and Lagrange Multiplier Setup",
        "syllabus": "20MA203 - Differential Calculus",
        "core_idea": "Critical points are located by first derivatives and classified by second-order behavior.",
        "exam_checklist": [
            "Solve f_x = 0 and f_y = 0 for critical points",
            "Compute f_xx, f_xy, f_yy and discriminant",
            "Classify each point as min, max, or saddle",
            "For constraints, solve grad f = lambda grad g",
        ],
        "tech_link": "Optimization pipelines in ML and engineering use the same gradient/Hessian logic.",
    },
    "limit": {
        "title": "Limit Evaluation Workflow",
        "syllabus": "20MA203 - Differential Calculus",
        "core_idea": "Start with direct substitution, then move to algebraic simplification or L'Hospital only if needed.",
        "exam_checklist": [
            "Try substitution first",
            "Identify indeterminate forms",
            "Apply simplification or L'Hospital rule",
            "Re-evaluate and present final finite/infinite limit",
        ],
        "tech_link": "Limit intuition underpins numerical stability and asymptotic algorithm analysis.",
    },
}


FOUNDATION_CARDS: Dict[str, FoundationCard] = {
    "vector_space": {
        "name": "Vector Space Foundations",
        "prompt": "To prove subspace: check non-empty, closed under addition, closed under scalar multiplication.",
    },
    "span_basis_rank": {
        "name": "Span, Basis, Rank, Nullity",
        "prompt": "Use row reduction to obtain basis vectors; rank + nullity = number of columns.",
    },
    "linear_transformation": {
        "name": "Linear Transformation Properties",
        "prompt": "Check T(u+v)=T(u)+T(v) and T(cu)=cT(u); then move to matrix form and basis change.",
    },
    "curvature": {
        "name": "Curvature and Radius of Curvature",
        "prompt": "For y(x), use kappa = |y''|/(1+(y')^2)^(3/2) and radius R = 1/kappa.",
    },
}


TOPIC_TO_FOUNDATIONS: Dict[str, List[str]] = {
    "eigenvalues": ["linear_transformation", "span_basis_rank"],
    "eigenvalues_3x3": ["linear_transformation", "span_basis_rank"],
    "cayley_hamilton": ["linear_transformation"],
    "quadratic_form": ["linear_transformation"],
    "partial_derivative": ["curvature"],
    "jacobian": ["linear_transformation"],
    "maxima_minima": ["curvature"],
}


def get_topic_card(topic_key: str) -> TopicCard:
    """Return concept metadata for a topic key."""
    return TOPIC_CONCEPTS.get(topic_key, {})


def get_foundation_cards(topic_key: str) -> List[FoundationCard]:
    """Return lightweight theory cards related to a computational topic."""
    keys = TOPIC_TO_FOUNDATIONS.get(topic_key, [])
    return [FOUNDATION_CARDS[k] for k in keys if k in FOUNDATION_CARDS]
