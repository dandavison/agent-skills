from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import ClassVar


class OperandValidationError(Exception):
    """Raised when operands fail validation."""


class OperationType(Enum):
    ADD = "add"


@dataclass(frozen=True)
class OperationResult:
    operation: OperationType
    operands: tuple[float, ...]
    value: float

    def __str__(self) -> str:
        return f"{self.operation.value}({', '.join(str(o) for o in self.operands)}) = {self.value}"


class Operation(ABC):
    operation_type: ClassVar[OperationType]
    min_operands: ClassVar[int] = 2
    max_operands: ClassVar[int] = 2

    def execute(self, *operands: float) -> OperationResult:
        self._validate_operands(operands)
        value = self._compute(operands)
        return OperationResult(
            operation=self.operation_type,
            operands=operands,
            value=value,
        )

    def _validate_operands(self, operands: tuple[float, ...]) -> None:
        if len(operands) < self.min_operands:
            raise OperandValidationError(
                f"{self.operation_type.value} requires at least {self.min_operands} operands, "
                f"got {len(operands)}"
            )
        if len(operands) > self.max_operands:
            raise OperandValidationError(
                f"{self.operation_type.value} accepts at most {self.max_operands} operands, "
                f"got {len(operands)}"
            )
        for i, operand in enumerate(operands):
            if not isinstance(operand, int | float):
                raise OperandValidationError(
                    f"operand {i} must be numeric, got {type(operand).__name__}"
                )

    @abstractmethod
    def _compute(self, operands: tuple[float, ...]) -> float: ...


class Addition(Operation):
    operation_type = OperationType.ADD

    def _compute(self, operands: tuple[float, ...]) -> float:
        return sum(operands)


_REGISTRY: dict[OperationType, Operation] = {}


def _register(op: Operation) -> None:
    _REGISTRY[op.operation_type] = op


def _get_operation(op_type: OperationType) -> Operation:
    if op_type not in _REGISTRY:
        raise ValueError(f"no operation registered for {op_type.value}")
    return _REGISTRY[op_type]


_register(Addition())


def add(a: float, b: float) -> float:
    result = _get_operation(OperationType.ADD).execute(a, b)
    return result.value
