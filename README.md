# Calculator Backend

## 1. Project Overview

This repository contains the backend implementation of a
front-end and back-end separated calculator system.

The backend is responsible for mathematical expression
evaluation, input validation, calculation history storage,
and RESTful API communication.

All mathematical calculations are performed on the server.
The frontend does not independently calculate results.

## 2. Technology Stack

- Programming Language: Python 3.12
- Web Framework: Flask 3.1.3
- Cross-Origin Support: Flask-CORS 6.0.5
- Database: SQLite
- Expression Parsing: Python AST
- Decimal Arithmetic: Python Decimal
- Testing Framework: unittest
- Deployment Platform: PythonAnywhere

## 3. Project Structure

```text
calculator_backend/
│
├── app.py
├── calculator.py
├── database.py
│
├── test_calculator.py
├── test_database.py
├── test_api.py
│
├── requirements.txt
├── .gitignore
├── PSP.md
├── codestyle.md
└── README.md
```

The SQLite database is generated automatically inside
the data directory.

The virtual environment and local database files are
excluded from version control.

## 4. Main Features

### Mathematical Expression Evaluation

The calculator supports:

- Addition
- Subtraction
- Multiplication
- Division
- Decimal numbers
- Parentheses
- Unary positive and negative operators
- Standard mathematical operator precedence

The implementation uses Python's AST module.

Only explicitly permitted mathematical operations
can be evaluated.

The application does not use eval() or exec().

### Error Handling

The calculator handles:

- Empty expressions
- Invalid mathematical syntax
- Division by zero
- Unsupported operators
- Excessively long expressions
- Excessively complex expressions

Invalid calculations are rejected without being
saved to the database.

### Calculation History

Successful calculations are stored in SQLite.

Each history record contains:

- Unique record ID
- Mathematical expression
- Calculation result
- Creation timestamp

Records are retrieved with the newest entries first.

Users can delete individual records by ID.

## 5. Installation

### Requirements

Python 3.12 and pip are required.

### Windows

Create a virtual environment:

```powershell
python -m venv .venv
```

Install dependencies:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Start the backend:

```powershell
.\.venv\Scripts\python.exe app.py
```

The development server runs at:

http://127.0.0.1:5000

### Linux

Create and activate a virtual environment:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Start the backend:

```bash
python app.py
```

## 6. Database Initialization

The database is initialized automatically when
the Flask application is created.

The database contains one table:

calculation_history

The table includes:

| Column | Type | Description |
|---|---|---|
| id | INTEGER | Unique record identifier |
| expression | TEXT | Mathematical expression |
| result | TEXT | Calculation result |
| created_at | TEXT | UTC creation timestamp |

Calculation results are stored as text to preserve
the decimal representation.

## 7. API Documentation

### POST /api/calculate

Evaluates a mathematical expression and saves
the successful calculation.

Example request:

```json
{
    "expression": "(1+2)*3"
}
```

Example successful response:

```json
{
    "success": true,
    "id": 1,
    "expression": "(1+2)*3",
    "result": "9"
}
```

Success status code: 201

Invalid calculation status code: 400

### GET /api/history

Retrieves all saved calculations.

Example response:

```json
{
    "success": true,
    "history": [
        {
            "id": 1,
            "expression": "(1+2)*3",
            "result": "9",
            "created_at": "2026-10-07T02:30:00+00:00"
        }
    ],
    "total": 1
}
```

Success status code: 200

### DELETE /api/history/{id}

Deletes the history record identified by its ID.

Example:

DELETE /api/history/1

Successful deletion returns status code 200.

If the record does not exist, the API returns 404.

### GET /health

Returns the health status of the backend service.

## 8. Testing

The project uses Python's built-in unittest framework.

Run all automated tests:

```bash
python -m unittest discover -v
```

The test suite contains 31 tests covering:

- Mathematical operations
- Expression precedence
- Parentheses
- Decimal arithmetic
- Invalid input
- Division by zero
- Unsafe expressions
- Database initialization
- History insertion
- History retrieval
- History deletion
- Database persistence
- API responses and error handling

The tests use isolated temporary databases
to prevent modification of production data.

## 9. Deployment

The backend is deployed on PythonAnywhere.

Production URL:

https://candice0chen.pythonanywhere.com

The application is loaded through a WSGI configuration.

The production server uses a Python 3.12
virtual environment.

SQLite data is stored in the server's persistent
account storage.

## 10. Security Considerations

The backend uses:

- Explicitly allowed AST operators
- Input length restrictions
- Expression complexity restrictions
- Parameterized SQL queries
- Structured error responses
- Configurable CORS origins

The backend is responsible for all mathematical
calculations and database modifications.

## 11. Repository Information

Student ID: 832401107

Frontend Repository:
https://github.com/Candice-Pooh/832401107_calculator_frontend

Backend Repository:
https://github.com/Candice-Pooh/832401107_calculator_backend