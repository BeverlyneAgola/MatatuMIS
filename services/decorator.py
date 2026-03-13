from functools import wraps
from flask import session, redirect, url_for, flash

def post_required(allowed_posts):
    """Decorator to allow access only for users with specific posts."""
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            user_post = session.get("post")
            print("SESSION POST:", user_post)
            print("ALLOWED POSTS:", allowed_posts)

            if not user_post or user_post.lower() not in [p.lower() for p in allowed_posts]:
                flash("Access denied")
                return redirect(url_for("dashboard_bp.dashboard"))

            return f(*args, **kwargs)
        return wrapper
    return decorator