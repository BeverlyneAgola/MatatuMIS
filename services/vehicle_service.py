class VEHICLE_MANAGEMENT:
    def __init__(self, db):
        self.db = db
        self.collection = db['vehicles']

    def register_vehicle(self, vehicle_data: dict):
        """Registers a new vehicle."""
        try:
            self.collection.insert_one(vehicle_data)
            return {"message": "Vehicle registration successful!", "vehicle": vehicle_data}, 201
        except Exception as e:
            return {"error": f"Error during vehicle registration: {str(e)}"}, 500

    def view_vehicles(self):
        """Retrieves all vehicle records."""
        try:
            vehicles = list(self.collection.find())
            for vehicle in vehicles:
                vehicle['_id'] = str(vehicle['_id'])
            return {"vehicles": vehicles}, 200
        except Exception as e:
            return {"error": f"Error viewing vehicles: {str(e)}"}, 500

    def delete_vehicle(self, vehicle_number):
        """Deletes a vehicle by its number."""
        try:
            result = self.collection.delete_one({"vehicle_number": vehicle_number})
            if result.deleted_count > 0:
                return {"message": f"Vehicle '{vehicle_number}' deleted successfully."}, 200
            else:
                return {"error": f"Vehicle '{vehicle_number}' not found."}, 404
        except Exception as e:
            return {"error": f"Error deleting vehicle: {str(e)}"}, 500

    def update_vehicle_route(self, vehicle_number, new_route):
        """Updates a vehicle's assigned route."""
        try:
            result = self.collection.update_one(
                {"vehicle_number": vehicle_number},
                {"$set": {"assigned_route": new_route}}
            )
            if result.modified_count > 0:
                return {"message": f"Route for vehicle '{vehicle_number}' updated to '{new_route}'"}, 200
            else:
                return {"error": f"Vehicle '{vehicle_number}' not found or route was already '{new_route}'"}, 404
        except Exception as e:
            return {"error": f"Error updating vehicle route: {str(e)}"}, 500