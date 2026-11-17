
import sqlite3
import os
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

# Database location
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_DIR = os.path.join(BASE_DIR, "instance")
os.makedirs(DATABASE_DIR, exist_ok=True)

DATABASE_PATH = os.path.join(DATABASE_DIR, "orders.db")


# Connect to database
def get_connection():
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection


# Create database tables
def initialize_database():
    connection = get_connection()

    try:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                broker TEXT NOT NULL,
                order_id TEXT NOT NULL UNIQUE,
                symbol TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                side TEXT NOT NULL,
                order_type TEXT NOT NULL,
                status TEXT NOT NULL,
                mode TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        """)

        connection.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE COLLATE NOCASE,
                password TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        """)

        connection.commit()

    finally:
        connection.close()


# Register a new user
def create_user(full_name, email, password):
    hashed_password = generate_password_hash(password)
    connection = get_connection()

    try:
        cursor = connection.execute("""
            INSERT INTO users (full_name, email, password, created_at)
            VALUES (?, ?, ?, ?)
        """, (
            full_name,
            email.lower().strip(),
            hashed_password,
            datetime.now().isoformat()
        ))

        connection.commit()
        return cursor.lastrowid

    finally:
        connection.close()


# Find user using email
def get_user_by_email(email):
    connection = get_connection()

    try:
        user = connection.execute("""
            SELECT * FROM users
            WHERE email = ?
        """, (email.lower().strip(),)).fetchone()

        return dict(user) if user else None

    finally:
        connection.close()


# Find user using ID
def get_user_by_id(user_id):
    connection = get_connection()

    try:
        user = connection.execute("""
            SELECT id, full_name, email, created_at
            FROM users
            WHERE id = ?
        """, (user_id,)).fetchone()

        return dict(user) if user else None

    finally:
        connection.close()


# Verify password
def verify_password(stored_password, entered_password):
    return check_password_hash(stored_password, entered_password)


# Save an order for a user
def save_order(order, user_id=None):
    connection = get_connection()

    try:
        connection.execute("""
            INSERT INTO orders (
                user_id,
                broker,
                order_id,
                symbol,
                quantity,
                side,
                order_type,
                status,
                mode,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            user_id,
            order["broker"],
            order["order_id"],
            order["symbol"],
            order["quantity"],
            order["side"],
            order["order_type"],
            order["status"],
            order["mode"],
            order["timestamp"]
        ))

        connection.commit()

    finally:
        connection.close()


# Get orders (all users or one user)
def get_all_orders(user_id=None):
    connection = get_connection()

    try:
        if user_id is None:
            orders = connection.execute("""
                SELECT * FROM orders
                ORDER BY id DESC
            """).fetchall()

        else:
            orders = connection.execute("""
                SELECT * FROM orders
                WHERE user_id = ?
                ORDER BY id DESC
            """, (user_id,)).fetchall()

        return [dict(order) for order in orders]

    finally:
        connection.close()


# Get dashboard statistics for one user
def get_dashboard_stats(user_id):
    connection = get_connection()

    try:
        summary = connection.execute("""
            SELECT
                COUNT(*) AS total_orders,
                SUM(CASE WHEN side = 'BUY' THEN 1 ELSE 0 END) AS buy_orders,
                SUM(CASE WHEN side = 'SELL' THEN 1 ELSE 0 END) AS sell_orders
            FROM orders
            WHERE user_id = ?
        """, (user_id,)).fetchone()

        broker_rows = connection.execute("""
            SELECT broker, COUNT(*) AS total
            FROM orders
            WHERE user_id = ?
            GROUP BY broker
            ORDER BY total DESC
        """, (user_id,)).fetchall()

        return {
            "total_orders": summary["total_orders"] or 0,
            "buy_orders": summary["buy_orders"] or 0,
            "sell_orders": summary["sell_orders"] or 0,
            "broker_summary": [
                {
                    "broker": row["broker"],
                    "total": row["total"]
                }
                for row in broker_rows
            ]
        }

    finally:
        connection.close()
