
import datetime
from flask import Blueprint, send_file, jsonify ,render_template , request
from openpyxl import Workbook
from io import BytesIO
from db.mongodb import get_db
import re
from services.decorator import post_required
from services.payroll_service import PAYROLL_MANAGEMENT

payroll_bp = Blueprint('payroll', __name__, url_prefix="/payroll")


@payroll_bp.route("/payroll")
@post_required(["admin", "Finance"])
def payroll_page():
    return render_template("payroll/payroll_dashboard.html")

@payroll_bp.route("/dashboard")
@post_required(["admin", "Finance"])
def payroll_dashboard():
    return render_template("payroll/payroll_dashboard.html")


@payroll_bp.route("/form")
@post_required(["admin", "Finance"])
def payroll_form():
    return render_template("payroll/payroll_form.html")


@payroll_bp.route("/api/staff", methods=["GET"])
@post_required(["admin", "Finance"])
def get_staff():

    db = get_db()

    position = request.args.get("position")
    query = {}

    if position:
        query["post"] = {
            "$regex": f"^{re.escape(position)}$",
            "$options": "i"
        }

    staff = list(db["staff"].find(query))

    service = PAYROLL_MANAGEMENT(db)

    for person in staff:

        person["_id"] = str(person["_id"])

        role = person.get("post", "Driver").title()

        person["role"] = role

        person["name"] = person.get("name", "Unknown")

        person["basic_salary"] = service.basic_salaries.get(role, 0)

    return jsonify(staff)

@payroll_bp.route("/api/calculate", methods=["POST"])
@post_required(["admin", "Finance"])
def calculate_payroll():

    db = get_db()

    service = PAYROLL_MANAGEMENT(db)

    data = request.get_json()

    result, status = service.calculate_payroll(data)

    return jsonify(result), status

@payroll_bp.route("/", methods=["GET"])
@post_required(["admin", "Finance"])
def payroll():
    db = get_db()  # connect to database
    payroll_data = list(db["payroll"].find())  # fetch records

    print("DATA FROM DB:", payroll_data) 
    
    for record in payroll_data:
        record["_id"] = str(record["_id"])
        
    return render_template(
        "payroll/payroll_list.html",
        records=payroll_data
    )


@payroll_bp.route("/api/payroll", methods=["GET"])
@post_required(["admin", "Finance"])
def get_payroll():

    db = get_db()

    position = request.args.get("position")
    month = request.args.get("month")

    query = {}

    # Position filter (case-insensitive)
    if position:
        query["position"] = {
            "$regex": f"^{re.escape(position)}$",
            "$options": "i"
        }

    # Month filter
    if month:
        query["calculation_date"] = {
            "$regex": f"^{month}"
        }

    print("QUERY:", query)

    payroll_data = list(db["payroll"].find(query))

    for record in payroll_data:
        record["_id"] = str(record["_id"])

    return jsonify(payroll_data)


@payroll_bp.route("/export", methods=["GET"])
@post_required(["admin","Finance"])
def export_payroll_excel():

    db = get_db()

    # Get same query parameters as table
    position = request.args.get("position")
    month = request.args.get("month")

    query = {}

    # Position filter (case-insensitive)
    if position:
        query["position"] = {
            "$regex": f"^{re.escape(position)}$",
            "$options": "i"
        }

    # Month filter
    if month:
        query["calculation_date"] = {"$regex": f"^{month}"}

    payroll_data = list(db["payroll"].find(query))

    if not payroll_data:
        return jsonify({"error": "No payroll records found"}), 404

    # Convert ObjectId and datetime to string
    for record in payroll_data:
        record["_id"] = str(record["_id"])
        for key, value in record.items():
            if isinstance(value, datetime.datetime):
                record[key] = value.strftime("%Y-%m-%d %H:%M:%S")
            elif not isinstance(value, (str, int, float)):
                record[key] = str(value)

    # Create Excel
    wb = Workbook()
    ws = wb.active
    ws.title = "Payroll"

    # Get headers dynamically
    headers = set()
    for r in payroll_data:
        headers.update(r.keys())
    headers = list(headers)
    ws.append(headers)

    for r in payroll_data:
        ws.append([r.get(h, "") for h in headers])

    output = BytesIO()
    wb.save(output)
    output.seek(0)
    wb.close()

    return send_file(
        output,
        download_name="payroll_report.xlsx",
        as_attachment=True,
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )