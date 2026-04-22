from flask import Blueprint, render_template, request, jsonify
from services.decorator import post_required
from services.vehicle_service import VEHICLE_MANAGEMENT
from db.mongodb import get_db

db = get_db()

vehicle_bp = Blueprint('vehicle_bp', __name__)

vehicle_management_system = VEHICLE_MANAGEMENT(db) if db is not None else None


@vehicle_bp.route("/vehicles")
@post_required(["Admin", "manager"])
def vehicles():
    return render_template("vehicles/vehicles_list.html")

@vehicle_bp.route('/api/vehicles', methods=['POST'])
@post_required(["Admin", "Manager"])
def register_vehicle_api():
    if not request.json or vehicle_management_system is None:
        return jsonify({"error": "Invalid request or database not connected"}), 400
    response, status_code = vehicle_management_system.register_vehicle(request.json)
    return jsonify(response), status_code

@vehicle_bp.route('/api/vehicles', methods=['GET'])
@post_required(["Admin", "Manager"])
def get_vehicles_api():
    if vehicle_management_system is None:
        return jsonify({"error": "Database not connected"}), 500
    response, status_code = vehicle_management_system.view_vehicles()
    return jsonify(response), status_code


@vehicle_bp.route('/api/vehicles/<vehicle_number>', methods=['DELETE'])
@post_required(["Admin", "Manager"])
def delete_vehicle_api(vehicle_number):
    if vehicle_management_system is None:
        return jsonify({"error": "Database not connected"}), 500
    response, status_code = vehicle_management_system.delete_vehicle(vehicle_number)
    return jsonify(response), status_code


@vehicle_bp.route('/api/vehicles/update-route', methods=['POST'])
@post_required(["Admin", "Manager"])
def update_vehicle_route_api():
    if not request.json or vehicle_management_system is None:
        return jsonify({"error": "Invalid request or database not connected"}), 400
    vehicle_number = request.json.get('vehicle_number')
    new_route = request.json.get('new_route')

    if not vehicle_number or not new_route:
        return jsonify({"error": "Vehicle number and new route are required"}), 400

    response, status_code = vehicle_management_system.update_vehicle_route(vehicle_number, new_route)
    return jsonify(response), status_code