"""SQLite database operations for calculation history."""

import os
import sqlite3

from contextlib import closing
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent

DATABASE_PATH = Path(
    os.environ.get(
        "CALCULATOR_DATABASE_PATH",
        str(BASE_DIR / "data" / "calculator.db"),
    )
)


def init_db() -> None:
    """Create the database and history table if necessary."""

    DATABASE_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with closing(sqlite3.connect(DATABASE_PATH)) as connection:
        with connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS calculation_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    expression TEXT NOT NULL,
                    result TEXT NOT NULL,
                    created_at TEXT NOT NULL
                )
                """
            )


def add_history(expression: str, result: Decimal) -> int:
    """Save a successful calculation and return its ID."""

    created_at = datetime.now(timezone.utc).isoformat(
        timespec="seconds"
    )

    with closing(sqlite3.connect(DATABASE_PATH)) as connection:
        with connection:
            cursor = connection.execute(
                """
                INSERT INTO calculation_history
                    (expression, result, created_at)
                VALUES (?, ?, ?)
                """,
                (
                    expression,
                    str(result),
                    created_at,
                ),
            )

            record_id = cursor.lastrowid

    if record_id is None:
        raise sqlite3.DatabaseError(
            "Failed to retrieve the inserted record ID"
        )

    return record_id


def get_history() -> list[dict]:
    """Retrieve calculation history, newest first."""

    with closing(sqlite3.connect(DATABASE_PATH)) as connection:
        connection.row_factory = sqlite3.Row

        cursor = connection.execute(
            """
            SELECT id, expression, result, created_at
            FROM calculation_history
            ORDER BY id DESC
            """
        )

        records = cursor.fetchall()

    return [dict(record) for record in records]


def delete_history(record_id: int) -> bool:
    """Delete a specific history record."""

    if type(record_id) is not int or record_id <= 0:
        raise ValueError(
            "History ID must be a positive integer"
        )

    with closing(sqlite3.connect(DATABASE_PATH)) as connection:
        with connection:
            cursor = connection.execute(
                """
                DELETE FROM calculation_history
                WHERE id = ?
                """,
                (record_id,),
            )

            deleted = cursor.rowcount > 0

    return deleted