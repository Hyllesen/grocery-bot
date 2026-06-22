import sqlite3
from pathlib import Path

DB_DIR = Path(__file__).parent / "data"
DB_PATH = DB_DIR / "shopping.db"


def _get_connection() -> sqlite3.Connection:
    DB_DIR.mkdir(exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    return conn


def init_db() -> None:
    conn = _get_connection()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_name TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    conn.commit()
    conn.close()


def add_item(item_name: str) -> int:
    conn = _get_connection()
    cur = conn.execute(
        "INSERT INTO items (item_name) VALUES (?)",
        (item_name.strip().lower(),),
    )
    conn.commit()
    row_id = cur.lastrowid
    conn.close()
    return row_id


def get_items() -> list[sqlite3.Row]:
    conn = _get_connection()
    rows = conn.execute(
        "SELECT * FROM items ORDER BY created_at"
    ).fetchall()
    conn.close()
    return rows


def delete_item(item_name: str) -> int:
    conn = _get_connection()
    cur = conn.execute(
        "DELETE FROM items WHERE item_name = ?",
        (item_name.strip().lower(),),
    )
    conn.commit()
    deleted = cur.rowcount
    conn.close()
    return deleted


def search_items_by_prefix(prefix: str) -> list[sqlite3.Row]:
    conn = _get_connection()
    rows = conn.execute(
        "SELECT * FROM items WHERE item_name LIKE ?",
        (prefix + "%",),
    ).fetchall()
    conn.close()
    return rows


def delete_all_items() -> int:
    conn = _get_connection()
    cur = conn.execute("DELETE FROM items")
    conn.commit()
    deleted = cur.rowcount
    conn.close()
    return deleted
