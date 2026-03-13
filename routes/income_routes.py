from flask import Blueprint, request, jsonify
from services.income_service import IncomeExpenseTracker
from db.mongodb import get_db

db = get_db()
income_bp = Blueprint('income_bp', __name__)

income_expense_tracker = IncomeExpenseTracker(db) if db is not None else None




@income_bp.route('/api/income', methods=['POST'])
def add_income_record_api():
    if not request.json or income_expense_tracker is None:
        return jsonify({"error": "Invalid request or database not connected"}), 400
    response, status_code = income_expense_tracker.add_record(request.json)
    return jsonify(response), status_code


@income_bp.route('/api/income', methods=['GET'])
def get_income_records_api():
    if income_expense_tracker is None:
        return jsonify({"error": "Database not connected"}), 500
    response, status_code = income_expense_tracker.view_records()
    return jsonify(response), status_code


