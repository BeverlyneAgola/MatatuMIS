class IncomeExpenseTracker:
    def __init__(self, db):
        self.db = db
        self.collection = db['income_expenses']
        self.TAX_RATE = 0.05

    def add_record(self, record_data):
        """Adds a new income/expense record."""
        try:
            revenue = record_data.get("revenue", 0)
            expense = record_data.get("expenses", 0)
            record_data["gross"] = revenue * (1 - self.TAX_RATE)
            record_data["net_income"] = record_data["gross"] - expense
            self.collection.insert_one(record_data)
            return {"message": "Income and expense record added successfully!", "record": record_data}, 201
        except Exception as e:
            return {"error": f"Error adding record: {str(e)}"}, 500

    def view_records(self):
        """Retrieves all income/expense records."""
        try:
            records = list(self.collection.find())
            for record in records:
                record['_id'] = str(record['_id'])
            return {"records": records}, 200
        except Exception as e:
            return {"error": f"Error viewing records: {str(e)}"}, 500
