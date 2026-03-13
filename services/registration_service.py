class REGISTRATION:
    def __init__(self, db):
        self.db = db
        self.collection = db['staff']

    def register_user(self, user_data: dict):
        """Registers a new staff member with role included."""
        try:
            # Check if email or phone already exists
            if self.collection.find_one({"email": user_data["email"]}):
                return {"error": "Email already registered."}, 400
            if self.collection.find_one({"phone": user_data["phone"]}):
                return {"error": "Phone number already registered."}, 400

            # Optional: validate role
            valid_posts = ["Driver", "Conductor", "HR", "Finance", "Manager", "IT", "Admin"]
            if user_data.get("post") not in valid_posts:
                return {"error": "Invalid post selected."}, 400

            # Insert user
            self.collection.insert_one(user_data)
            return {"message": "Registration successful!", "user": user_data}, 201
        except Exception as e:
            return {"error": f"Error during registration: {str(e)}"}, 500