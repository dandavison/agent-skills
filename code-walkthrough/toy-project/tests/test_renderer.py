from calculator.renderer import render_addition


def test_render_addition() -> None:
    assert render_addition(2, 3) == "2 + 3 = 5"


def test_render_addition_floats() -> None:
    assert render_addition(1.5, 2.5) == "1.5 + 2.5 = 4.0"
