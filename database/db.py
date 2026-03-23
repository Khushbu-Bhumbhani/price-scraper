import sqlite3
from pathlib import Path
from typing import Optional


DATABASE_PATH = Path(__file__).resolve().parents[1] / "price_tracker.db"


def get_connection() -> sqlite3.Connection:
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_db() -> None:
    with get_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT NOT NULL UNIQUE,
                title TEXT,
                latest_price_text TEXT,
                latest_price_value REAL,
                latest_rating TEXT,
                updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS price_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id INTEGER NOT NULL,
                price_text TEXT,
                price_value REAL,
                rating TEXT,
                checked_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (product_id) REFERENCES products(id)
            )
            """
        )


def get_product_by_url(url: str) -> Optional[sqlite3.Row]:
    with get_connection() as connection:
        return connection.execute(
            "SELECT * FROM products WHERE url = ?",
            (url,),
        ).fetchone()


def upsert_product(
    url: str,
    title: Optional[str],
    price_text: Optional[str],
    price_value: Optional[float],
    rating: Optional[str],
) -> int:
    with get_connection() as connection:
        existing = connection.execute(
            "SELECT id FROM products WHERE url = ?",
            (url,),
        ).fetchone()

        if existing:
            connection.execute(
                """
                UPDATE products
                SET title = ?, latest_price_text = ?, latest_price_value = ?,
                    latest_rating = ?, updated_at = CURRENT_TIMESTAMP
                WHERE url = ?
                """,
                (title, price_text, price_value, rating, url),
            )
            return int(existing["id"])

        cursor = connection.execute(
            """
            INSERT INTO products (url, title, latest_price_text, latest_price_value, latest_rating)
            VALUES (?, ?, ?, ?, ?)
            """,
            (url, title, price_text, price_value, rating),
        )
        return int(cursor.lastrowid)


def insert_price_history(
    product_id: int,
    price_text: Optional[str],
    price_value: Optional[float],
    rating: Optional[str],
) -> None:
    with get_connection() as connection:
        connection.execute(
            """
            INSERT INTO price_history (product_id, price_text, price_value, rating)
            VALUES (?, ?, ?, ?)
            """,
            (product_id, price_text, price_value, rating),
        )


def get_latest_price_record(product_id: int) -> Optional[sqlite3.Row]:
    with get_connection() as connection:
        return connection.execute(
            """
            SELECT *
            FROM price_history
            WHERE product_id = ?
            ORDER BY id DESC
            LIMIT 1
            """,
            (product_id,),
        ).fetchone()
