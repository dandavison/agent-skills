import pytest

from calculator.engine import (
    Addition,
    Multiplication,
    OperandValidationError,
    OperationResult,
    OperationType,
    _get_operation,
    add,
    multiply,
)


class TestAddFunction:
    def test_integers(self) -> None:
        assert add(2, 3) == 5

    def test_floats(self) -> None:
        assert add(1.5, 2.5) == 4.0

    def test_negative(self) -> None:
        assert add(-1, 1) == 0


class TestAdditionOperation:
    def test_execute_returns_result(self) -> None:
        op = Addition()
        result = op.execute(2.0, 3.0)
        assert isinstance(result, OperationResult)
        assert result.value == 5.0
        assert result.operation == OperationType.ADD
        assert result.operands == (2.0, 3.0)

    def test_result_str(self) -> None:
        op = Addition()
        result = op.execute(2.0, 3.0)
        assert str(result) == "add(2.0, 3.0) = 5.0"


class TestMultiplyFunction:
    def test_integers(self) -> None:
        assert multiply(2, 3) == 6

    def test_floats(self) -> None:
        assert multiply(1.5, 2.0) == 3.0

    def test_by_zero(self) -> None:
        assert multiply(42, 0) == 0


class TestMultiplicationOperation:
    def test_execute_returns_result(self) -> None:
        op = Multiplication()
        result = op.execute(4.0, 5.0)
        assert isinstance(result, OperationResult)
        assert result.value == 20.0
        assert result.operation == OperationType.MULTIPLY
        assert result.operands == (4.0, 5.0)

    def test_result_str(self) -> None:
        op = Multiplication()
        result = op.execute(4.0, 5.0)
        assert str(result) == "multiply(4.0, 5.0) = 20.0"


class TestOperandValidation:
    def test_too_few_operands(self) -> None:
        op = Addition()
        with pytest.raises(OperandValidationError, match="at least 2"):
            op.execute(1.0)

    def test_too_many_operands(self) -> None:
        op = Addition()
        with pytest.raises(OperandValidationError, match="at most 2"):
            op.execute(1.0, 2.0, 3.0)


class TestRegistry:
    def test_add_registered(self) -> None:
        op = _get_operation(OperationType.ADD)
        assert isinstance(op, Addition)

    def test_multiply_registered(self) -> None:
        op = _get_operation(OperationType.MULTIPLY)
        assert isinstance(op, Multiplication)

    def test_unknown_operation(self) -> None:
        with pytest.raises(ValueError):
            _get_operation(OperationType("nonexistent"))
