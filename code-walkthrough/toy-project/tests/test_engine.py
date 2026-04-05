from calculator.engine import add


def test_add_integers() -> None:
    assert add(2, 3) == 5


def test_add_floats() -> None:
    assert add(1.5, 2.5) == 4.0


def test_add_negative() -> None:
    assert add(-1, 1) == 0
