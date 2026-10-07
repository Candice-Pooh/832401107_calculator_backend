"""Integration tests for calculator API endpoints."""

import tempfile
import unittest

from pathlib import Path
from unittest.mock import patch

import database

from app import create_app


class TestCalculatorAPI(unittest.TestCase):
    """Test calculator API requests and responses."""

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()

        self.database_path = (
            Path(self.temp_dir.name) / "api_test.db"
        )

        self.database_patch = patch.object(
            database,
            "DATABASE_PATH",
            self.database_path,
        )

        self.database_patch.start()

        self.app = create_app()
        self.app.config["TESTING"] = True

        self.client = self.app.test_client()

    def tearDown(self):
        self.database_patch.stop()
        self.temp_dir.cleanup()

    def test_home(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json["success"])

    def test_calculate(self):
        response = self.client.post(
            "/api/calculate",
            json={"expression": "(1+2)*3"},
        )

        self.assertEqual(response.status_code, 201)
        self.assertTrue(response.json["success"])
        self.assertEqual(response.json["result"], "9")

    def test_calculation_saves_history(self):
        self.client.post(
            "/api/calculate",
            json={"expression": "12+8"},
        )

        response = self.client.get("/api/history")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["total"], 1)

        record = response.json["history"][0]

        self.assertEqual(record["expression"], "12+8")
        self.assertEqual(record["result"], "20")

    def test_invalid_expression(self):
        response = self.client.post(
            "/api/calculate",
            json={"expression": "1+*/2"},
        )

        self.assertEqual(response.status_code, 400)
        self.assertFalse(response.json["success"])

    def test_division_by_zero(self):
        response = self.client.post(
            "/api/calculate",
            json={"expression": "10/0"},
        )

        self.assertEqual(response.status_code, 400)

        history = self.client.get("/api/history")

        self.assertEqual(history.json["total"], 0)

    def test_missing_expression(self):
        response = self.client.post(
            "/api/calculate",
            json={},
        )

        self.assertEqual(response.status_code, 400)

    def test_invalid_json_body(self):
        response = self.client.post(
            "/api/calculate",
            data="not-json",
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 400)

    def test_delete_history(self):
        calculation = self.client.post(
            "/api/calculate",
            json={"expression": "5*5"},
        )

        record_id = calculation.json["id"]

        response = self.client.delete(
            f"/api/history/{record_id}"
        )

        self.assertEqual(response.status_code, 200)

        history = self.client.get("/api/history")

        self.assertEqual(history.json["total"], 0)

    def test_delete_nonexistent_history(self):
        response = self.client.delete(
            "/api/history/999"
        )

        self.assertEqual(response.status_code, 404)

    def test_unsafe_expression(self):
        response = self.client.post(
            "/api/calculate",
            json={
                "expression": "__import__('os').getcwd()"
            },
        )

        self.assertEqual(response.status_code, 400)


if __name__ == "__main__":
    unittest.main()