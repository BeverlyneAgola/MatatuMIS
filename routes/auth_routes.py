from unittest import result
from flask import Blueprint, request, jsonify, url_for, redirect, render_template , session, flash
from services.registration_service import REGISTRATION
from services.login_service import LOGIN
from db.mongodb import get_db
from werkzeug.security import generate_password_hash

db = get_db()

auth_bp = Blueprint('auth_bp', __name__)

registration_system = REGISTRATION(db) if db is not None else None
login_system = LOGIN(db) if db is not None else None

@auth_bp.route("/api/register", methods=["POST"])
def api_register():
    if registration_system is None:
        return jsonify({"error": "Database not connected"}), 500

    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    phone = data.get("phone")
    password = data.get("password")
    post = data.get("post")  # <-- added role

    # Validate input
    if not name or not email or not phone or not password or not post:
        return jsonify({"error": "All fields are required"}), 400

    # Hash password before storing
    hashed_password = generate_password_hash(password)

    user_data = {
        "name": name,
        "email": email,
        "phone": phone,
        "password": hashed_password,
        "post": post
    }
    response, status_code = registration_system.register_user(user_data)

    return jsonify(response), status_code

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        
        result ,status_code = login_system.login_user(email, password)  # Replace 

        if status_code == 200:
            session.clear()
            user = result["user"]  
            session["user"] = user
            session["post"] = user.get("post", "").strip().lower()  
            session["email"] = user.get("email")
            flash(result["message"], "success")
            return redirect(url_for("dashboard_bp.dashboard"))
        else:
            flash("Invalid credentials", "danger")
            return redirect(url_for("auth_bp.login"))

    return render_template("login.html")