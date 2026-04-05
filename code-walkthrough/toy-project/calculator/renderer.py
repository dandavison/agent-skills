from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import ClassVar

from calculator.engine import OperationResult, OperationType, _get_operation


class OutputFormat(Enum):
    PLAIN = "plain"
    VERBOSE = "verbose"


_SYMBOLS: dict[OperationType, str] = {
    OperationType.ADD: "+",
    OperationType.MULTIPLY: "*",
}


def _symbol_for(op_type: OperationType) -> str:
    if op_type not in _SYMBOLS:
        raise ValueError(f"no symbol registered for {op_type.value}")
    return _SYMBOLS[op_type]


@dataclass(frozen=True)
class RenderContext:
    format: OutputFormat
    precision: int | None = None

    def format_number(self, n: float) -> str:
        if self.precision is not None:
            return f"{n:.{self.precision}f}"
        if n == int(n):
            return str(int(n))
        return str(n)


class Renderer(ABC):
    output_format: ClassVar[OutputFormat]

    @abstractmethod
    def render(self, result: OperationResult, ctx: RenderContext) -> str: ...


class InfixRenderer(Renderer):
    output_format = OutputFormat.PLAIN

    def render(self, result: OperationResult, ctx: RenderContext) -> str:
        symbol = _symbol_for(result.operation)
        parts = [ctx.format_number(o) for o in result.operands]
        lhs = f" {symbol} ".join(parts)
        rhs = ctx.format_number(result.value)
        return f"{lhs} = {rhs}"


class VerboseRenderer(Renderer):
    output_format = OutputFormat.VERBOSE

    def render(self, result: OperationResult, ctx: RenderContext) -> str:
        operand_strs = [ctx.format_number(o) for o in result.operands]
        return (
            f"Operation: {result.operation.value}\n"
            f"Operands:  {', '.join(operand_strs)}\n"
            f"Result:    {ctx.format_number(result.value)}"
        )


_RENDERER_REGISTRY: dict[OutputFormat, Renderer] = {}


def _register_renderer(renderer: Renderer) -> None:
    _RENDERER_REGISTRY[renderer.output_format] = renderer


def _get_renderer(fmt: OutputFormat) -> Renderer:
    if fmt not in _RENDERER_REGISTRY:
        raise ValueError(f"no renderer registered for {fmt.value}")
    return _RENDERER_REGISTRY[fmt]


_register_renderer(InfixRenderer())
_register_renderer(VerboseRenderer())

_DEFAULT_CTX = RenderContext(format=OutputFormat.PLAIN)


def _render_operation(
    op_type: OperationType,
    a: float,
    b: float,
    fmt: OutputFormat = OutputFormat.PLAIN,
    precision: int | None = None,
) -> str:
    op = _get_operation(op_type)
    result = op.execute(a, b)
    ctx = RenderContext(format=fmt, precision=precision)
    renderer = _get_renderer(fmt)
    return renderer.render(result, ctx)


def render_addition(
    a: float,
    b: float,
    fmt: OutputFormat = OutputFormat.PLAIN,
    precision: int | None = None,
) -> str:
    return _render_operation(OperationType.ADD, a, b, fmt, precision)


def render_multiplication(
    a: float,
    b: float,
    fmt: OutputFormat = OutputFormat.PLAIN,
    precision: int | None = None,
) -> str:
    return _render_operation(OperationType.MULTIPLY, a, b, fmt, precision)
