from functools import wraps
from flask import session, redirect, url_for, flash

def post_required(allowed_posts):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):

            user_post = session.get("post", "").strip().lower()

            allowed = [p.strip().lower() for p in allowed_posts]

            if user_post not in allowed:
                flash("Access denied", "danger")
                return redirect(url_for("dashboard_bp.dashboard"))

            return f(*args, **kwargs)

        return wrapper
    return decorator