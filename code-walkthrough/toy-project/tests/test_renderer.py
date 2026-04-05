import pytest

from calculator.engine import OperationType
from calculator.renderer import (
    OutputFormat,
    RenderContext,
    _get_renderer,
    _symbol_for,
    render_addition,
)


class TestRenderAddition:
    def test_integers(self) -> None:
        assert render_addition(2, 3) == "2 + 3 = 5"

    def test_floats(self) -> None:
        assert render_addition(1.5, 2.5) == "1.5 + 2.5 = 4"

    def test_verbose(self) -> None:
        result = render_addition(2, 3, fmt=OutputFormat.VERBOSE)
        assert "Operation: add" in result
        assert "Operands:  2, 3" in result
        assert "Result:    5" in result

    def test_precision(self) -> None:
        assert render_addition(1, 2, precision=2) == "1.00 + 2.00 = 3.00"


class TestRenderContext:
    def test_format_integer_float(self) -> None:
        ctx = RenderContext(format=OutputFormat.PLAIN)
        assert ctx.format_number(3.0) == "3"

    def test_format_with_precision(self) -> None:
        ctx = RenderContext(format=OutputFormat.PLAIN, precision=3)
        assert ctx.format_number(3.14) == "3.140"


class TestSymbolLookup:
    def test_add_symbol(self) -> None:
        assert _symbol_for(OperationType.ADD) == "+"

    def test_unknown_symbol(self) -> None:
        with pytest.raises(ValueError):
            _symbol_for(OperationType("nonexistent"))


class TestRendererRegistry:
    def test_plain_registered(self) -> None:
        renderer = _get_renderer(OutputFormat.PLAIN)
        assert renderer is not None

    def test_verbose_registered(self) -> None:
        renderer = _get_renderer(OutputFormat.VERBOSE)
        assert renderer is not None
