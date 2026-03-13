from werkzeug.security import check_password_hash

class LOGIN:
    def __init__(self, db):
        self.db = db
        self.collection = db['staff']

    def login_user(self, email, password):
        user = self.collection.find_one({"email": email})
        if user and check_password_hash(user["password"], password):
        # Return the relevant user info as a dict
            user_data = {
            "name": user.get("name"),
            "email": user.get("email"),
            "post": user.get("post")  # <-- THIS is required for your decorator
        }
            return {"message": "Login successful!", "user": user_data}, 200
        else:
            return {"error": "Invalid email or password."}, 401
