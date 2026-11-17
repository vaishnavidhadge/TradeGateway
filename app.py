
from flask import (
    Flask, request, jsonify, render_template,
    redirect, url_for, session, flash
)
from dotenv import load_dotenv
import os
from functools import wraps

from order_manager import place_order
from config import setup_logging

from database import (
    initialize_database,
    save_order,
    get_all_orders,
    create_user,
    get_user_by_email,
    get_user_by_id,
    verify_password,
    get_dashboard_stats
)

load_dotenv()

app = Flask(__name__)

# Secret key for secure sessions
app.secret_key = os.getenv(
    "SECRET_KEY",
    "change-this-to-a-long-random-secret-before-deployment"
)

app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax"
)

logger = setup_logging()

# Initialize database
initialize_database()


# Check whether user is logged in
def login_required(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("login"))

        return function(*args, **kwargs)

    return wrapper


# Home page
@app.route("/")
def home():
    if "user_id" in session:
        return redirect(url_for("dashboard"))

    return jsonify({
        "status": "success",
        "project": "TradeGateway",
        "mode": "MOCK",
        "message": "Flask API is running"
    })


# Registration page
@app.route("/register", methods=["GET", "POST"])
def register():

    if "user_id" in session:
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        full_name = request.form.get("full_name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        if not full_name or not email or not password:
            flash("Please fill in all fields.", "error")
            return redirect(url_for("register"))

        if len(full_name) > 100 or len(email) > 254:
            flash("Name or email is too long.", "error")
            return redirect(url_for("register"))

        if len(password) < 8:
            flash("Password must contain at least 8 characters.", "error")
            return redirect(url_for("register"))

        if get_user_by_email(email):
            flash("This email is already registered.", "error")
            return redirect(url_for("register"))

        try:
            user_id = create_user(full_name, email, password)

            session.clear()
            session["user_id"] = user_id

            flash("Registration successful!", "success")
            return redirect(url_for("dashboard"))

        except Exception:
            logger.exception("Registration error")
            flash("Could not create your account.", "error")

    return render_template("register.html")


# Login page
@app.route("/login", methods=["GET", "POST"])
def login():

    if "user_id" in session:
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        user = get_user_by_email(email)

        if user and verify_password(user["password"], password):
            session.clear()
            session["user_id"] = user["id"]

            return redirect(url_for("dashboard"))

        flash("Invalid email or password.", "error")

    return render_template("login.html")


# Logout
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


# Dashboard (protected)
@app.route("/dashboard")
@login_required
def dashboard():

    user = get_user_by_id(session["user_id"])

    if not user:
        session.clear()
        return redirect(url_for("login"))

    return render_template("index.html", user=user)


# Place order API (protected)
@app.route("/place-order", methods=["POST"])
@login_required
def place_order_api():

    try:
        data = request.get_json(silent=True)

        if not isinstance(data, dict):
            return jsonify({
                "status": "error",
                "message": "Request body must be valid JSON"
            }), 400

        required_fields = [
            "broker", "symbol", "qty", "side", "order_type"
        ]

        missing = [
            field for field in required_fields if field not in data
        ]

        if missing:
            return jsonify({
                "status": "error",
                "message": "Missing required fields",
                "missing_fields": missing
            }), 400

        broker = data["broker"]
        symbol = data["symbol"]
        qty = data["qty"]
        side = data["side"]
        order_type = data["order_type"]

        if not all(
            isinstance(value, str) and value.strip()
            for value in [broker, symbol, side, order_type]
        ):
            return jsonify({
                "status": "error",
                "message": "Invalid string fields"
            }), 400

        if isinstance(qty, bool) or not isinstance(qty, int) or qty <= 0:
            return jsonify({
                "status": "error",
                "message": "Quantity must be a positive integer"
            }), 400

        broker = broker.strip().lower()
        symbol = symbol.strip().upper()
        side = side.strip().upper()
        order_type = order_type.strip().upper()

        if side not in ["BUY", "SELL"]:
            return jsonify({
                "status": "error",
                "message": "Side must be BUY or SELL"
            }), 400

        if order_type not in ["MARKET", "LIMIT", "SL", "SL-M"]:
            return jsonify({
                "status": "error",
                "message": "Invalid order type"
            }), 400

        result = place_order(
            broker, symbol, qty, side, order_type
        )

        # Save order for the currently logged-in user
        save_order(result, user_id=session["user_id"])

        logger.info(
            "Mock order saved for user %s: %s",
            session["user_id"], result
        )

        return jsonify(result), 200

    except ValueError as error:
        logger.warning("Order rejected: %s", error)

        return jsonify({
            "status": "error",
            "message": str(error)
        }), 400

    except Exception:
        logger.exception("Unexpected order error")

        return jsonify({
            "status": "error",
            "message": "Internal server error"
        }), 500


# User-specific order history
@app.route("/order-history", methods=["GET"])
@login_required
def order_history():

    try:
        orders = get_all_orders(user_id=session["user_id"])

        return jsonify({
            "status": "success",
            "total_orders": len(orders),
            "orders": orders
        })

    except Exception:
        logger.exception("Order history error")

        return jsonify({
            "status": "error",
            "message": "Could not retrieve order history"
        }), 500


# Dashboard analytics API (protected)
@app.route("/api/dashboard-stats", methods=["GET"])
@login_required
def dashboard_stats():

    try:
        stats = get_dashboard_stats(session["user_id"])

        return jsonify({
            "status": "success",
            "stats": stats
        })

    except Exception:
        logger.exception("Dashboard statistics error")

        return jsonify({
            "status": "error",
            "message": "Could not retrieve dashboard statistics"
        }), 500


# Run Flask application
if __name__ == "__main__":

    port = int(os.getenv("PORT", "5005"))

    app.run(
        host="127.0.0.1",
        port=port,
        debug=True
    )
