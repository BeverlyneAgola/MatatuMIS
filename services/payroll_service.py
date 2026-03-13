import datetime


class PAYROLL_MANAGEMENT:
    def __init__(self, db):
        self.db = db
        self.collection = db['payroll']
        self.basic_salaries = {
            "Driver": 50000,
            "Conductor": 30000,
            "Manager": 80000
        }
        self.tax_rate = 0.15

    def calculate_payroll(self, payroll_data):
        """Calculates and stores a single payroll record."""
        try:
            position = payroll_data.get("position", "Unknown").title()
            basic_salary = self.basic_salaries.get(position, 0)
            allowances = payroll_data.get("allowances", 0)
            deductions = payroll_data.get("deductions", 0)

            gross_salary = basic_salary + allowances
            tax_amount = gross_salary * self.tax_rate
            net_salary = gross_salary - deductions - tax_amount

            payroll_data["position"] = position
            payroll_data["basic_salary"] = basic_salary
            payroll_data["gross_salary"] = gross_salary
            payroll_data["tax_amount"] = tax_amount
            payroll_data["net_salary"] = net_salary

            
            self.collection.insert_one(payroll_data)

            return {"message": "Payroll calculation successful!", "payroll": payroll_data}, 201

        except Exception as e:
            return {"error": f"Error calculating payroll: {str(e)}"}, 500

    def view_records(self):
        """Retrieves all payroll records."""
        try:
            records = list(self.collection.find())

            for record in records:
                record["_id"] = str(record["_id"])

            return {"records": records}, 200

        except Exception as e:
            return {"error": f"Error viewing payroll records: {str(e)}"}, 500

    

        except Exception as e:
            return {"error": f"Error retrieving payroll records: {str(e)}"}, 500