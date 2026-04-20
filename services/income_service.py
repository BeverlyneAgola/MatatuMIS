import datetime

class IncomeExpenseTracker:

    def __init__(self, db):
        self.db = db
        self.collection = db['income']
        self.TAX_RATE = 0.05

    def get_mpesa_income(self, vehicle_number):
        payments = list(self.db["payments"].find({
            "Vehicle": vehicle_number
        }))

        total = 0

        for p in payments:
            total += float(p.get("Amount", 0))

        return total

    def add_record(self, record_data):
        try:
            vehicle = record_data["vehicle_number"]

            print("RECEIVED:", record_data)
            mpesa = self.get_mpesa_income(vehicle)
            cash = float(record_data.get("cash_income", 0))

            revenue = mpesa + cash
            gross = revenue * (1 - self.TAX_RATE)

            save_data = {
                "vehicle_number": vehicle,
                "mpesa_income": mpesa,
                "cash_income": cash,
                "revenue": revenue,
                "gross": gross,
                "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

            self.collection.insert_one(save_data)

            return {"message": "Saved successfully"}, 201
    
        except Exception as e:
            return {"error": str(e)}, 500
        
    def view_records(self):
        try:
            records = list(self.collection.find())

            for r in records:
                r["_id"] = str(r["_id"])

            return {"records": records}, 200

        except Exception as e:
            return {"error": str(e)}, 500
        