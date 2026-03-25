from flask import Blueprint, render_template, request, redirect, url_for

main_bp = Blueprint("main_bp", __name__)

# Homepage
@main_bp.route("/")
def home():
    return render_template("main/home.html")

# About Us
@main_bp.route("/about_us")
def about_us():
    return render_template("main/about_us.html")

# Routes & Fares
@main_bp.route("/routes_fare")
def routes_fares():
    return render_template("main/routes_fare.html")

# Contact Us
@main_bp.route("/contact_us")
def contact_us():
    submitted = request.args.get("submitted")  # to show confirmation message
    return render_template("main/Contact_Us.html", submitted=submitted)

# Login
@main_bp.route("/login")
def login():
    return render_template("main/login.html")