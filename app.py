"""
app.py  —  MA3151 Deterministic CAS Tutoring Engine
Streamlit UI with session-state machine, topic selector, step-through solver,
and Hint mode.
"""
import streamlit as st
import sympy as sp

# ─── Generators ──────────────────────────────────────────────────────────────
from generators.eigen_generator import (
    generate_clean_eigen_problem,
    generate_cayley_hamilton_problem,
    generate_quadratic_form_problem,
)
from generators.calculus_generator import (
    generate_limit_problem,
    generate_partial_derivative_problem,
    generate_jacobian_problem,
    generate_taylor_problem,
    generate_maxima_minima_problem,
    generate_definite_integral_problem,
    generate_multiple_integral_problem,
    generate_variable_change_problem,
    generate_linear_ode_problem,
)

# ─── Solvers ─────────────────────────────────────────────────────────────────
from solvers.eigen_solver import eigen_steps
from solvers.cayley_hamilton_solver import cayley_hamilton_steps
from solvers.quadratic_form_solver import quadratic_form_steps
from solvers.limit_continuity_solver import limit_steps
from solvers.partial_derivative_solver import partial_derivative_steps
from solvers.jacobian_solver import jacobian_steps
from solvers.taylor_maclaurin_solver import taylor_steps
from solvers.maxima_minima_solver import maxima_minima_steps
from solvers.definite_integral_solver import definite_integral_steps
from solvers.multiple_integral_solver import multiple_integral_steps
from solvers.variable_change_solver import variable_change_steps
from solvers.linear_ode_solver import linear_ode_steps
from content.concept_cards import get_topic_card, get_foundation_cards

VISUALIZER_AVAILABLE = True
try:
    from visualizers.plots import plot_linear_transformation_2d, plot_maxima_surface
except ModuleNotFoundError:
    VISUALIZER_AVAILABLE = False
    plot_linear_transformation_2d = None
    plot_maxima_surface = None

# ─── Topic registry ──────────────────────────────────────────────────────────
# Each entry: (display_name, unit_label, generator_fn, solver_fn, generator_kwargs)

TOPICS = {
    "eigenvalues": (
        "Eigenvalues & Eigenvectors", "Unit 1 — Matrices",
        generate_clean_eigen_problem, eigen_steps, {"dim": 2},
    ),
    "eigenvalues_3x3": (
        "Eigenvalues & Eigenvectors (3×3)", "Unit 1 — Matrices",
        generate_clean_eigen_problem, eigen_steps, {"dim": 3},
    ),
    "cayley_hamilton": (
        "Cayley-Hamilton Theorem", "Unit 1 — Matrices",
        generate_cayley_hamilton_problem, cayley_hamilton_steps, {"dim": 2},
    ),
    "quadratic_form": (
        "Quadratic Form — Canonical Reduction", "Unit 1 — Matrices",
        generate_quadratic_form_problem, quadratic_form_steps, {},
    ),
    "limit": (
        "Limits & L'Hôpital's Rule", "Unit 2 — Differential Calculus",
        generate_limit_problem, limit_steps, {},
    ),
    "partial_derivative": (
        "Partial Derivatives & Euler's Theorem", "Unit 2 — Differential Calculus",
        generate_partial_derivative_problem, partial_derivative_steps, {},
    ),
    "jacobian": (
        "Jacobian & Functional Dependence", "Unit 2 — Differential Calculus",
        generate_jacobian_problem, jacobian_steps, {},
    ),
    "taylor": (
        "Taylor / Maclaurin Series (2-variable)", "Unit 3 — Series Expansions",
        generate_taylor_problem, taylor_steps, {},
    ),
    "maxima_minima": (
        "Maxima & Minima", "Unit 3 — Applications",
        generate_maxima_minima_problem, maxima_minima_steps, {},
    ),
    "definite_integral": (
        "Definite Integral & Leibniz Rule", "Unit 4 — Integral Calculus",
        generate_definite_integral_problem, definite_integral_steps, {},
    ),
    "multiple_integral": (
        "Double Integrals", "Unit 4 — Integral Calculus",
        generate_multiple_integral_problem, multiple_integral_steps, {},
    ),
    "variable_change": (
        "Change of Variables (Polar)", "Unit 4 — Integral Calculus",
        generate_variable_change_problem, variable_change_steps, {},
    ),
    "linear_ode": (
        "Linear 2nd-Order ODE", "Unit 5 — Ordinary Differential Equations",
        generate_linear_ode_problem, linear_ode_steps, {},
    ),
}

TOPIC_KEYS = list(TOPICS.keys())
MATRIX_VISUAL_TOPICS = {"eigenvalues", "eigenvalues_3x3", "cayley_hamilton", "quadratic_form"}


# ─── Session-state initialisation ────────────────────────────────────────────

def _load_problem(topic_key: str):
    """Generate a new problem for the given topic and populate session state."""
    display_name, unit, gen_fn, solver_fn, gen_kwargs = TOPICS[topic_key]
    prob = gen_fn(**gen_kwargs)
    # Matrix-centric solvers consume prob["matrix"], while the others consume prob.
    if solver_fn in (eigen_steps, cayley_hamilton_steps, quadratic_form_steps):
        ast = solver_fn(prob["matrix"])
    else:
        ast = solver_fn(prob)
    st.session_state.update({
        "topic": topic_key,
        "step": 0,
        "active_problem": prob,
        "solution_ast": ast,
        "show_all": False,
    })


def _init_session(topic_key: str):
    if "topic" not in st.session_state or st.session_state.topic != topic_key:
        _load_problem(topic_key)
    else:
        # ensure keys exist (first run)
        for k, v in [("step", 0), ("show_all", False)]:
            if k not in st.session_state:
                st.session_state[k] = v


def _render_concept_card(topic_key: str):
    """Render compact concept notes for the selected topic."""
    card = get_topic_card(topic_key)
    if not card:
        return

    with st.expander("Concept Card", expanded=True):
        st.markdown(f"**{card['title']}**")
        st.caption(str(card["syllabus"]))
        st.markdown(str(card["core_idea"]))
        st.markdown("**Exam checklist**")
        for item in card["exam_checklist"]:
            st.markdown(f"- {item}")
        st.markdown(f"**Tech link:** {card['tech_link']}")

        related = get_foundation_cards(topic_key)
        if related:
            st.markdown("**Related theory prompts**")
            for node in related:
                st.markdown(f"- **{node['name']}**: {node['prompt']}")


def _render_visual(topic_key: str, active_problem: dict):
    """Render an optional geometric visual for selected topics."""
    if topic_key in MATRIX_VISUAL_TOPICS:
        A = active_problem["matrix"]
        if A.shape != (2, 2):
            st.caption("Visualization currently supports 2x2 matrix transformations.")
            return True
        fig = plot_linear_transformation_2d(A)
        st.pyplot(fig, use_container_width=True)
        return True

    if topic_key == "maxima_minima":
        fig = plot_maxima_surface(active_problem["function"], active_problem["variables"])
        st.pyplot(fig, use_container_width=True)
        return True

    return False


# ─── AST renderer ────────────────────────────────────────────────────────────

def _render_node(node: dict, show_hint: bool = False):
    """Render a single AST node as Streamlit widgets."""
    label = node.get("label", "")
    val = node.get("value")
    hint = node.get("hint", "")
    node_type = node.get("type", "text")

    if label:
        st.markdown(label)

    if node_type == "matrix":
        st.latex(sp.latex(val))
    elif node_type == "vector":
        st.latex(sp.latex(val))
    elif node_type == "polynomial":
        st.latex(sp.latex(val) + r" = 0")
    elif node_type == "factored_poly":
        st.latex(sp.latex(val))
    elif node_type == "solution_set":
        # val is a list of eigenvalues
        formatted = r",\quad ".join(r"\lambda = " + sp.latex(v) for v in val)
        st.latex(formatted)
    elif node_type == "latex":
        st.latex(str(val))
    elif node_type == "text":
        st.latex(str(val)) if val and val.strip().startswith("\\") else st.markdown(str(val))
    elif node_type == "equation":
        st.latex(sp.latex(val))

    if show_hint and hint:
        st.info(f"💡 **Hint:** {hint}")
    st.markdown("---")


# ─── Page config ─────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="MA3151 CAS Tutor",
    page_icon="📐",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Custom CSS ──────────────────────────────────────────────────────────────

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Dark gradient background */
    .stApp {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        color: #e8e8f0;
    }

    /* Sidebar */
    .css-1d391kg, [data-testid="stSidebar"] {
        background: rgba(15, 12, 41, 0.85) !important;
        border-right: 1px solid rgba(255,255,255,0.08);
    }

    /* Cards / containers */
    .step-card {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 12px;
        padding: 1.2rem 1.5rem;
        margin-bottom: 0.8rem;
        backdrop-filter: blur(8px);
        transition: all 0.2s ease;
    }
    .step-card:hover {
        border-color: rgba(120,100,255,0.5);
        box-shadow: 0 4px 20px rgba(100,80,255,0.15);
    }

    /* Topic badge */
    .unit-badge {
        display: inline-block;
        font-size: 0.72rem;
        font-weight: 600;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        color: #a78bfa;
        background: rgba(167,139,250,0.12);
        padding: 3px 10px;
        border-radius: 20px;
        margin-bottom: 0.5rem;
    }

    /* Progress bar */
    .progress-bar-outer {
        background: rgba(255,255,255,0.08);
        border-radius: 999px;
        height: 6px;
        width: 100%;
        margin: 0.6rem 0 1.2rem;
        overflow: hidden;
    }
    .progress-bar-inner {
        background: linear-gradient(90deg, #7c3aed, #a78bfa);
        border-radius: 999px;
        height: 100%;
        transition: width 0.35s ease;
    }

    /* Buttons */
    .stButton > button {
        border-radius: 8px !important;
        font-weight: 500 !important;
        transition: all 0.2s ease !important;
    }
    .stButton > button:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 12px rgba(124,58,237,0.35) !important;
    }

    /* LaTeX math display */
    .katex-display {
        padding: 0.5rem 0;
    }

    /* Step counter chip */
    .step-chip {
        font-size: 0.8rem;
        color: #a78bfa;
        font-weight: 600;
    }

    /* Divider */
    hr {
        border-color: rgba(255,255,255,0.07) !important;
        margin: 0.5rem 0 !important;
    }

    /* Info boxes */
    .stAlert {
        border-radius: 10px !important;
        font-size: 0.9rem !important;
    }
</style>
""", unsafe_allow_html=True)


# ─── Sidebar ─────────────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown("## 📐 MA3151 Tutor")
    st.markdown("*Deterministic CAS-powered step-by-step solver*")
    st.markdown("---")

    # Unit groupings for the selector
    unit_groups = {}
    for key, (name, unit, *_) in TOPICS.items():
        unit_groups.setdefault(unit, []).append((key, name))

    st.markdown("### Select Topic")
    selected_unit = st.selectbox(
        "Unit",
        options=list(unit_groups.keys()),
        label_visibility="collapsed",
    )
    topic_options = unit_groups[selected_unit]
    topic_display = {name: key for key, name in topic_options}
    selected_name = st.selectbox(
        "Topic",
        options=list(topic_display.keys()),
        label_visibility="collapsed",
    )
    selected_topic = topic_display[selected_name]

    st.markdown("---")
    st.markdown("### Options")
    hint_mode = st.toggle("🔦 Hint Mode", value=False,
                          help="Show a pedagogical hint below each step.")
    show_concepts = st.toggle("Concept Cards", value=True)
    show_visuals = st.toggle(
        "Visualize",
        value=VISUALIZER_AVAILABLE,
        disabled=not VISUALIZER_AVAILABLE,
    )
    if not VISUALIZER_AVAILABLE:
        st.caption("Install matplotlib to enable visualizations.")
    matrix_dim = None
    if selected_topic in ("eigenvalues", "cayley_hamilton"):
        matrix_dim = st.radio("Matrix dim", [2, 3], horizontal=True)
        if selected_topic == "eigenvalues":
            selected_topic = "eigenvalues_3x3" if matrix_dim == 3 else "eigenvalues"

    st.markdown("---")
    st.markdown(
        "<small style='color:#6b7280'>Built with SymPy + Streamlit<br>"
        "All solutions are deterministic CAS output.</small>",
        unsafe_allow_html=True,
    )


# ─── Init ────────────────────────────────────────────────────────────────────

_init_session(selected_topic)

# ─── Header ──────────────────────────────────────────────────────────────────

display_name, unit_label, *_ = TOPICS[selected_topic]

st.markdown(f'<div class="unit-badge">{unit_label}</div>', unsafe_allow_html=True)
st.markdown(f"## {display_name}")

ast = st.session_state.solution_ast
total_steps = len(ast)
current_step = st.session_state.step
show_all = st.session_state.show_all

# Progress bar
pct = int(100 * (current_step + 1) / total_steps)
st.markdown(
    f'<div class="progress-bar-outer">'
    f'<div class="progress-bar-inner" style="width:{pct}%"></div>'
    f'</div>',
    unsafe_allow_html=True,
)
st.markdown(
    f'<span class="step-chip">Step {current_step + 1} of {total_steps}</span>',
    unsafe_allow_html=True,
)

# ─── Step renderer ───────────────────────────────────────────────────────────

if show_concepts:
    _render_concept_card(selected_topic)

if VISUALIZER_AVAILABLE and show_visuals and (
    selected_topic in MATRIX_VISUAL_TOPICS or selected_topic == "maxima_minima"
):
    st.markdown("### Visual Intuition")
    try:
        _render_visual(selected_topic, st.session_state.active_problem)
    except Exception as exc:
        st.warning(f"Visualization unavailable for this problem: {exc}")

if show_all:
    steps_to_show = range(total_steps)
else:
    steps_to_show = range(current_step + 1)

for i in steps_to_show:
    node = ast[i]
    with st.container():
        st.markdown(f'<div class="step-card">', unsafe_allow_html=True)
        _render_node(node, show_hint=hint_mode)
        st.markdown('</div>', unsafe_allow_html=True)

# ─── Controls ────────────────────────────────────────────────────────────────

st.markdown("")
col1, col2, col3, col4 = st.columns([1, 1, 1, 1])

with col1:
    if st.button("⬅ Previous", disabled=(current_step == 0 or show_all),
                 use_container_width=True):
        st.session_state.step -= 1
        st.session_state.show_all = False
        st.rerun()

with col2:
    if st.button("Next Step ➡", disabled=(current_step >= total_steps - 1 or show_all),
                 use_container_width=True):
        st.session_state.step += 1
        st.rerun()

with col3:
    label = "☰ Collapse" if show_all else "☰ Show All"
    if st.button(label, use_container_width=True):
        st.session_state.show_all = not show_all
        if not show_all:
            st.session_state.step = total_steps - 1
        st.rerun()

with col4:
    if st.button("🔀 New Problem", type="primary", use_container_width=True):
        _load_problem(selected_topic)
        st.rerun()
