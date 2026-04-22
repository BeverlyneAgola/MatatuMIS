from flask import Blueprint, jsonify, render_template , request, redirect, url_for, flash
from services.staff_service import STAFF_MANAGEMENT
from services.registration_service import REGISTRATION
from db.mongodb import get_db
from services.decorator import post_required

db = get_db()
staff_bp = Blueprint('staff_bp', __name__)

staff_management_system = STAFF_MANAGEMENT(db) if db is not None else None



@staff_bp.route("/staff/staff_management")
@post_required(["admin", "hr" ,"HR" ,"manager"])
def staff_management():
    return render_template("staff/staff_management.html")

@staff_bp.route("/staff")
@post_required(["admin", "hr" ,"manager"])
def staff_page():
    return render_template("staff.html")

# View staff list
@staff_bp.route("/staff/view")
@post_required(["admin", "hr" ,"manager"])
def view_staff():
    return render_template("staff/staff_list.html")


# Register staff
@staff_bp.route("/staff/register", methods=["GET", "POST"])
@post_required(["admin", "hr" ])
def register_staff():
    registration = REGISTRATION(db)  # instantiate the service

    if request.method == "POST":
        # Get data from form submission
        name = request.form.get("name")
        email = request.form.get("email")
        post = request.form.get("post")
        
        # Call your service to add staff
        response, status_code = registration.add_staff(name, email, post)

        if status_code == 201:
            flash("Staff registered successfully!", "success")
            return redirect(url_for("staff_bp.staff_management"))
        else:
            flash(response.get("error", "Registration failed"), "danger")
            return redirect(url_for("staff_bp.register_staff"))

    # GET request → just render registration form
    return render_template("auth/register.html")


# API: Get staff
@staff_bp.route('/api/staff', methods=['GET'])
@post_required(["admin", "hr", "manager"])
def get_staff_api():
    if staff_management_system is None:
        return jsonify({"error": "Database not connected"}), 500

    response, status_code = staff_management_system.view_all_staff()
    return jsonify(response), status_code


# API: Delete staff
@staff_bp.route('/api/staff/<staff_name>', methods=['DELETE'])
@post_required([ "admin", "hr" ,"HR" ])
def delete_staff_api(staff_name):
    if staff_management_system is None:
        return jsonify({"error": "Database not connected"}), 500

    response, status_code = staff_management_system.delete_staff(staff_name)
    return jsonify(response), status_code