from flask import Blueprint, request, jsonify, render_template
from db.mongodb import get_db
from services.schedule_management_service import SCHEDULE_MANAGEMENT

db = get_db()
routes_schedules_bp = Blueprint('routes_schedules', __name__, url_prefix="/schedule")
schedule_management_system = SCHEDULE_MANAGEMENT(db) if db is not None else None


@routes_schedules_bp.route("/")
def schedule_management():
    return render_template("Schedule_management.html")


@routes_schedules_bp.route("/api/update_schedule", methods=["POST"])
def update_schedule():
    if schedule_management_system is None:
        return jsonify({"error": "Database not connected"}), 500

    data = request.get_json()
    result, status = schedule_management_system.update_schedule(data)
    return jsonify(result), status


@routes_schedules_bp.route("/update")
def update_schedule_page():
    if schedule_management_system is None:
        return "Database not connected", 500

    # Get all vehicles
    vehicles = list(db['vehicles'].find())
    for v in vehicles:
        v['_id'] = str(v['_id'])
        v['assigned_route'] = v.get('assigned_route', "").strip()
        v['vehicle_number'] = v.get('vehicle_number', "").strip()

    # Filter out vehicles that have no assigned route
    vehicles_with_route = [v for v in vehicles if v['assigned_route']]

    # Get unique routes from vehicles that actually have a vehicle
    routes = list(set([v['assigned_route'] for v in vehicles_with_route]))

    return render_template(
        "schedules/update_schedule.html",
        routes=routes,
        vehicles=vehicles_with_route
    )
@routes_schedules_bp.route("/view")
def view_schedules_page():
    if schedule_management_system is None:
        return "Database not connected", 500

    route_filter = request.args.get("route")

    result, status = schedule_management_system.view_schedule()
    schedules = result.get("schedules", [])

    # Get unique routes for dropdown
    routes = list(set([s["route"] for s in schedules]))

    # Apply filter if selected
    if route_filter:
        schedules = [s for s in schedules if s["route"] == route_filter]

    return render_template(
        "schedules/view_schedules.html",
        schedules=schedules,
        routes=routes,
        selected_route=route_filter
    )
    
    
