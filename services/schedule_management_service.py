class SCHEDULE_MANAGEMENT:
    def __init__(self, db):
        self.db = db
        self.collection = db['routes_schedules']

    def update_schedule(self, route_data):
        try:
            route = route_data.get("route")
            schedule_time = route_data.get("schedule_time")
            vehicle_number = route_data.get("vehicle")

            shift1 = route_data.get("shift1", {})
            shift2 = route_data.get("shift2", {})
            stages = route_data.get("stages", [])

            # ---------------- VALIDATE VEHICLE ----------------
            vehicle_doc = self.db['vehicles'].find_one({
                "vehicle_number": vehicle_number,
            })

            if not vehicle_doc:
                return {
                    "error": f"Vehicle {vehicle_number} is not assigned to route {route}"
                }, 400

            # ---------------- BUILD FULL DOCUMENT ----------------
            schedule_doc = {
                "route": route,
                "vehicle_number": vehicle_number,
                "schedule_time": schedule_time,

                "driver1": shift1.get("driver"),
                "conductor1": shift1.get("conductor"),

                "driver2": shift2.get("driver"),
                "conductor2": shift2.get("conductor"),

                "stages": stages
            }

            # ---------------- SAVE (DO NOT OVERWRITE OLD ROUTES) ----------------
            self.collection.update_one(
                {
                    "route": route,
                    "vehicle_number": vehicle_number
                },
                {"$set": schedule_doc},
                upsert=True
            )

            return {
                "message": "Schedule updated successfully!",
                "data": schedule_doc
            }, 200

        except Exception as e:
            return {"error": f"Error updating schedule: {str(e)}"}, 500

    def view_schedule(self):
        try:
            schedules = list(self.collection.find())

            for s in schedules:
                s['_id'] = str(s['_id'])

            return {"schedules": schedules}, 200

        except Exception as e:
            return {"error": str(e)}, 500