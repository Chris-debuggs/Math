import pytest
import sympy as sp

from content.concept_cards import get_foundation_cards, get_topic_card


def test_topic_card_includes_expected_fields():
    card = get_topic_card("eigenvalues")
    assert card["title"]
    assert card["syllabus"]
    assert card["core_idea"]
    assert card["exam_checklist"]
    assert card["tech_link"]


def test_foundation_cards_are_linked_for_matrix_topic():
    cards = get_foundation_cards("quadratic_form")
    assert len(cards) >= 1
    assert all("name" in node and "prompt" in node for node in cards)


def test_linear_transformation_plot_for_2x2_matrix():
    pytest.importorskip("matplotlib")
    from visualizers.plots import plot_linear_transformation_2d

    fig = plot_linear_transformation_2d(sp.Matrix([[2, 1], [0, 1]]))
    assert fig is not None
    assert len(fig.axes) == 1


def test_maxima_surface_plot_marks_axes():
    pytest.importorskip("matplotlib")
    from visualizers.plots import plot_maxima_surface

    x, y = sp.symbols("x y", real=True)
    fig = plot_maxima_surface(x**2 + y**2, (x, y), span=2.0, samples=30)
    assert fig is not None
    assert len(fig.axes) == 1
