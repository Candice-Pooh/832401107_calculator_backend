"""Safely evaluate basic mathematical expressions."""

import ast
import operator
from decimal import Decimal, DivisionByZero, InvalidOperation, localcontext


MAX_EXPRESSION_LENGTH = 200
MAX_AST_NODES = 100
MAX_DEPTH = 30
MAX_RESULT = Decimal("1e12")


BINARY_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
}

UNARY_OPERATORS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}


def _evaluate_node(node, depth=0):
    """Evaluate an allowed mathematical AST node."""

    if depth > MAX_DEPTH:
        raise ValueError("Expression is too complex")

    if isinstance(node, ast.Constant):
        if type(node.value) not in (int, float):
            raise ValueError("Invalid expression")

        number = Decimal(str(node.value))

        if not number.is_finite():
            raise ValueError("Invalid number")

        return number

    if isinstance(node, ast.BinOp):
        operation = BINARY_OPERATORS.get(type(node.op))

        if operation is None:
            raise ValueError("Unsupported operator")

        left = _evaluate_node(node.left, depth + 1)
        right = _evaluate_node(node.right, depth + 1)

        if isinstance(node.op, ast.Div) and right == 0:
            raise ZeroDivisionError("Division by zero")

        return operation(left, right)

    if isinstance(node, ast.UnaryOp):
        operation = UNARY_OPERATORS.get(type(node.op))

        if operation is None:
            raise ValueError("Unsupported operator")

        operand = _evaluate_node(node.operand, depth + 1)

        return operation(operand)

    raise ValueError("Invalid expression")


def calculate_expression(expression):
    """Parse and calculate a mathematical expression safely."""

    if not isinstance(expression, str) or not expression.strip():
        raise ValueError("Expression cannot be empty")

    if len(expression) > MAX_EXPRESSION_LENGTH:
        raise ValueError("Expression is too long")

    try:
        tree = ast.parse(expression, mode="eval")

    except (SyntaxError, ValueError, RecursionError) as error:
        raise ValueError("Invalid expression") from error

    if sum(1 for _ in ast.walk(tree)) > MAX_AST_NODES:
        raise ValueError("Expression is too complex")

    with localcontext() as context:
        context.prec = 28

        try:
            result = _evaluate_node(tree.body)

        except (InvalidOperation, DivisionByZero, OverflowError) as error:
            raise ValueError("Calculation failed") from error

        if not result.is_finite():
            raise ValueError("Invalid calculation result")

        if abs(result) > MAX_RESULT:
            raise ValueError("Calculation result is too large")

        return result