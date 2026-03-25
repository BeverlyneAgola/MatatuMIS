class SCHEDULE_MANAGEMENT:
    def __init__(self, db):
        self.db = db
        self.collection = db['routes_schedules']

    def update_schedule(self, route_data):
        """Updates or creates a route schedule with vehicle validation."""
        try:
            route = route_data.get("route")
            schedule_time = route_data.get("schedule_time")
            vehicle_number = route_data.get("vehicle")  # From form dropdown

            # Validate vehicle exists and is assigned to the route
            vehicle_doc = self.db['vehicles'].find_one({
                "vehicle_number": vehicle_number,
                "route": route
            })
            if not vehicle_doc:
                return {
                    "error": f"Vehicle {vehicle_number} is not registered for route {route}"
                }, 400

            # Update schedule
            self.collection.update_one(
                {"route": route},
                {"$set": {"schedule_time": schedule_time, "vehicle_number": vehicle_number}},
                upsert=True
            )
            return {"message": "Schedule updated successfully!", "route": route_data}, 200

        except Exception as e:
            return {"error": f"Error updating schedule: {str(e)}"}, 500

    def view_schedule(self):
        """Retrieves all schedules."""
        try:
            schedules = list(self.collection.find())
            for schedule in schedules:
                schedule['_id'] = str(schedule['_id'])
            return {"schedules": schedules}, 200
        except Exception as e:
            return {"error": f"Error viewing schedules: {str(e)}"}, 500