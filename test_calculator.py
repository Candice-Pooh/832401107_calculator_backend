"""Unit tests for the calculator module."""

import unittest
from decimal import Decimal

from calculator import calculate_expression


class TestCalculator(unittest.TestCase):
    """Test valid calculations and error handling."""

    def test_addition(self):
        self.assertEqual(
            calculate_expression("12+8"),
            Decimal("20")
        )

    def test_subtraction(self):
        self.assertEqual(
            calculate_expression("10-3"),
            Decimal("7")
        )

    def test_multiplication(self):
        self.assertEqual(
            calculate_expression("4*5"),
            Decimal("20")
        )

    def test_division(self):
        self.assertEqual(
            calculate_expression("10/2"),
            Decimal("5")
        )

    def test_operator_precedence(self):
        self.assertEqual(
            calculate_expression("1+2*3"),
            Decimal("7")
        )

    def test_parentheses(self):
        self.assertEqual(
            calculate_expression("(1+2)*3"),
            Decimal("9")
        )

    def test_negative_numbers(self):
        self.assertEqual(
            calculate_expression("-5+8"),
            Decimal("3")
        )

    def test_unary_minus(self):
        self.assertEqual(
            calculate_expression("3*-2"),
            Decimal("-6")
        )

    def test_decimal_calculation(self):
        self.assertEqual(
            calculate_expression("0.1+0.2"),
            Decimal("0.3")
        )

    def test_division_by_zero(self):
        with self.assertRaises(ZeroDivisionError):
            calculate_expression("10/0")

    def test_invalid_expression(self):
        with self.assertRaises(ValueError):
            calculate_expression("1+*/2")

    def test_empty_expression(self):
        with self.assertRaises(ValueError):
            calculate_expression("")

    def test_unsupported_operator(self):
        with self.assertRaises(ValueError):
            calculate_expression("2**3")

    def test_unsafe_expression(self):
        with self.assertRaises(ValueError):
            calculate_expression("__import__('os').getcwd()")


if __name__ == "__main__":
    unittest.main()