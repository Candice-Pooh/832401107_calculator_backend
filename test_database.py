"""Unit tests for SQLite database operations."""

import tempfile
import unittest

from decimal import Decimal
from pathlib import Path
from unittest.mock import patch

import database


class TestDatabase(unittest.TestCase):
    """Test database operations using an isolated test database."""

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()

        self.database_path = (
            Path(self.temp_dir.name) / "test_calculator.db"
        )

        self.patch_database = patch.object(
            database,
            "DATABASE_PATH",
            self.database_path,
        )

        self.patch_database.start()

        database.init_db()

    def tearDown(self):
        self.patch_database.stop()
        self.temp_dir.cleanup()

    def test_database_creation(self):
        self.assertTrue(self.database_path.exists())

    def test_add_history(self):
        record_id = database.add_history(
            "12+8",
            Decimal("20"),
        )

        self.assertIsInstance(record_id, int)

        records = database.get_history()

        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]["expression"], "12+8")
        self.assertEqual(records[0]["result"], "20")

    def test_history_order(self):
        database.add_history("1+1", Decimal("2"))
        database.add_history("2+2", Decimal("4"))

        records = database.get_history()

        self.assertEqual(len(records), 2)
        self.assertEqual(records[0]["expression"], "2+2")
        self.assertEqual(records[1]["expression"], "1+1")

    def test_delete_history(self):
        record_id = database.add_history(
            "5*5",
            Decimal("25"),
        )

        self.assertTrue(database.delete_history(record_id))
        self.assertEqual(database.get_history(), [])

    def test_delete_nonexistent_record(self):
        self.assertFalse(database.delete_history(999))

    def test_invalid_record_id(self):
        for record_id in [-1, 0, "abc", True]:
            with self.subTest(record_id=record_id):
                with self.assertRaises(ValueError):
                    database.delete_history(record_id)

    def test_history_persistence(self):
        database.add_history(
            "10/2",
            Decimal("5"),
        )

        # Reinitialize the database without deleting its data.
        database.init_db()

        records = database.get_history()

        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]["result"], "5")


if __name__ == "__main__":
    unittest.main()