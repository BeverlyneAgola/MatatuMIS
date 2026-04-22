from flask import Blueprint, request, jsonify, render_template
from services.decorator import post_required
from services.income_service import IncomeExpenseTracker
from db.mongodb import get_db
from datetime import datetime, timedelta


ROLE_PERMISSIONS = {
    "view": ["admin", "Finance", "Manager"],
    "write": ["admin", "Finance"],
}

income_bp = Blueprint('income_bp', __name__, url_prefix="/income")


@income_bp.route("/")
def income():    
    return render_template("income/income.html")


@income_bp.route("/form")
def income_form():
    return render_template("income/income_form.html")


@income_bp.route("/records")
def income_records_page():
    return render_template("income/income_list.html")


@income_bp.route("/api/income", methods=["POST"])
@post_required(ROLE_PERMISSIONS["write"])
def add_income_record_api():

    db = get_db()
    tracker = IncomeExpenseTracker(db)

    response, status = tracker.add_record(request.get_json())

    return jsonify(response), status


@income_bp.route("/api/income", methods=["GET"])
@post_required(ROLE_PERMISSIONS["view"])
def get_income_records_api():

    db = get_db()
    tracker = IncomeExpenseTracker(db)

    response, status = tracker.view_records()

    return jsonify(response), status


@income_bp.route("/api/vehicles", methods=["GET"])
@post_required(ROLE_PERMISSIONS["view"])
def vehicles():
    db = get_db()

    route = request.args.get("route")

    if not route:
        return jsonify([]), 200

    route = route.strip()

    cursor = db["vehicles"].find(
        {"assigned_route": route},
        {"_id": 0, "vehicle_number": 1}
    )

    return jsonify([v["vehicle_number"] for v in cursor]), 200


@income_bp.route("/api/mpesa", methods=["GET"])
@post_required(ROLE_PERMISSIONS["view"])
def mpesa():
    db = get_db()

    route = request.args.get("route")
    vehicle = request.args.get("vehicle")
    date_str = request.args.get("date")

    if not route or not vehicle or not date_str:
        return jsonify({"error": "Missing route, vehicle, or date"}), 400

    try:
        start = datetime.strptime(date_str, "%Y-%m-%d")
        end = start + timedelta(days=1)
    except Exception:
        return jsonify({"error": "Invalid date format"}), 400

    payments = db["payments"].find({
        "Route": route,
        "Vehicle": vehicle,
        "ReceivedAt": {
            "$gte": start,
            "$lt": end
        }
    })

    transactions = []
    total = 0

    for p in payments:
        amount = float(p.get("Amount", 0))
        total += amount

        transactions.append({
            "phone": p.get("PhoneNumber"),
            "date": p.get("ReceivedAt"),
            "status": p.get("ResultDesc"),
            "checkout_id": p.get("CheckoutRequestID")
        })

    return jsonify({
        "vehicle": vehicle,
        "route": route,
        "date": date_str,
        "mpesa_total": total,
        "transactions": transactions
    })