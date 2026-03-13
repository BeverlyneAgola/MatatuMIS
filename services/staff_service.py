class STAFF_MANAGEMENT:
    def __init__(self, db):
        self.db = db
        self.collection = db['staff']

    def view_all_staff(self):
        """Retrieves all staff records."""
        try:
            staff_records = list(self.collection.find())
            for staff in staff_records:
                staff['_id'] = str(staff['_id'])
            return {"staff": staff_records}, 200
        except Exception as e:
            return {"error": f"Error viewing staff: {str(e)}"}, 500

    def delete_staff(self, name):
        """Deletes a staff member by name."""
        try:
            result = self.collection.delete_one({"name": name})
            if result.deleted_count > 0:
                return {"message": f"Staff member '{name}' deleted successfully."}, 200
            else:
                return {"error": f"Staff member '{name}' not found."}, 404
        except Exception as e:
            return {"error": f"Error deleting staff: {str(e)}"}, 500