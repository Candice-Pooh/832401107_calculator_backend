# Backend Code Style

## 1. Reference Standard

This project follows Python PEP 8 as its primary
coding style reference.

Reference:
https://peps.python.org/pep-0008/

## 2. Naming Conventions

Functions and variables use snake_case.

Examples:

- calculate_expression
- add_history
- get_history
- delete_history

Constants use UPPER_CASE.

Examples:

- DATABASE_PATH
- MAX_EXPRESSION_LENGTH
- MAX_RESULT

Classes use PascalCase.

Example:

- TestCalculator

## 3. Indentation

Python code uses four spaces per indentation level.

Tabs are not used for indentation.

## 4. Documentation

Modules and major functions include docstrings.

Comments explain important design decisions
rather than repeating obvious code behavior.

## 5. Function Design

Functions should have a clear responsibility.

Mathematical evaluation, database operations,
and HTTP request handling are implemented
in separate modules.

## 6. Error Handling

Invalid input is handled using appropriate exceptions.

API errors return structured JSON responses.

Unexpected database errors are logged
without exposing internal implementation details.

## 7. Database Operations

SQL queries use parameterized placeholders.

Database transactions are managed explicitly.

Database connections are closed after use.

## 8. Testing

Unit tests use Python's unittest framework.

Tests cover normal operations, invalid input,
and important boundary conditions.

## 9. Code Formatting

Four-space indentation is required.

Two blank lines separate top-level functions.

Imports are grouped logically.

The project generally follows PEP 8 conventions,
with a practical target of approximately
88 characters per line.