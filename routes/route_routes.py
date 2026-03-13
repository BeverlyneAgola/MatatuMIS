from flask import Blueprint, request, jsonify
from services.route_service import ROUTE_SCHEDULE_MANAGEMENT
from db.mongodb import get_db

db = get_db()
route_bp = Blueprint('route_bp', __name__)

route_schedule_management_system = ROUTE_SCHEDULE_MANAGEMENT(db) if db is not None else None


@route_bp.route('/api/routes', methods=['POST'])
def update_schedule_api():
    if not request.json or route_schedule_management_system is None:
        return jsonify({"error": "Invalid request or database not connected"}), 400
    response, status_code = route_schedule_management_system.update_schedule(request.json)
    return jsonify(response), status_code


@route_bp.route('/api/routes', methods=['GET'])
def get_routes_api():
    if route_schedule_management_system is None:
        return jsonify({"error": "Database not connected"}), 500
    response, status_code = route_schedule_management_system.view_schedule()
    return jsonify(response), status_code