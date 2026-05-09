from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)  # allows your HTML files to talk to this server

DB = "essence.db"

# ── Create tables on startup ───────────────────────────────────────────────────
def init_db():
    conn = sqlite3.connect(DB)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            name     TEXT NOT NULL,
            email    TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            user_email TEXT NOT NULL,
            items      TEXT NOT NULL,   -- cart items stored as plain text
            total      REAL NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

# ── REGISTER ───────────────────────────────────────────────────────────────────
# Call with: POST /register  { "name": "Riya", "email": "r@r.com", "password": "123" }
@app.route("/register", methods=["POST"])
def register():
    data     = request.get_json()
    name     = data.get("name")
    email    = data.get("email")
    password = data.get("password")

    if not name or not email or not password:
        return jsonify({"success": False, "message": "All fields are required"}), 400

    try:
        conn = sqlite3.connect(DB)
        conn.execute(
            "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
            (name, email, password)   # plain text password — simple & local only
        )
        conn.commit()
        conn.close()
        return jsonify({"success": True, "message": "Account created!"})
    except Exception:
        return jsonify({"success": False, "message": "Email already registered"}), 400

# ── LOGIN ──────────────────────────────────────────────────────────────────────
# Call with: POST /login  { "email": "r@r.com", "password": "123" }
@app.route("/login", methods=["POST"])
def login():
    data     = request.get_json()
    email    = data.get("email")
    password = data.get("password")

    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    user = conn.execute(
        "SELECT * FROM users WHERE email = ? AND password = ?", (email, password)
    ).fetchone()
    conn.close()

    if user:
        return jsonify({"success": True, "name": user["name"], "email": user["email"]})
    else:
        return jsonify({"success": False, "message": "Wrong email or password"}), 401

# ── SAVE ORDER (when checkout is clicked) ─────────────────────────────────────
# Call with: POST /order  { "email": "r@r.com", "items": "Leather Bag x1, Watch x2", "total": 5698 }
@app.route("/order", methods=["POST"])
def save_order():
    data  = request.get_json()
    email = data.get("email")
    items = data.get("items")
    total = data.get("total")

    conn = sqlite3.connect(DB)
    conn.execute(
        "INSERT INTO orders (user_email, items, total) VALUES (?, ?, ?)",
        (email, items, total)
    )
    conn.commit()
    conn.close()
    return jsonify({"success": True, "message": "Order saved!"})

# ── VIEW ALL ORDERS (for admin) ────────────────────────────────────────────────
# Call with: GET /orders
@app.route("/orders", methods=["GET"])
def get_orders():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    orders = conn.execute("SELECT * FROM orders ORDER BY created_at DESC").fetchall()
    conn.close()
    return jsonify([dict(o) for o in orders])

# ── VIEW ALL USERS (for admin) ─────────────────────────────────────────────────
# Call with: GET /users
@app.route("/users", methods=["GET"])
def get_users():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    users = conn.execute("SELECT id, name, email FROM users").fetchall()
    conn.close()
    return jsonify([dict(u) for u in users])

# ── RUN ────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    init_db()
    print("ESSENCE backend running at http://localhost:5000")
    app.run(debug=True)
