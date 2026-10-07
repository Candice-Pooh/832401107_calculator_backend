"""Flask API for the calculator system."""

import os
import sqlite3

from flask import Flask, jsonify, request
from flask_cors import CORS

from calculator import calculate_expression
from database import (
    add_history,
    delete_history,
    get_history,
    init_db,
)


def create_app():
    """Create and configure the Flask application."""

    app = Flask(__name__)

    # Allow the frontend to access the API.
    allowed_origins = os.environ.get(
        "FRONTEND_ORIGINS",
        (
            "http://127.0.0.1:5500,"
            "http://localhost:5500,"
            "http://127.0.0.1:5501,"
            "http://localhost:5501,"
            "https://candice-pooh.github.io"
        ),
    ).split(",")

    CORS(
        app,
        resources={
            r"/api/*": {
                "origins": [origin.strip() for origin in allowed_origins]
            }
        },
    )

    # Initialize the database.
    init_db()

    def error_response(message, status_code):
        """Return a standardized error response."""

        return jsonify({
            "success": False,
            "message": message,
        }), status_code

    @app.get("/")
    def home():
        """Check whether the backend is running."""

        return jsonify({
            "success": True,
            "message": "Calculator backend is running",
        })

    @app.get("/health")
    def health():
        """Provide a simple health-check endpoint."""

        return jsonify({
            "status": "ok",
        })

    @app.post("/api/calculate")
    def calculate():
        """Calculate an expression and save its history."""

        data = request.get_json(silent=True)

        if not isinstance(data, dict):
            return error_response(
                "Request body must be a JSON object",
                400,
            )

        expression = data.get("expression")

        try:
            result = calculate_expression(expression)

        except (ValueError, ZeroDivisionError) as error:
            return error_response(str(error), 400)

        try:
            record_id = add_history(expression, result)

        except sqlite3.Error:
            app.logger.exception("Failed to save calculation")
            return error_response("Database operation failed", 500)

        return jsonify({
            "success": True,
            "id": record_id,
            "expression": expression,
            "result": str(result),
        }), 201

    @app.get("/api/history")
    def history():
        """Return all saved calculations."""

        try:
            records = get_history()

        except sqlite3.Error:
            app.logger.exception("Failed to retrieve history")
            return error_response("Database operation failed", 500)

        return jsonify({
            "success": True,
            "history": records,
            "total": len(records),
        }), 200

    @app.delete("/api/history/<int:record_id>")
    def remove_history(record_id):
        """Delete a calculation record by ID."""

        try:
            deleted = delete_history(record_id)

        except ValueError as error:
            return error_response(str(error), 400)

        except sqlite3.Error:
            app.logger.exception("Failed to delete history")
            return error_response("Database operation failed", 500)

        if not deleted:
            return error_response("History record not found", 404)

        return jsonify({
            "success": True,
            "message": "History record deleted successfully",
            "id": record_id,
        }), 200

    return app


app = create_app()


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=int(os.environ.get("PORT", "5000")),
        debug=os.environ.get("FLASK_DEBUG") == "1",
    )