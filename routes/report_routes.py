from flask import Blueprint, render_template, request, jsonify
from services.decorator import post_required
from services.report_service import REPORTING_AND_ANALYTICS
from db.mongodb import get_db   
from flask import redirect, url_for, flash
from flask import session
db = get_db()

report_bp = Blueprint('report_bp', __name__)

reporting_analytics_system = REPORTING_AND_ANALYTICS(db) if db is not None else None


@report_bp.route("/reports")
@post_required(["admin", "finance", "hr", "manager", "It", "driver", "conductor"])
def reports():

    action = request.args.get("action", "view")
    user_post = session.get("post", "").lower()

    reports = []
    selected_category = None

    # VIEW
    if action == "view":

        if user_post == "finance"  or user_post == "It" or user_post == "driver" or user_post == "conductor":
            flash("Access denied.", "danger")
            return redirect(url_for("report_bp.reports", action="file"))

        selected_category = request.args.get("category")

        if reporting_analytics_system:
            response, status = reporting_analytics_system.view_reports()

            if status == 200:
                reports = response.get("reports", [])

                if selected_category:
                    reports = [
                        r for r in reports
                        if r["category"] == selected_category
                    ]

    return render_template(
        "reports/reports.html",
        action=action,
        reports=reports,
        selected_category=selected_category
    )

@report_bp.route('/api/reports', methods=['POST'])
def generate_report_api():
    if not request.json or reporting_analytics_system is None:
        return jsonify({"error": "Invalid request or database not connected"}), 400
    response, status_code = reporting_analytics_system.generate_report(request.json)
    return jsonify(response), status_code


@report_bp.route('/api/reports', methods=['GET'])
@post_required(["admin", "hr", ])
def get_reports_api():
    if reporting_analytics_system is None:
        return jsonify({"error": "Database not connected"}), 500
    response, status_code = reporting_analytics_system.view_reports()
    return jsonify(response), status_code

@report_bp.route('/submit-report', methods=['POST'])
def submit_report():

    if reporting_analytics_system is None:
        return redirect(url_for("main_bp.contact_us", submitted="false"))

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
        return redirect(url_for("main_bp.contact_us", submitted="true"))
    else:
        return redirect(url_for("main_bp.contact_us", submitted="false"))