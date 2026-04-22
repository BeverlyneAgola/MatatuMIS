from flask import Blueprint, request, jsonify, render_template
from db.mongodb import get_db
from services.decorator import post_required
from services.schedule_management_service import SCHEDULE_MANAGEMENT


routes_schedules_bp = Blueprint('routes_schedules', __name__, url_prefix="/schedule")



@routes_schedules_bp.route("/")
@post_required(["admin", "hr" ,"HR" ,"manager" , "Driver", "Conductor"])
def schedule_management():
    return render_template("Schedule_management.html")


@routes_schedules_bp.route("/api/update_schedule", methods=["POST"])
@post_required(["admin", "hr" ,"HR" ,"manager"])
def update_schedule():
    db = get_db()

    if db is None:
        return jsonify({"error": "Database not connected"}), 500
    
    service = SCHEDULE_MANAGEMENT(db)

    data = request.get_json()
    result, status = service.update_schedule(data)

    return jsonify(result), status


@routes_schedules_bp.route("/update")
@post_required(["admin", "hr" ,"HR" ,"manager"])
def update_schedule_page():
    print("🔥 UPDATE ROUTE HIT 🔥")
    db = get_db()
    
    if db is None:
        return "Database not connected", 500

    vehicles = list(db['vehicles'].find())
    staff = list(db['staff'].find())
    

    for v in vehicles:
        v['_id'] = str(v.get('_id'))
        v['assigned_route'] = str(v.get('assigned_route') or "").strip()
        v['vehicle_number'] = str(v.get('vehicle_number') or "").strip()

    vehicles_with_route = vehicles

    routes = ["Rongai", "Ngong", "Thika"]

    for s in staff:
        s['_id'] = str(s.get('_id'))
        s['name'] = str(s.get('name') or "").strip()
        s['post'] = str(s.get('post') or s.get('position') or "").lower().strip()

    staff = [s for s in staff if s['post'] in ['driver', 'conductor']]
    
    
    return render_template(
        "schedules/update_schedule.html",
        routes=routes,
        vehicles=vehicles_with_route,
        staff=staff
    )
    
    
@routes_schedules_bp.route("/view")
@post_required(["admin", "hr" ,"HR" ,"manager" , "Driver", "Conductor"])
def view_schedules_page():
    db = get_db()

    if db is None:
        return "Database not connected", 500

    service = SCHEDULE_MANAGEMENT(db)

    route_filter = request.args.get("route")

    result, status = service.view_schedule()
    schedules = result.get("schedules", [])

    routes = list(set(s["route"] for s in schedules if "route" in s))

    if route_filter:
        schedules = [s for s in schedules if s.get("route") == route_filter]

    return render_template(
        "schedules/view_schedules.html",
        schedules=schedules,
        routes=routes,
        selected_route=route_filter
    )