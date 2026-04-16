from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any

from flask import Flask, jsonify, render_template, request

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "cloud_data.db"

app = Flask(__name__)


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS cloud_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                data_type TEXT NOT NULL,
                storage_region TEXT NOT NULL,
                description TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
            """
        )


@app.route("/")
def home() -> str:
    return render_template("index.html")


@app.route("/api/records", methods=["GET"])
def list_records() -> Any:
    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT id, title, data_type, storage_region, description, created_at
            FROM cloud_records
            ORDER BY created_at DESC
            """
        ).fetchall()

    return jsonify([dict(row) for row in rows])


@app.route("/api/records", methods=["POST"])
def add_record() -> Any:
    payload = request.get_json(silent=True) or {}

    required_fields = ["title", "data_type", "storage_region"]
    missing = [field for field in required_fields if not str(payload.get(field, "")).strip()]
    if missing:
        return jsonify({"error": f"Missing required fields: {', '.join(missing)}"}), 400

    title = payload["title"].strip()
    data_type = payload["data_type"].strip()
    storage_region = payload["storage_region"].strip()
    description = str(payload.get("description", "")).strip()

    with get_connection() as conn:
        cursor = conn.execute(
            """
            INSERT INTO cloud_records (title, data_type, storage_region, description)
            VALUES (?, ?, ?, ?)
            """,
            (title, data_type, storage_region, description),
        )
        conn.commit()
        record_id = cursor.lastrowid

        created = conn.execute(
            """
            SELECT id, title, data_type, storage_region, description, created_at
            FROM cloud_records
            WHERE id = ?
            """,
            (record_id,),
        ).fetchone()

    return jsonify(dict(created)), 201


@app.route("/api/records/<int:record_id>", methods=["DELETE"])
def delete_record(record_id: int) -> Any:
    with get_connection() as conn:
        cursor = conn.execute("DELETE FROM cloud_records WHERE id = ?", (record_id,))
        conn.commit()

    if cursor.rowcount == 0:
        return jsonify({"error": "Record not found"}), 404

    return jsonify({"message": "Record deleted"})


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
