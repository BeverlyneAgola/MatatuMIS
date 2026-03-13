from flask import Blueprint, render_template, request, jsonify
from services.decorator import post_required
from services.report_service import REPORTING_AND_ANALYTICS
from db.mongodb import get_db   
from flask import redirect, url_for, flash

db = get_db()

report_bp = Blueprint('report_bp', __name__)

reporting_analytics_system = REPORTING_AND_ANALYTICS(db) if db is not None else None


@report_bp.route("/reports")
@post_required([ "Admin","finance", "hr", "manager"])
def reports():
    """
    HR Reports page:
    - Step 1: choose action (view reports / file report)
    - Step 2: show table (if view selected)
    """
    reports = []
    selected_category = None
    action = request.args.get("action")  # "view" or "file"
    
    if action == "view":
        selected_category = request.args.get("category")  # e.g., "accident"
        if reporting_analytics_system:
            response, status = reporting_analytics_system.view_reports()
            if status == 200:
                reports = response.get("reports", [])
                if selected_category:
                    # Filter by category
                    reports = [r for r in reports if r["category"] == selected_category]
    
    return render_template("reports/reports.html",
                           action=action,
                           reports=reports,
                           selected_category=selected_category)


@report_bp.route('/api/reports', methods=['POST'])
def generate_report_api():
    if not request.json or reporting_analytics_system is None:
        return jsonify({"error": "Invalid request or database not connected"}), 400
    response, status_code = reporting_analytics_system.generate_report(request.json)
    return jsonify(response), status_code


@report_bp.route('/api/reports', methods=['GET'])
def get_reports_api():
    if reporting_analytics_system is None:
        return jsonify({"error": "Database not connected"}), 500
    response, status_code = reporting_analytics_system.view_reports()
    return jsonify(response), status_code

@report_bp.route('/submit-report', methods=['POST'])
def submit_report():

    if reporting_analytics_system is None:
        return redirect(url_for("main.contact", submitted="false"))

    report_data = {
        "name": request.form.get("name"),
        "email": request.form.get("email"),
        "phone": request.form.get("phone"),
        "category": request.form.get("category"),
        "message": request.form.get("message"),
        "status": "Pending"
    }

    response, status_code = reporting_analytics_system.generate_report(report_data)

    if status_code == 201:
        # Redirect with a query parameter
        return redirect(url_for("main.contact", submitted="true"))
    else:
        return redirect(url_for("main.contact", submitted="false"))