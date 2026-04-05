from calculator.engine import add


def render_addition(a: float, b: float) -> str:
    result = add(a, b)
    return f"{a} + {b} = {result}"
