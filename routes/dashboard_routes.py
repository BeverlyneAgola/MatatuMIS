from flask import Blueprint, flash, jsonify , render_template, session, redirect, url_for
import datetime
from db.mongodb import get_db

# --- Initialize Blueprint and DB once ---
dashboard_bp = Blueprint("dashboard_bp", __name__, url_prefix="/dashboard")
db = get_db()
payments_col = db["payments"] if db is not None else None


@dashboard_bp.route("/", methods=["GET"])
def dashboard():
    if "user" not in session:
        flash("Please login first", "warning")
        return redirect(url_for("auth_bp.login"))
    return render_template("dashboard/dashboard.html")

@dashboard_bp.route("/api/dashboard-stats", methods=["GET"])
def dashboard_stats():
    if db is None:
        return jsonify({"error": "Database not available"}), 500

    try:
        staff_count = db["staff"].count_documents({})
        vehicle_count = db["vehicles"].count_documents({})
        route_count = db["routes"].count_documents({})
        income_count = db["income"].count_documents({})
        payroll_count = db["payroll"].count_documents({})

        return jsonify({
            "staff_count": staff_count,
            "vehicle_count": vehicle_count,
            "route_count": route_count,
            "income_count": income_count,
            "payroll_count": payroll_count
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- Vehicle income per route ---
@dashboard_bp.route("/api/route-income")
def route_income():
    if payments_col is None:
        return jsonify([])

    pipeline = [
        {"$group": {"_id": "$Route", "total": {"$sum": "$Amount"}}}
    ]
    results = list(payments_col.aggregate(pipeline))
    return jsonify([{"route": r["_id"], "total": r["total"]} for r in results])

# --- Monthly income trend ---
@dashboard_bp.route("/api/monthly-income")
def monthly_income():
    if payments_col is None:
        return jsonify([])

    pipeline = [
        {"$group": {
            "_id": {"month": {"$month": "$ReceivedAt"}},
            "total": {"$sum": "$Amount"}
        }},
        {"$sort": {"_id.month": 1}}
    ]
    results = list(payments_col.aggregate(pipeline))
    monthNames = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
    return jsonify([{"month": monthNames[r["_id"]["month"]-1], "total": r["total"]} for r in results])

# --- Recent M-Pesa payments ---
@dashboard_bp.route("/api/recent-payments")
def recent_payments():
    if payments_col is None:
        return jsonify([])

    results = list(payments_col.find().sort("ReceivedAt", -1).limit(10))

    def format_date(dt):
        if not dt:
            return "-"
        if isinstance(dt, datetime.datetime):
            return dt.strftime("%Y-%m-%d %H:%M:%S")
        return str(dt)

    payments = []
    for p in results:
        payments.append({
            "receipt": p.get("TransactionID", "-"),
            "checkout_id": p.get("CheckoutRequestID", "-"),
            "phone": p.get("PhoneNumber", "-"),
            "route": p.get("Route", "-"),
            "vehicle": p.get("Vehicle", "-"),
            "date": format_date(p.get("ReceivedAt")),
            "amount": p.get("Amount", 0)
        })

    return jsonify(payments), 200